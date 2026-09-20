#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

static double g_freq;
static double g_startTime;

static double now_us(void) {
    LARGE_INTEGER li;
    QueryPerformanceCounter(&li);
    return (double)li.QuadPart / g_freq * 1e6;
}

static double elapsed_us(void) {
    return now_us() - g_startTime;
}

static volatile double g_sink;

static void busy_work_internal(int count) {
    double x = 0.5;
    double mu = 1.5;
    for (int i = 0; i < count; i++) {
        x = 1.0 - mu * x * x;
    }
    g_sink = x;
}

static int g_busyCountPerSec;
static double g_busyDuration;

static void calibrate(void) {
    int testCount = 5000000;

    double start = now_us();
    busy_work_internal(testCount);
    double elapsed = (now_us() - start) / 1e6;

    g_busyCountPerSec = (int)(testCount / elapsed + 0.5);

    start = now_us();
    busy_work_internal(g_busyCountPerSec);
    g_busyDuration = (now_us() - start) / 1e6;
}

struct WorkerParam {
    double wallTime;
    int nCycles;
    double busySeconds;
    double idleSeconds;
    int startWithBusy;
    int useAffinity;
};

DWORD WINAPI worker(LPVOID arg) {
    WorkerParam* p = (WorkerParam*)arg;

    if (p->useAffinity) {
        SetThreadAffinityMask(GetCurrentThread(), 1);
    }

    DWORD tid = GetCurrentThreadId();
    int busyIters = (int)(g_busyCountPerSec * p->busySeconds + 0.5);

    double startTime = now_us();
    for (int i = 0; i < p->nCycles * 2; i++) {
        int cycleNum = i / 2;
        int isBusy = (i % 2 == (p->startWithBusy ? 0 : 1)) ? 1 : 0;

        if (isBusy) {
            printf("[%10.3f us] TID=%lu cycle=%d: BUSY start (%.1fs)\n",
                   elapsed_us(), (unsigned long)tid, cycleNum, p->busySeconds);
            busy_work_internal(busyIters);
            printf("[%10.3f us] TID=%lu cycle=%d: BUSY end\n",
                   elapsed_us(), (unsigned long)tid, cycleNum);
        } else if (p->idleSeconds > 0) {
            printf("[%10.3f us] TID=%lu cycle=%d: IDLE start (%.1fs)\n",
                   elapsed_us(), (unsigned long)tid, cycleNum, p->idleSeconds);
            Sleep((DWORD)(p->idleSeconds * 1000.0 + 0.5));
            printf("[%10.3f us] TID=%lu cycle=%d: IDLE end\n",
                   elapsed_us(), (unsigned long)tid, cycleNum);
        }
    }

    p->wallTime = (now_us() - startTime) / 1e6;
    printf("[%10.3f us] TID=%lu: DONE (wall: %.3f s)\n",
           elapsed_us(), (unsigned long)tid, p->wallTime);
    return 0;
}

static double run_scenario1(int nCycles, double busySec, double idleSec) {
    printf("\n=== Scenario 1: Single Thread (no contention) ===\n");
    printf("BUSY=%.1fs  IDLE=%.1fs  cycles=%d\n\n", busySec, idleSec, nCycles);

    g_startTime = now_us();

    WorkerParam param;
    param.wallTime = 0.0;
    param.nCycles = nCycles;
    param.busySeconds = busySec;
    param.idleSeconds = idleSec;
    param.startWithBusy = 1;
    param.useAffinity = 1;

    HANDLE h = CreateThread(NULL, 0, worker, &param, 0, NULL);
    if (!h) {
        fprintf(stderr, "  Failed to create thread\n");
        return -1.0;
    }
    WaitForSingleObject(h, INFINITE);
    CloseHandle(h);

    printf("\n  >> Scenario 1 result: %.3f s\n", param.wallTime);
    return param.wallTime;
}

static double run_scenario2(int nCycles, double busySec, double idleSec) {
    printf("\n=== Scenario 2: Two Threads on Core 0 (SetThreadAffinityMask) ===\n");
    printf("BUSY=%.1fs  IDLE=%.1fs  cycles=%d\n", busySec, idleSec, nCycles);
    printf("T1 starts BUSY, T2 starts IDLE (phase offset)\n\n");

    g_startTime = now_us();

    WorkerParam p1, p2;
    p1.wallTime = 0.0; p1.nCycles = nCycles;
    p1.busySeconds = busySec; p1.idleSeconds = idleSec;
    p1.startWithBusy = 1; p1.useAffinity = 1;

    p2.wallTime = 0.0; p2.nCycles = nCycles;
    p2.busySeconds = busySec; p2.idleSeconds = idleSec;
    p2.startWithBusy = 0; p2.useAffinity = 1;

    HANDLE h1 = CreateThread(NULL, 0, worker, &p1, 0, NULL);
    HANDLE h2 = CreateThread(NULL, 0, worker, &p2, 0, NULL);

    if (!h1 || !h2) {
        fprintf(stderr, "  Failed to create threads\n");
        return -1.0;
    }

    WaitForSingleObject(h1, INFINITE);
    WaitForSingleObject(h2, INFINITE);

    CloseHandle(h1);
    CloseHandle(h2);

    double overall = (now_us() - g_startTime) / 1e6;
    printf("\n  >> Thread-1 wall: %.3f s\n", p1.wallTime);
    printf("  >> Thread-2 wall: %.3f s\n", p2.wallTime);
    printf("  >> Overall wall:  %.3f s\n", overall);
    return (p1.wallTime + p2.wallTime) / 2.0;
}

static void print_usage(void) {
    printf("Usage: thread_switch_demo.exe <scenario> [busy_seconds] [idle_seconds] [n_cycles]\n");
    printf("  scenario   1 = single thread (no contention)\n");
    printf("              2 = two threads on CPU 0 (T1 BUSY first, T2 IDLE first)\n");
    printf("  busy_seconds   target CPU-work per BUSY period (default: 1)\n");
    printf("  idle_seconds   sleep per IDLE period (default: 0; skip if 0)\n");
    printf("  n_cycles       number of BUSY/IDLE cycles (default: 5)\n");
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_usage();
        return 1;
    }

    int scenario = atoi(argv[1]);
    if (scenario < 1 || scenario > 2) {
        print_usage();
        return 1;
    }

    double busySec = 1.0;
    if (argc > 2) {
        double val = atof(argv[2]);
        if (val > 0) busySec = val;
    }

    double idleSec = 0.0;
    if (argc > 3) {
        double val = atof(argv[3]);
        if (val >= 0) idleSec = val;
    }

    int nCycles = 5;
    if (argc > 4) {
        int val = atoi(argv[4]);
        if (val > 0) nCycles = val;
    }

    LARGE_INTEGER li;
    QueryPerformanceFrequency(&li);
    g_freq = (double)li.QuadPart;

    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);

    printf("=== Thread Context Switch Demo ===\n");
    printf("System: %lu logical CPU(s)\n", sysInfo.dwNumberOfProcessors);
    printf("Busy work: x = 1 - mu*x*x  (logistic map, thread-local)\n");
    fflush(stdout);

    printf("\nCalibrating ... ");
    fflush(stdout);
    calibrate();
    printf("%d iter/s  (%.3f s solo)\n", g_busyCountPerSec, g_busyDuration);
    fflush(stdout);

    double result;
    if (scenario == 1) {
        result = run_scenario1(nCycles, busySec, idleSec);
    } else {
        result = run_scenario2(nCycles, busySec, idleSec);
    }

    if (result < 0) return 1;

    printf("\nDone (%.3f s)\n", result);
    return 0;
}
