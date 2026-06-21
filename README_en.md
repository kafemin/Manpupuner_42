# Manpupuner_42

**Hybrid System Call Arbiter**  
*Гибридный арбитр системных вызовов*

[![Version](https://img.shields.io/badge/version-0.1-blue)](https://github.com/Kafemin/Manpupuner_42)
[![Python](https://img.shields.io/badge/python-3.6+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

---

## 📖 About

**Manpupuner_42** is a Proof of Concept (PoC) of a unified system call arbiter.

**Core idea:**  
Create a minimal abstraction layer between hardware and system calls that understands requests from different ecosystems (POSIX and NT) and processes them through a common internal API of 7 basic calls.

> **This is not emulation, not virtualization, and not a second kernel.**  
> This is **interface unification** at the lowest level.

---

## 🏔️ Name

The project is named after **Manpupuner** — a geological monument in the Northern Urals.

- **Seven stone pillars-giants** → symbolize **7 basic system calls**
- **Number 42** → universal answer, search for a universal solution

> *The seven pillars of Manpupuner stand for centuries.*  
> *The seven system calls of Manpupuner_42 could become the foundation for a new era.*

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Kafemin/Manpupuner_42.git
cd Manpupuner_42

# Run the demo
python3 hybrid_arbiter_en.py

🧱 Architecture

The system consists of three levels:
text

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

🔧 7 Basic Calls
#	Call	Description
1	READ_FILE	Read data from virtual FS
2	WRITE_FILE	Write data to virtual FS
3	CREATE_PROCESS	Create a new process (emulation)
4	SLEEP	Suspend execution
5	ALLOC_MEMORY	Allocate virtual memory block
6	FREE_MEMORY	Free memory block
7	LIST_FILES	List files in virtual FS
💻 Usage Example
python

from hybrid_arbiter import HybridArbiter, LinuxCompatLayer, WindowsCompatLayer

# Create the arbiter kernel
kernel = HybridArbiter()

# Linux-style (POSIX)
linux = LinuxCompatLayer(kernel)
fd = linux.open("/home/user/hello.txt")
content = linux.read(fd, 50)
linux.close(fd)

# Windows-style (WinAPI)
windows = WindowsCompatLayer(kernel)
handle = windows.CreateFile("C:\\Users\\User\\hello.txt")
content = windows.ReadFile(handle, 50)
windows.CloseHandle(handle)

📊 Comparison with Alternatives
Approach	Principle	Difference from Manpupuner_42
Hybrid kernel	One kernel, one ecosystem	Cannot run apps from other systems
One-way translation	A → B (only one direction)	Only one direction
Virtualization	Two kernels, hypervisor	Requires virtualization
API emulation	User mode	Works at API level, not kernel
Manpupuner_42	One kernel — two interfaces	Two-way compatibility at kernel level
📁 Project Structure
text

Manpupuner_42/
├── README_ru.md              # Main description (Russian)
├── README_en.md           # Main description (English)
├── LICENSE                # MIT License
├── .gitignore             # Ignored files
├── hybrid_arbiter_ru.py   # Main code (Russian comments)
├── hybrid_arbiter_en.py   # Main code (English comments)
├── docs/
│   ├── concept_ru.md      # Concept (Russian)
│   └── concept_en.md      # Concept (English)
└── examples/
    ├── example_linux_ru.py   # Linux layer example (Russian)
    ├── example_linux_en.py# Linux layer example (English)
    ├── example_windows_ru.py # Windows layer example (Russian)
    └── example_windows_en.py # Windows layer example (English)

🧪 Testing
bash

python3 -m unittest discover tests

📜 License

This project is distributed under the MIT License. See the LICENSE file for details.
👤 Authors
Role	Name
Idea and Architecture Author	Kafemin
Technical Implementation	With DeepSeek AI assistant participation
🙏 Acknowledgments

    Inspiration — the seven pillars of Manpupuner

    Technical support — DeepSeek AI assistant

    Everyone who believes in uniting, not dividing

Version: 0.1
Date: 21.06.2026

    "People need to see the principle, and then... everything will take its course."
