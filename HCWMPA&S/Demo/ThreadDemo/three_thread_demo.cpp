#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 3

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

static HANDLE g_hWake[NUM_THREADS];

struct WorkerParam {
    int id;
    int nRounds;
    double busySeconds;
    double wallTime;
};

DWORD WINAPI worker(LPVOID arg) {
    WorkerParam* p = (WorkerParam*)arg;

    SetThreadAffinityMask(GetCurrentThread(), 0x3);

    int busyIters = (int)(g_busyCountPerSec * p->busySeconds + 0.5);
    double startTime = now_us();

    for (int round = 0; round < p->nRounds; round++) {
        WaitForSingleObject(g_hWake[p->id], INFINITE);
        printf("[%10.3f us] T%d round=%d: WOKEN (Core=%u)\n",
               elapsed_us(), p->id + 1, round,
               (unsigned)GetCurrentProcessorNumber());

        if (p->id == 0 && round == 0) {
            printf("[%10.3f us] T1 round=%d: wakes T2\n", elapsed_us(), round);
            SetEvent(g_hWake[1]);
        }

        busy_work_internal(busyIters);
        busy_work_internal(busyIters);

        int next = (p->id == 0) ? 2 : (p->id == 1) ? 0 : 1;
        printf("[%10.3f us] T%d round=%d: wakes T%d, goes idle\n",
               elapsed_us(), p->id + 1, round, next + 1);
        SetEvent(g_hWake[next]);
    }

    p->wallTime = (now_us() - startTime) / 1e6;
    printf("[%10.3f us] T%d: DONE (wall: %.3f s)\n",
           elapsed_us(), p->id + 1, p->wallTime);
    return 0;
}

int main(int argc, char* argv[]) {
    double busySec = 1.0;
    if (argc > 1) {
        double val = atof(argv[1]);
        if (val > 0) busySec = val;
    }

    int nRounds = 5;
    if (argc > 2) {
        int val = atoi(argv[2]);
        if (val > 0) nRounds = val;
    }

    LARGE_INTEGER li;
    QueryPerformanceFrequency(&li);
    g_freq = (double)li.QuadPart;

    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);

    if (sysInfo.dwNumberOfProcessors < 2) {
        fprintf(stderr, "This demo requires at least 2 logical CPUs\n");
        return 1;
    }

    printf("=== Three Threads on Two Cores ===\n");
    printf("System: %lu logical CPU(s)\n", sysInfo.dwNumberOfProcessors);
    printf("Threads pinned to cores 0-1 (SetThreadAffinityMask 0x3)\n");
    printf("Busy work: x = 1 - mu*x*x  (logistic map, thread-local)\n");
    printf("\nWake-up chain:\n");
    printf("  main -> T1 (init)\n");
    printf("  T1 wakes T2 during its 1st busy period (init)\n");
    printf("  T1 ends -> wakes T3,  T2 ends -> wakes T1,  T3 ends -> wakes T2\n\n");
    fflush(stdout);

    printf("Calibrating ... ");
    fflush(stdout);
    calibrate();
    printf("%d iter/s  (%.3f s solo)\n\n", g_busyCountPerSec, g_busyDuration);

    for (int i = 0; i < NUM_THREADS; i++) {
        g_hWake[i] = CreateEventA(NULL, FALSE, FALSE, NULL);
        if (!g_hWake[i]) {
            fprintf(stderr, "Failed to create event %d (error %lu)\n", i, GetLastError());
            return 1;
        }
    }

    WorkerParam params[NUM_THREADS];
    HANDLE hThreads[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        params[i].id = i;
        params[i].nRounds = nRounds;
        params[i].busySeconds = busySec;
        params[i].wallTime = 0.0;
        hThreads[i] = CreateThread(NULL, 0, worker, &params[i], 0, NULL);
        if (!hThreads[i]) {
            fprintf(stderr, "Failed to create thread %d (error %lu)\n", i, GetLastError());
            return 1;
        }
    }

    g_startTime = now_us();
    printf("[%10.3f us] main: wakes T1\n", elapsed_us());
    SetEvent(g_hWake[0]);

    WaitForMultipleObjects(NUM_THREADS, hThreads, TRUE, INFINITE);

    double overall = (now_us() - g_startTime) / 1e6;

    printf("\n  >> Thread-1 wall: %.3f s\n", params[0].wallTime);
    printf("  >> Thread-2 wall: %.3f s\n", params[1].wallTime);
    printf("  >> Thread-3 wall: %.3f s\n", params[2].wallTime);
    printf("  >> Overall wall:  %.3f s\n", overall);

    for (int i = 0; i < NUM_THREADS; i++) {
        CloseHandle(hThreads[i]);
        CloseHandle(g_hWake[i]);
    }
    return 0;
}
