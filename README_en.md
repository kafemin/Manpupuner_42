# ⛰️ Manpupuner_42

**Hybrid System Call Arbiter**  
*Гибридный арбитр системных вызовов*

[![Version](https://img.shields.io/badge/version-0.1-blue)](https://github.com/kafemin/Manpupuner_42)
[![Python](https://img.shields.io/badge/python-3.6+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

## 🔗 Repository Links

| Repository | Description | Link |
|:---|:---|:---|
| **Manpupuner_42** | Python PoC (concept) | [https://github.com/kafemin/Manpupuner_42](https://github.com/kafemin/Manpupuner_42) |
| **manpupuner_kernel** | Kernel in C/Asm (implementation) | [https://github.com/kafemin/manpupuner_kernel](https://github.com/kafemin/manpupuner_kernel) |

---

## 📖 About

**Manpupuner_42** is a Proof of Concept that challenges established approaches in operating system development. Instead of emulation or virtualization, the project proposes **interface unification** at the lowest level — the level of system calls.

**The core idea:**  
Create a minimal abstraction layer (arbiter) between hardware and applications. This arbiter understands requests from different ecosystems (e.g., POSIX and NT) and processes them through a **unified internal API of 7 basic calls**.

> 🚀 **This is not emulation, not virtualization, and not a second kernel.**  
> This is — **a single kernel with two interfaces**, providing bidirectional compatibility.

---

## ⚠️ Disclaimer

**This is a Proof of Concept (demonstration).**

This project is experimental. It may contain bugs, errors, or unexpected behavior. Testing has been conducted **only** in the QEMU emulator. Running on real hardware is at your own risk. The author assumes no responsibility for any damage, data loss, or hardware failure.

**Kernel size: ~14 KB (less than 20 KB).**

---

## 🏔️ Name: Symbolism and Philosophy

The project is named after the **Manpupuner** plateau in the Northern Urals — a geological monument with seven giant stone pillars.

- **Seven stone pillars** → symbolize the **7 fundamental system calls** on which the Manpupuner_42 architecture is built.
- **Number 42** → a reference to the "Answer to the Ultimate Question of Life, the Universe, and Everything." In our case, it is the search for a universal answer to the problem of system compatibility.

> *The seven pillars of Manpupuner stand for centuries. The seven system calls of Manpupuner_42 could become the foundation for a new era in software development.*

---

## 🚀 Quick Start

Try the project locally in 30 seconds:

```bash
# 1. Clone the repository
git clone https://github.com/kafemin/Manpupuner_42.git
cd Manpupuner_42

# 2. Run the demo (English)
python3 hybrid_arbiter_en.py

# 3. Or run the demo (Russian)
python3 hybrid_arbiter_ru.py
```

---

## 🧱 Architecture: Three Levels of Unification

The system builds a "bridge" between two different worlds through three logical levels:

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

## 🔧 Internal API: The 7 Pillars of the System

The arbiter's internal API is the "heart" of the project. It contains only 7 calls that cover all the basic needs of any program:

| # | Call | Description | Usage Example |
|:-:|:---|:---|:---|
| 1 | `READ_FILE` | Read data from virtual FS | `READ_FILE(path="/home/file.txt")` |
| 2 | `WRITE_FILE` | Write data to virtual FS | `WRITE_FILE(path="/home/file.txt", data="Hello")` |
| 3 | `CREATE_PROCESS` | Create a new process (emulation) | `CREATE_PROCESS(name="my_app")` |
| 4 | `SLEEP` | Suspend execution | `SLEEP(seconds=2)` |
| 5 | `ALLOC_MEMORY` | Allocate a virtual memory block | `ALLOC_MEMORY(size=1024)` |
| 6 | `FREE_MEMORY` | Free a memory block | `FREE_MEMORY(id=0)` |
| 7 | `LIST_FILES` | List files in virtual FS | `LIST_FILES()` |

---

## 💻 Usage Example: How It Works

This example shows how two different interfaces (POSIX and NT) are reduced to the same internal action.

```python
from hybrid_arbiter_en import HybridArbiter, PosixCompatLayer, NtCompatLayer

# 1. Create the kernel-arbiter
kernel = HybridArbiter()

# 2. Create two compatibility layers
posix = PosixCompatLayer(kernel)
nt = NtCompatLayer(kernel)

# 3. POSIX program (Linux-style)
fd = posix.open("/home/user/hello.txt")  # Returns a file descriptor
content = posix.read(fd, 50)             # Reads the file
posix.close(fd)                          # Closes the file

# 4. NT program (Windows-style)
handle = nt.CreateFile("C:\\Users\\User\\hello.txt")  # Returns a HANDLE
content = nt.ReadFile(handle, 50)                    # Reads the file
nt.CloseHandle(handle)                               # Closes the file
```

**The magic?** Inside the arbiter, both calls (`open()` and `CreateFile()`) are translated into the same internal call `READ_FILE`. The arbiter doesn't know where the request came from — it simply executes the command.

---

## 📊 Comparison with Existing Approaches

| Approach | Principle | Drawback / Difference from Manpupuner_42 |
|:---|:---|:---|
| **Hybrid kernel** (Windows NT, macOS XNU) | One kernel, one ecosystem | Cannot run applications from other systems |
| **One-way translation** (WSL 1) | Translates calls A → B | Works in only one direction |
| **Virtualization** (WSL 2, VirtualBox) | Runs a full guest OS kernel | Two kernels, high overhead |
| **API emulation** (Wine) | Emulates API in user mode | Works at API level, not kernel |
| **Manpupuner_42** | **One kernel — two interfaces** | ✅ **Two-way compatibility at kernel level** |

---

## 📁 Project Structure

The project is organized for easy navigation:

```text
Manpupuner_42/
├── README_ru.md           # Main description (Russian)
├── README_en.md           # Main description (English)
├── LICENSE                # MIT License
├── .gitignore             # Ignored files
├── hybrid_arbiter_ru.py   # Main code (Russian comments)
├── hybrid_arbiter_en.py   # Main code (English comments)
├── docs/
│   ├── concept_ru.md      # Full project concept (Russian)
│   └── concept_en.md      # Full project concept (English)
├── examples/
│   ├── example_posix_ru.py    # POSIX layer example (Russian)
│   ├── example_posix_en.py    # POSIX layer example (English)
│   ├── example_nt_ru.py       # NT layer example (Russian)
│   └── example_nt_en.py       # NT layer example (English)
└── tests/
    ├── __init__.py         # Makes the folder a Python module
    └── test_arbiter.py     # Unit tests
```

---

## 🧪 Testing

```bash
# Run all unit tests
python3 -m unittest discover tests
```

---

## 🤝 How to Contribute

The project is at the Proof of Concept stage. We welcome any ideas, suggestions, and pull requests!

1.  Fork the repository (`Fork`)
2.  Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📜 License

This project is distributed under the **MIT License** — a permissive license that allows using the code for any purpose. See the [LICENSE](LICENSE) file for details.

---

## 👤 Authors

| Role | Name |
|:---|:---|
| **Idea & Architecture Author** | [Kaskov Aleksandr (Kafemin)](https://github.com/kafemin) |
| **Technical Implementation** | With [DeepSeek](https://deepseek.com) AI assistant participation |

---

## 🙏 Acknowledgments

- **Inspiration** — The seven pillars of Manpupuner
- **Technical support** — DeepSeek AI assistant
- **Community** — Everyone who believes in uniting, not dividing

---

**Version:** 0.1  
**Date:** 21.06.2026

---

> *"People need to see the principle, and then... everything will take its course."*
