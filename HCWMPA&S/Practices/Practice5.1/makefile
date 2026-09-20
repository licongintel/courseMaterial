# ============================================================
#  LLVM + MinGW64 Makefile — Windows CMD compatible
#  Usage: mingw32-make SRC=myfile.cpp [OPTIONS...]
# ============================================================

# --- Toolchain ---
CXX       = clang++

# --- Target / Source ---
SRC       ?= single.cpp
TARGET    ?= run-$(basename $(SRC)).exe

# --- Standard ---
STD       ?= c++17

# --- Optimization ---
# Options: -O0 (debug), -O1, -O2, -O3, -Os (size)
OPT       ?= -O2 --target=x86_64-w64-mingw32

# --- Include / Library paths ---
INCLUDES  ?=
LIBS      ?= -L/LLVM/lib

# --- Extra user flags ---
EXTRA_CXXFLAGS ?=
EXTRA_LDFLAGS  ?=

# --- Debug symbols ---
# Set DEBUG=1 to include debug info
NATIVE     ?= 0

# --- Assemble flags ---
ifeq ($(NATIVE), 1)
NATIVE_FLAGS = -march=native
else
NATIVE_FLAGS =
endif

CXXFLAGS  = -std=$(STD) $(OPT) $(NATIVE_FLAGS) \
            $(INCLUDES) $(EXTRA_CXXFLAGS)

LDFLAGS   = $(LIBS) $(EXTRA_LDFLAGS)

# ============================================================
#  Targets
# ============================================================

.PHONY: all clean run info

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDFLAGS)
	@echo [OK] Built: $@

clean:
	@if exist $(TARGET) del /Q $(TARGET)
	@echo [OK] Cleaned.

run: all
	@echo [>>] Running $(TARGET)
	$(TARGET)

info:
	@echo SRC       = $(SRC)
	@echo TARGET    = $(TARGET)
	@echo STD       = $(STD)
	@echo OPT       = $(OPT)
	@echo DEBUG     = $(DEBUG)
	@echo CXXFLAGS  = $(CXXFLAGS)
	@echo LDFLAGS   = $(LDFLAGS)
