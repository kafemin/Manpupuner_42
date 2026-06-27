# ⛰️ Manpupuner_42

**Unified System Interface Demonstration**  
*Демонстрация унификации системных интерфейсов*

[![Version](https://img.shields.io/badge/version-0.1-blue)](https://github.com/kafemin/Manpupuner_42)
[![Python](https://img.shields.io/badge/python-3.6+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

## 🔗 Repository Links

| Repository | Description | Link |
|:---|:---|:---|
| **Manpupuner_42** | Python PoC (Proof of Concept) | [https://github.com/kafemin/Manpupuner_42](https://github.com/kafemin/Manpupuner_42) |
| **manpupuner_kernel** | C/Asm Kernel (under development) | [https://github.com/kafemin/manpupuner_kernel](https://github.com/kafemin/manpupuner_kernel) |

---

## 📖 About the Project

**Manpupuner_42** is a demonstrational Proof of Concept that rethinks the approach to system interfaces. Inspired by the architectural principles of the **L4** microkernel family, it offers a **fundamentally different path**:

- **Instead of dozens of system calls** — just **7 basic ones**
- **Instead of a complex C/Asm kernel** — **clear Python implementation** (for demonstration)
- **Instead of hardware dependency** — **cross-platform compatibility**
- **Instead of a single interface** — **POSIX and NT unification**

### Core Idea

Create a minimal arbiter layer that:
1. **Understands requests** from different ecosystems (POSIX, NT)
2. **Translates them** into a unified internal API of 7 calls
3. **Emulates execution** in a virtual environment

> 🚀 **This is a concept demonstration, not a production kernel.**  
> The main goal is to show how L4 ideas can be rethought to solve system compatibility problems. A C-based kernel implementation is currently under development to validate the concept at a lower level.

---

## ⚠️ Disclaimer

**This is a Proof of Concept demonstration.**

The project is experimental. It may contain bugs, crashes, or unexpected behavior. Testing was performed only in the QEMU emulator. Running on real hardware is at your own risk. The author is not responsible for any damage, data loss, or hardware failure.

**Current implementation:** ~200 lines of Python code.  
**Planned C kernel:** ~18 KB of binary code.

---

## 🏔️ Name: Symbolism and Philosophy

The project is named after the **Manpupuner** plateau in the Northern Urals — a geological monument with seven giant stone pillars.

- **Seven stone pillars** → symbolize the **7 fundamental system calls** that form the architecture of Manpupuner_42.
- **Number 42** → a reference to "The Answer to the Ultimate Question of Life, the Universe, and Everything." In our case, it's the search for a universal answer to system compatibility.

> *The seven pillars of Manpupuner have stood for centuries. The seven system calls of Manpupuner_42 could become the foundation for a new era in software development.*

---

## 📚 Sources of Inspiration

**Manpupuner_42** is inspired by the architectural principles of the L4 microkernel family:

- **L4 Microkernel** — Jochen Liedtke, 1990s
- **seL4** — Trustworthy Systems (UNSW) / seL4 Foundation
- **Codezero** — Bahadir Balban, B-Labs

### References:
- [seL4 Official Website](https://sel4.com/)
- [seL4 on GitHub](https://github.com/seL4)
- [Codezero on GitHub](https://github.com/jserv/codezero)
- [L4Linux Project (TU Dresden)](https://os.inf.tu-dresden.de/L4/LinuxOnL4/)

---

## 🚀 Quick Start

Try the concept locally in 30 seconds:

```bash
# 1. Clone the repository
git clone https://github.com/kafemin/Manpupuner_42.git
cd Manpupuner_42

# 2. Run the demonstration (English)
python3 hybrid_arbiter_en.py

# 3. Or run the demonstration (Russian)
python3 hybrid_arbiter_ru.py
```

---

## 🧱 Architecture: From L4 to Unified Arbiter

The project reinterprets L4 microkernel ideas to solve interface unification.

### Three Architecture Layers

```text
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATIONS                              │
├──────────────────────────┬──────────────────────────────────┤
│  Layer A (POSIX-style)   │  Layer B (NT-style)             │
│  open(), read(), fork()  │  CreateFile(), ReadFile(), ...  │
├──────────────────────────┴──────────────────────────────────┤
│               UNIFIED ARBITER                               │
│         7 basic calls:                                      │
│   READ_FILE, WRITE_FILE, CREATE_PROCESS, SLEEP,            │
│   ALLOC_MEMORY, FREE_MEMORY, LIST_FILES                    │
├─────────────────────────────────────────────────────────────┤
│               EXECUTOR (EMULATION)                          │
│         Virtual FS, memory, processes, time                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔬 Comparison with L4 Microkernel Family

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
seL4 (verified)          → ~40 base calls + capability macros
Manpupuner_42 (PoC)      → 7 calls (API only, no privileged)
```

> **Important note:** In seL4, the number of "real" system calls is smaller than it appears. Many of the ~150 mentioned operations are macros and helper functions for capability management, not separate system calls.

### Architectural Decisions

| Component | L4 Family | Manpupuner_42 |
|:---|:---|:---|
| **Scheduler** | In-kernel, hardware interrupt level | **Fully externalized** (emulated) |
| **Memory Management** | In-kernel, works with MMU | **Virtual**, in user space |
| **IPC** | Complex mechanism with priorities, queues | **None** (replaced by direct calls) |
| **Capability System** | Core security mechanism | **None** (not needed for demo) |
| **Drivers** | In user space (as services) | **Not implemented** (emulated) |

---

## 🔧 Internal API: 7 Pillars of the System

The arbiter's internal API contains just 7 calls that cover all basic program needs:

| # | Call | Description | Example |
|:-:|:---|:---|:---|
| 1 | `READ_FILE` | Read data from virtual FS | `READ_FILE(path="/home/file.txt")` |
| 2 | `WRITE_FILE` | Write data to virtual FS | `WRITE_FILE(path="/home/file.txt", data="Hello")` |
| 3 | `CREATE_PROCESS` | Create new process (emulation) | `CREATE_PROCESS(name="my_app")` |
| 4 | `SLEEP` | Suspend execution | `SLEEP(seconds=2)` |
| 5 | `ALLOC_MEMORY` | Allocate virtual memory block | `ALLOC_MEMORY(size=1024)` |
| 6 | `FREE_MEMORY` | Free memory block | `FREE_MEMORY(id=0)` |
| 7 | `LIST_FILES` | List files in virtual FS | `LIST_FILES()` |

---

## 💻 Usage Example

This example shows how two different interfaces (POSIX and NT) map to the same internal action.

```python
from hybrid_arbiter_en import HybridArbiter, PosixCompatLayer, NtCompatLayer

# 1. Create the arbiter core
kernel = HybridArbiter()

# 2. Create two compatibility layers
posix = PosixCompatLayer(kernel)
nt = NtCompatLayer(kernel)

# 3. POSIX-style program (Linux-like)
fd = posix.open("/home/user/hello.txt")
content = posix.read(fd, 50)
posix.close(fd)

# 4. NT-style program (Windows-like)
handle = nt.CreateFile("C:\\Users\\User\\hello.txt")
content = nt.ReadFile(handle, 50)
nt.CloseHandle(handle)
```

**The magic?** Both calls (`open()` and `CreateFile()`) translate to the same internal call `READ_FILE`. The arbiter doesn't know where the request came from — it just executes the command.

---

## 📊 Comparison with Existing Approaches

| Approach | Principle | Limitation vs Manpupuner_42 |
|:---|:---|:---|
| **Hybrid Kernel** (Windows NT, XNU) | One kernel, one ecosystem | Cannot run apps from other systems |
| **One-way Translation** (WSL 1) | Translates calls A → B | Works in only one direction |
| **Virtualization** (WSL 2, VirtualBox) | Runs full guest OS kernel | Two kernels, high overhead |
| **API Emulation** (Wine) | Emulates API in user space | Works at API level, not kernel |
| **Microkernels** (L4, seL4) | Secure kernel for embedded | Don't solve OS compatibility |
| **Manpupuner_42** | **Unified arbiter with 7 calls** | ✅ **Interface unification, simplicity** |

---

## 📁 Project Structure

```text
Manpupuner_42/
├── README_en.md           # Main description (English)
├── README_ru.md           # Main description (Russian)
├── LICENSE                # MIT License
├── .gitignore             # Ignored files
├── hybrid_arbiter_en.py   # Main code (English comments)
├── hybrid_arbiter_ru.py   # Main code (Russian comments)
├── docs/
│   ├── concept_en.md      # Full concept (English)
│   └── concept_ru.md      # Full concept (Russian)
├── examples/
│   ├── example_posix_en.py
│   ├── example_posix_ru.py
│   ├── example_nt_en.py
│   └── example_nt_ru.py
└── tests/
    ├── __init__.py
    └── test_arbiter.py
```

---

## 🧪 Testing

```bash
python3 -m unittest discover tests
```

---

## 🤝 How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **MIT** License.

---

## 👤 Authors

| Role | Name |
|:---|:---|
| **Idea & Architecture** | [Alexander Kaskov (Kafemin)](https://github.com/kafemin) |
| **Technical Implementation** | With assistance from AI assistant [DeepSeek](https://deepseek.com) |

---

## 🙏 Acknowledgements

- **Inspiration** — The Seven Pillars of Manpupuner
- **Architectural Ideas** — L4 Microkernel (Jochen Liedtke), seL4, Codezero
- **Technical Support** — AI assistant DeepSeek

---

**Version:** 0.1  
**Date:** 2026-06-21

---

> *"People must see the principle, and then... everything will take its course."*
