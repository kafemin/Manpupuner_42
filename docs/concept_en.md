# Manpupuner_42 — Concept

**Version:** 0.2  
**Date:** 2026-06-21

---

## 🔗 Repository Links

| Repository | Description | Link |
|:---|:---|:---|
| **Manpupuner_42** | Python PoC (Proof of Concept) | [https://github.com/kafemin/Manpupuner_42](https://github.com/kafemin/Manpupuner_42) |
| **manpupuner_kernel** | C/Asm Kernel (under development) | [https://github.com/kafemin/manpupuner_kernel](https://github.com/kafemin/manpupuner_kernel) |

---

## ⚠️ Disclaimer

**This is a Proof of Concept demonstration.**

The project is experimental. It may contain bugs, crashes, or unexpected behavior. Testing was performed only in the QEMU emulator. Running on real hardware is at your own risk. The author is not responsible for any damage, data loss, or hardware failure.

**Current implementation:** ~200 lines of Python code.  
**Planned C kernel:** ~18 KB of binary code.

---

## 1. Introduction: The Problem and the Idea

Modern operating systems are built around a **kernel** — a program that manages hardware and provides applications with **system calls** (an interface for working with files, memory, processes, etc.).

The problem is that different OSes use **different sets of system calls**. A program written for one system cannot run on another without emulation or rewriting the code. This creates barriers for developers, users, and entire ecosystems.

**The core idea of the Manpupuner_42 project:**

> Create a **unified minimal layer** (arbiter) between applications and system calls that understands requests from different ecosystems and processes them through a common internal API.

This is not emulation, not virtualization, and not a second kernel. This is **interface unification** at the lowest level.

---

## 2. Inspiration: The L4 Microkernel Family

**Manpupuner_42** is inspired by the architectural principles of the **L4** microkernel family:

- **L4 Microkernel** — Jochen Liedtke, 1990s
- **seL4** — Trustworthy Systems (UNSW) / seL4 Foundation
- **Codezero** — Bahadir Balban, B-Labs

### Key Ideas Borrowed from L4:

1. **Minimalism** — the kernel should be as small as possible and do only the essentials
2. **Unified IPC mechanism** — all interactions through a single interface
3. **Services in user space** — drivers, file systems, and other components run outside the kernel

### Differences from L4:

| Aspect | L4 Family | Manpupuner_42 |
|:---|:---|:---|
| **Goal** | Security, performance | **Interface unification** |
| **Call count** | 11–40+ | **7** |
| **Execution level** | Privileged | **User space** (demo) |
| **Language** | C, ASM | **Python** (demo) |
| **Scheduler** | In-kernel | **Externalized** |
| **Memory management** | In-kernel (hardware) | **Externalized** (virtual) |

---

## 3. Project Name: Manpupuner_42

The name **Manpupuner_42** is inspired by two symbols:

1. **Manpupuner** — a geological monument in the Northern Urals. Seven giant stone pillars up to 42 meters tall stand as unshakable guardians, symbolizing the fundamental principles on which the new architecture is built.
2. **42** — the universal number referring to the search for the answer to the ultimate question. In our case, it is the search for a universal solution to system compatibility.

> **Symbolism:** Just as the seven pillars of Manpupuner stand on a remote plateau, the seven basic system calls become the foundation of a new architecture — simple, clear, and universal.

---

## 4. System Architecture: Three Levels

The Manpupuner_42 system consists of three logical levels:

### Level 1: External Interfaces (API Layers)

These layers accept requests from applications in the format of specific OSes. Each layer **translates** the external call into the arbiter's internal representation.

- **POSIX Layer:** Understands calls like `open()`, `read()`, `fork()`, `exec()`, `sleep()`.
- **NT Layer:** Understands calls like `CreateFile()`, `ReadFile()`, `CreateProcess()`, `Sleep()`.

These layers are not kernels. They are small translator libraries that convert call syntax and parameters into a unified format.

### Level 2: Unified Arbiter (Core)

This is the heart of the system. The arbiter receives **internal requests** (unified) and executes them through its own minimal set of functions.

The arbiter's internal API contains 7 basic operations:

| # | Internal Call | What it Does |
|:-:|:---|:---|
| 1 | `READ_FILE` | Reads data from the virtual file system |
| 2 | `WRITE_FILE` | Writes data to the virtual file system |
| 3 | `CREATE_PROCESS` | Creates a new process (emulation) |
| 4 | `SLEEP` | Suspends execution for a specified time |
| 5 | `ALLOC_MEMORY` | Allocates a virtual memory block |
| 6 | `FREE_MEMORY` | Frees a memory block |
| 7 | `LIST_FILES` | Returns a list of files in the virtual file system |

The arbiter doesn't know where the request came from — POSIX or NT. It just executes the command.

### Level 3: Executor (Emulation)

At this level, the arbiter interacts with the "hardware." In the current demonstration, the hardware is **emulated**:

- Instead of a real file system — a dictionary in memory.
- Instead of real processes — a counter and a list of names.
- Instead of real time — `time.sleep()`.

This is intentional, to show the **principle** rather than create a production OS.

---

## 5. How It Works: Step by Step

Let's walk through how the system processes a single request:

1. **Application** calls a function (e.g., `open("/home/file.txt")` in POSIX style or `CreateFile("C:\\file.txt")` in NT style).
2. **Compatibility layer** intercepts the call, extracts parameters, and forms an **internal request** to the arbiter: `{ type: READ_FILE, args: { path: "/home/file.txt" } }`.
3. **Arbiter** receives the request, determines its type, and calls the appropriate handler.
4. **Executor** performs the operation (e.g., looks up the file in the virtual FS and returns its contents).
5. **Arbiter** returns the result back to the compatibility layer.
6. **Compatibility layer** converts the result into the format expected by the application (e.g., a file descriptor or HANDLE).
7. **Application** receives the result and continues working.

**Key point:** The arbiter doesn't care where the request came from. The `open()` call from POSIX and `CreateFile()` from NT both map to the same internal call `READ_FILE`. This is **system call unification**.

---

## 6. What the Demonstration Proves

The Python demonstration shows:

1. ✅ **Recognition:** The arbiter understands commands from two different "worlds" (POSIX and NT).
2. ✅ **Uniformity:** Different external calls are reduced to one internal API.
3. ✅ **Functionality:** The system produces the expected result (file contents, process creation, pause).
4. ✅ **Minimalism:** 7 basic calls are enough for operation. Everything else can be built on top of them.

This proves that **the universal arbiter principle works**.

---

## 7. Differences from Existing Approaches

| Approach | Principle | Limitation vs Manpupuner_42 |
|:---|:---|:---|
| **Hybrid Kernel** (Windows NT, XNU) | One kernel, one ecosystem | Cannot run apps from other systems |
| **One-way Translation** (WSL 1) | Translates calls A → B | Works in only one direction |
| **Virtualization** (WSL 2, VirtualBox) | Runs guest OS kernel | Two kernels, high overhead |
| **API Emulation** (Wine) | Emulates API in user space | Works at API level, not kernel |
| **Microkernels** (L4, seL4, Codezero) | Secure kernel for embedded systems | Don't solve OS compatibility |
| **Manpupuner_42** | **Unified arbiter with 7 calls** | ✅ **Interface unification, simplicity, cross-platform** |

---

## 8. Comparison with the L4 Microkernel Family

### Key Differences

| Aspect | L4 (v2) | OKL4 | seL4 | Manpupuner_42 (PoC) |
|:---|:---|:---|:---|:---|
| **Implementation Language** | C, ASM | C, ASM | C, ASM, Isabelle/HOL | **Python** |
| **System Calls** | 11 (7 API + 4 priv.) | 16 (7 API + 9 priv.) | ~40 base (+ macros) | **7 (API only)** |
| **Code Size** | ~12 KB | ~20–30 KB | ~8,700 lines C + 200K lines proofs | **~200 lines Python** |
| **Memory Management** | In-kernel | In-kernel | In-kernel | **Externalized** |
| **Scheduler** | In-kernel | In-kernel | In-kernel | **Externalized** |
| **Execution Level** | Privileged | Privileged | Privileged | **User space** |
| **Target Platform** | x86 | ARM/x86 | ARM/x86/RISC-V | **Any with Python** |
| **Primary Goal** | Minimalism | Mobile devices | Security, verification | **Interface unification** |
| **Capability System** | ❌ | ✅ | ✅ | ❌ |
| **Formal Verification** | ❌ | ❌ | ✅ (Isabelle/HOL) | ❌ |

### Evolution of System Call Count

```text
Mach (microkernel)       → ~140 calls
L4 (J. Liedtke, 1990s)   → 11 calls (7 API + 4 privileged)
OKL4 (commercial)        → 16 calls (7 API + 9 privileged)
seL4 (verified)          → ~40 base calls + macros
Manpupuner_42 (PoC)      → 7 calls (API only)
```

---

## 9. History of Creation

### 🧠 Original Concept (Author: Alexander Kaskov)

The idea for the project came from an observation:

> *"If programs call the kernel through system calls, why not create a unified layer that understands calls from different systems and executes them through a common internal API?"*

The author hypothesized that:

- Two kernels are unnecessary — one arbiter is enough.
- Conflicts between kernels can be avoided by removing the kernels themselves and keeping only the system calls.
- This approach would reduce code size and simplify cross-platform development.

**Two-stage concept validation:**

1. **Python PoC** — concept validated in Python: [https://github.com/kafemin/Manpupuner_42](https://github.com/kafemin/Manpupuner_42)
2. **Kernel Implementation** — in C and assembly (in development): [https://github.com/kafemin/manpupuner_kernel](https://github.com/kafemin/manpupuner_kernel)

### 💻 Technical Implementation

The author approached the **DeepSeek** AI assistant with a request to create a working demonstration. During the conversation, the following were formulated and implemented:

1. Three-level architecture
2. Internal API of 7 basic calls
3. Two compatibility layers (POSIX and NT)
4. Virtual file system in memory
5. Set of test scenarios

---

## 10. Legal Status

Manpupuner_42 is an **original work**:

1. All code was written from scratch in Python
2. The project name is unique
3. Principles are described without reference to specific OSes
4. No seL4 or Codezero code is used or distributed

The project is **demonstration and educational in nature**.

---

## 11. Conclusion

Manpupuner_42 is a **philosophy**: to unite, not divide. To build bridges, not walls.

> *The seven pillars of Manpupuner have stood for centuries. The seven system calls of Manpupuner_42 could become the foundation for a new era.*

---

## 📋 Changelog

| Version | Date | Changes | Source / Justification |
|:---|:---|:---|:---|
| 0.1 | 2026-06-21 | Initial version | — |
| 0.2 | 2026-06-21 | **Added "Inspiration: L4 Family" section** | Clarification of architectural roots |
| 0.2 | 2026-06-21 | **Added "Comparison with L4 Family" section** | Detailed comparison with L4, OKL4, seL4 |
| 0.2 | 2026-06-21 | **Clarified code size** | Separated Python PoC from planned C kernel |
| 0.2 | 2026-06-21 | **Clarified seL4 call count** | ~40 base (+ macros), not ~150 |
| 0.2 | 2026-06-21 | **Added changelog** | Technical documentation standard |

---

## 📚 Data Sources for Comparison

| Data | Source |
|:---|:---|
| L4 v2 call count (11) | J. Liedtke, "L4 Reference Manual", 1996 |
| OKL4 call count (16) | OKL4 Microkernel Specification, Open Kernel Labs |
| seL4 size (~8,700 lines C) | seL4 GitHub repository, kernel/ directory |
| seL4 verification (200K+ lines) | Klein et al., "seL4: Formal Verification of an OS Kernel", SOSP 2009 |
| L4 v2 size (~12 KB) | J. Liedtke, "On Micro-Kernel Construction", SOSP 1995 |
| Codezero size | B. Balban, "Codezero L4 Microkernel", GitHub |
| Manpupuner_42 size (~200 lines) | Current repository analysis |

---

**Idea & Architecture Author:** Alexander Kaskov (Kafemin)  
**Technical Implementation:** With assistance from AI assistant DeepSeek  
**Version:** 0.2  
**Date:** 2026-06-21
