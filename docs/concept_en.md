# Manpupuner_42 — Concept

**Version:** 0.1  
**Date:** 21.06.2026

---

## 🔗 Repository Links

| Repository | Description | Link |
|:---|:---|:---|
| **Manpupuner_42** | Python PoC (concept) | [https://github.com/kafemin/Manpupuner_42](https://github.com/kafemin/Manpupuner_42) |
| **manpupuner_kernel** | Kernel in C/Asm (implementation) | [https://github.com/kafemin/manpupuner_kernel](https://github.com/kafemin/manpupuner_kernel) |

---

## ⚠️ Disclaimer

**This is a Proof of Concept (demonstration).**

This project is experimental. It may contain bugs, errors, or unexpected behavior. Testing has been conducted **only** in the QEMU emulator. Running on real hardware is at your own risk. The author assumes no responsibility for any damage, data loss, or hardware failure.

**Kernel size: ~14 KB (less than 20 KB).**

---

## 1. Introduction: The Problem and The Idea

Modern operating systems are built around a **kernel** — a program that manages hardware and provides applications with **system calls** (an interface for working with files, memory, processes, etc.).

The problem is that different OSs use **different sets of system calls**. A program written for one system cannot run on another without emulation or rewriting the code. This creates barriers for developers, users, and entire ecosystems.

**The core idea of the Manpupuner_42 project:**

> Create a **single minimal abstraction layer** (arbiter) between hardware and system calls that understands requests from different ecosystems and processes them through a common internal API.

This is not emulation, not virtualization, and not a second kernel. This is **interface unification** at the lowest level.

---

## 2. Project Name: Manpupuner_42

The name **Manpupuner_42** is inspired by two symbols:

1. **Manpupuner** — a geological monument in the Northern Urals. Seven stone pillars-giants up to 42 meters high stand as unshakable guardians, symbolizing the fundamental principles on which the new architecture is built.
2. **42** — a universal number, referencing the search for the answer to the ultimate question. In our case, it is the search for a universal solution for system compatibility.

> **Symbolism:** Just as the seven pillars of Manpupuner stand on a remote plateau, the seven basic system calls become the foundation of a new architecture — simple, clear, and universal.

---

## 3. System Architecture: Three Levels

The Manpupuner_42 system consists of three logical levels:

### Level 1: External Interfaces (API Layers)

These layers accept requests from applications in the format of specific OSs. Each layer **translates** the external call into the arbiter's internal representation.

- **POSIX Layer:** Understands calls like `open()`, `read()`, `fork()`, `exec()`, `sleep()`.
- **NT Layer:** Understands calls like `CreateFile()`, `ReadFile()`, `CreateProcess()`, `Sleep()`.

These layers are not kernels. They are small translator libraries that convert the syntax and parameters of calls into a unified format.

### Level 2: Unified Arbiter (The Kernel)

This is the heart of the system. The arbiter receives **internal requests** (unified) and executes them through its own minimal set of functions.

The arbiter's internal API contains 7 basic operations:

| # | Internal Call | Description |
|:-:|:---|:---|
| 1 | `READ_FILE` | Reads data from the virtual file system |
| 2 | `WRITE_FILE` | Writes data to the virtual file system |
| 3 | `CREATE_PROCESS` | Creates a new process (emulation) |
| 4 | `SLEEP` | Suspends execution for a specified time |
| 5 | `ALLOC_MEMORY` | Allocates a block of virtual memory |
| 6 | `FREE_MEMORY` | Frees a memory block |
| 7 | `LIST_FILES` | Returns the list of files in the virtual file system |

The arbiter does not know where the request came from — from POSIX or NT. It simply executes the command.

### Level 3: Executor (Hardware Emulation)

At this level, the arbiter interacts with the "hardware". In the current demonstration, the hardware is **emulated**:

- Instead of a real file system — an in-memory dictionary.
- Instead of real processes — a counter and a list of names.
- Instead of real time — `time.sleep()`.

This is done intentionally to demonstrate the **principle** rather than create a complete OS.

---

## 4. How It Works: Step by Step

Let's look at how the system processes a single request:

1. **Application** calls a function (e.g., `open("/home/file.txt")` in POSIX style or `CreateFile("C:\\file.txt")` in NT style).
2. **Compatibility layer** intercepts the call, extracts parameters, and forms an **internal request** to the arbiter: `{ type: READ_FILE, args: { path: "/home/file.txt" } }`.
3. **Arbiter** receives the request, determines its type, and calls the appropriate handler.
4. **Executor** performs the operation (e.g., looks up the file in the virtual FS and returns the content).
5. **Arbiter** returns the result back to the compatibility layer.
6. **Compatibility layer** converts the result into the format expected by the application (e.g., file descriptor or HANDLE).
7. **Application** receives the result and continues.

**Key point:** The arbiter does not care where the request came from. `open()` from POSIX and `CreateFile()` from NT are both reduced to one internal call: `READ_FILE`. This is **the unity of system calls**.

---

## 5. What the Demonstration Proves

The Python demonstration shows:

1. ✅ **Recognition:** The arbiter understands commands from two different "worlds" (POSIX and NT).
2. ✅ **Uniformity:** Different external calls are reduced to a single internal API.
3. ✅ **Functionality:** The system produces the expected result (file content, process creation, pause).
4. ✅ **Minimalism:** Only 7 basic calls are needed for operation. Everything else can be built on top of them.

This proves that the **principle of a universal arbiter works**.

---

## 6. Comparison with Existing Approaches

| Approach | Principle | Difference from Manpupuner_42 |
|:---|:---|:---|
| **Hybrid kernel** | One kernel, one ecosystem | Cannot run applications from other systems |
| **One-way translation** | A → B (only one direction) | Only one direction |
| **Virtualization** | Two kernels, hypervisor | Requires virtualization |
| **API emulation** | User mode | Works at API level, not kernel |
| **Guest kernel** | Two kernels, one is a "guest" | No unified arbiter |
| **Manpupuner_42** | **Single kernel-arbiter** with two translation layers | **Two-way compatibility at kernel level** |

---

## 7. Creation History

### 🧠 Original Concept (author: Kaskov Aleksandr)

The project idea was born from an observation:

> *"If programs access the kernel through system calls, why not create a single layer that understands calls from different systems and executes them through a common internal API?"*

The author suggested that:

- Two kernels are not needed — one arbiter is enough.
- Conflicts between kernels can be bypassed by removing the kernels themselves and keeping only system calls.
- This approach would reduce code volume and simplify cross-platform development.

**Two-stage validation:**

1. **Python PoC** — concept validated in Python: [https://github.com/kafemin/Manpupuner_42](https://github.com/kafemin/Manpupuner_42)
2. **Kernel implementation** — C and Assembly: [https://github.com/kafemin/manpupuner_kernel](https://github.com/kafemin/manpupuner_kernel)

### 💻 Technical Implementation

The author approached the **DeepSeek** AI assistant with a request to create a working demonstration. During the dialogue, the following were formulated and implemented:

1. Three-level architecture
2. Internal API of 7 basic calls
3. Two compatibility layers (POSIX and NT)
4. Virtual file system in memory
5. Set of test scenarios

---

## 8. Legal Purity

The Manpupuner_42 project is an **original development**:

1. All code is written from scratch in Python
2. The project name is unique
3. Principles are described without reference to specific OSs
4. The "clean room" method is used

The project is **demonstration and educational in nature**.

---

## 9. Conclusion

Manpupuner_42 is a **philosophy**: unite, not divide. Build bridges, not walls.

> *The seven pillars of Manpupuner stand for centuries. The seven system calls of Manpupuner_42 could become the foundation for a new era.*

---

**Idea and architecture author:** Kaskov Aleksandr (Kafemin)  
**Technical implementation:** with DeepSeek AI assistant participation  
**Version:** 0.1  
**Date:** 21.06.2026
