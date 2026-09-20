CXX = g++
CXXFLAGS = -O2 -Wall
LDFLAGS =

all: thread_switch_demo.exe three_thread_demo.exe

thread_switch_demo.exe: thread_switch_demo.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

three_thread_demo.exe: three_thread_demo.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	del /Q thread_switch_demo.exe three_thread_demo.exe

.PHONY: all clean
