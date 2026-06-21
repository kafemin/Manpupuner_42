#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
NT compatibility layer usage example
Demonstrates WinAPI-style calls

Version: 0.1
Date: 21.06.2026
"""

from hybrid_arbiter_en import HybridArbiter, NtCompatLayer


def main():
    """
    NT layer demonstration
    """
    print("=" * 60)
    print("Example: NT program (WinAPI-style)")
    print("=" * 60)
    print()

    # Create the arbiter kernel
    print("> Creating arbiter kernel...")
    kernel = HybridArbiter()
    
    # Create NT compatibility layer
    print("> Creating NT compatibility layer...")
    nt = NtCompatLayer(kernel)
    print()

    # =============================================================
    # 1. Opening a file (CreateFile)
    # =============================================================
    print(">>> 1. Opening file (CreateFile)")
    print("-" * 40)
    
    handle = nt.CreateFile("C:\\Users\\User\\hello.txt")
    if handle != -1:
        print(f"✅ File opened, HANDLE: {handle}")
    else:
        print("❌ Error opening file")
        return
    print()

    # =============================================================
    # 2. Reading a file (ReadFile)
    # =============================================================
    print(">>> 2. Reading file (ReadFile)")
    print("-" * 40)
    
    content = nt.ReadFile(handle, 50)
    if content:
        print(f"✅ Read: '{content}'")
    else:
        print("❌ Error reading file")
    print()

    # =============================================================
    # 3. Closing a file (CloseHandle)
    # =============================================================
    print(">>> 3. Closing file (CloseHandle)")
    print("-" * 40)
    
    result = nt.CloseHandle(handle)
    if result == 1:
        print("✅ File closed")
    else:
        print("❌ Error closing file")
    print()

    # =============================================================
    # 4. Creating a process (CreateProcess)
    # =============================================================
    print(">>> 4. Creating process (CreateProcess)")
    print("-" * 40)
    
    pid = nt.CreateProcess("notepad.exe")
    if pid != -1:
        print(f"✅ Process created, PID: {pid}")
    else:
        print("❌ Error creating process")
    print()

    # =============================================================
    # 5. Sleep
    # =============================================================
    print(">>> 5. Sleep")
    print("-" * 40)
    
    nt.Sleep(2000)  # 2000 ms = 2 seconds
    print("✅ Sleep completed")
    print()

    print("=" * 60)
    print("Demonstration completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
