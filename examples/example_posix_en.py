#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
POSIX compatibility layer usage example
Demonstrates POSIX-style calls

Version: 0.1
Date: 21.06.2026
"""

from hybrid_arbiter_en import HybridArbiter, PosixCompatLayer


def main():
    """
    POSIX layer demonstration
    """
    print("=" * 60)
    print("Example: POSIX program")
    print("=" * 60)
    print()

    # Create the arbiter kernel
    print("> Creating arbiter kernel...")
    kernel = HybridArbiter()
    
    # Create POSIX compatibility layer
    print("> Creating POSIX compatibility layer...")
    posix = PosixCompatLayer(kernel)
    print()

    # =============================================================
    # 1. Opening a file
    # =============================================================
    print(">>> 1. Opening file")
    print("-" * 40)
    
    fd = posix.open("/home/user/hello.txt")
    if fd != -1:
        print(f"✅ File opened, descriptor: {fd}")
    else:
        print("❌ Error opening file")
        return
    print()

    # =============================================================
    # 2. Reading a file
    # =============================================================
    print(">>> 2. Reading file")
    print("-" * 40)
    
    content = posix.read(fd, 50)
    if content:
        print(f"✅ Read: '{content}'")
    else:
        print("❌ Error reading file")
    print()

    # =============================================================
    # 3. Closing a file
    # =============================================================
    print(">>> 3. Closing file")
    print("-" * 40)
    
    result = posix.close(fd)
    if result == 0:
        print("✅ File closed")
    else:
        print("❌ Error closing file")
    print()

    # =============================================================
    # 4. Creating a process (fork)
    # =============================================================
    print(">>> 4. Creating process (fork)")
    print("-" * 40)
    
    pid = posix.fork()
    if pid != -1:
        print(f"✅ Process created, PID: {pid}")
    else:
        print("❌ Error creating process")
    print()

    # =============================================================
    # 5. Executing a program (execve)
    # =============================================================
    print(">>> 5. Executing program (execve)")
    print("-" * 40)
    
    pid2 = posix.execve("/bin/ls", ["ls", "-l"])
    if pid2 != -1:
        print(f"✅ Program executed, PID: {pid2}")
    else:
        print("❌ Error executing program")
    print()

    # =============================================================
    # 6. Sleep
    # =============================================================
    print(">>> 6. Sleep")
    print("-" * 40)
    
    result = posix.sleep(2)
    if result == 0:
        print("✅ Sleep completed")
    else:
        print("❌ Error during sleep")
    print()

    print("=" * 60)
    print("Demonstration completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
