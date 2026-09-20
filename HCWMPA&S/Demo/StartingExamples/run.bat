mingw32-make SRC=try.cpp EXTRA_CXXFLAGS="-DM=16777216 -DN=1" -B
try.exe
try.exe s
pause
mingw32-make SRC=try.cpp EXTRA_CXXFLAGS="-DM=4096 -DN=4096" -B
try.exe
try.exe s