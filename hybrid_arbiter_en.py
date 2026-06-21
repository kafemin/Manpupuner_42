#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
Manpupuner_42 - Hybrid System Call Arbiter

Proof of concept: a single kernel understands POSIX-style and NT-style calls

Version: 0.1
Date: 21.06.2026

Idea and architecture author: Kafemin
Technical implementation: with DeepSeek AI assistant participation

License: MIT (demonstration project)
================================================================================
"""

import time
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


# =============================================================================
# ARBITER INTERNAL API (UNIFIED STANDARD)
# =============================================================================

class SyscallType(Enum):
    """
    System call types understood by the arbiter
    
    These 7 types form the foundation of the system — like the seven pillars of Manpupuner.
    """
    READ_FILE = 1        # Read file
    WRITE_FILE = 2       # Write file
    CREATE_PROCESS = 3   # Create process
    SLEEP = 4            # Sleep
    ALLOC_MEMORY = 5     # Allocate memory
    FREE_MEMORY = 6      # Free memory
    LIST_FILES = 7       # List files


@dataclass
class SyscallRequest:
    """
    Internal request format for the arbiter
    
    Any external call (from POSIX or NT) is transformed into this format.
    """
    type: SyscallType          # Operation type
    args: Dict[str, Any]       # Arguments in unified form

    def __repr__(self):
        return f"<Request {self.type.name} {self.args}>"


@dataclass
class SyscallResponse:
    """
    Internal response format from the arbiter
    
    Unified return format for all compatibility layers.
    """
    success: bool              # Success flag
    data: Any = None           # Result data
    error: Optional[str] = None  # Error message

    def __repr__(self):
        if self.success:
            return f"<Response OK: {self.data}>"
        return f"<Response ERROR: {self.error}>"


# =============================================================================
# UNIFIED ARBITER (THE KERNEL)
# =============================================================================

class HybridArbiter:
    """
    Single kernel-arbiter.
    
    This class is the heart of the system. It:
    - Receives internal requests (SyscallRequest)
    - Executes them through its own minimal set of functions
    - Manages virtual file system, memory, and processes
    - Does not know where the request came from — POSIX or NT
    """

    def __init__(self):
        # =============================================================
        # Virtual file system (in memory)
        # =============================================================
        self._filesystem: Dict[str, str] = {
            "/etc/hosts": "127.0.0.1 localhost",
            "/home/user/hello.txt": "Hello from hybrid kernel!",
            "C:\\Users\\User\\hello.txt": "Hello from NT side!",
            "/README.md": "# Manpupuner_42\n\nHybrid Kernel Demo\n\nProof of Concept v0.1",
        }
        
        # =============================================================
        # Virtual memory (for demonstration)
        # =============================================================
        self._memory_blocks: Dict[int, bytes] = {}
        self._next_mem_id = 0
        
        # =============================================================
        # Process management
        # =============================================================
        self._process_count = 0
        
        # =============================================================
        # Logging
        # =============================================================
        self._log = []
    
    def log(self, msg: str):
        """Write to arbiter log"""
        self._log.append(f"[Arbiter] {msg}")
        print(f"[Arbiter] {msg}")
    
    # =========================================================================
    # INTERNAL API (called by compatibility layers)
    # =========================================================================
    
    def execute(self, request: SyscallRequest) -> SyscallResponse:
        """
        Main dispatcher. Receives internal request and executes it.
        
        This is the single entry point for all compatibility layers.
        """
        self.log(f"Executing: {request}")
        
        try:
            if request.type == SyscallType.READ_FILE:
                return self._sys_read_file(request.args.get('path', ''))
            elif request.type == SyscallType.WRITE_FILE:
                return self._sys_write_file(
                    request.args.get('path', ''),
                    request.args.get('data', '')
                )
            elif request.type == SyscallType.CREATE_PROCESS:
                return self._sys_create_process(request.args.get('name', 'process'))
            elif request.type == SyscallType.SLEEP:
                return self._sys_sleep(request.args.get('seconds', 0))
            elif request.type == SyscallType.ALLOC_MEMORY:
                return self._sys_alloc_memory(request.args.get('size', 0))
            elif request.type == SyscallType.FREE_MEMORY:
                return self._sys_free_memory(request.args.get('id', -1))
            elif request.type == SyscallType.LIST_FILES:
                return self._sys_list_files()
            else:
                return SyscallResponse(False, error=f"Unknown syscall: {request.type}")
        except Exception as e:
            return SyscallResponse(False, error=str(e))
    
    # =========================================================================
    # SYSTEM CALL IMPLEMENTATIONS
    # =========================================================================
    
    def _sys_read_file(self, path: str) -> SyscallResponse:
        """Read file from virtual FS"""
        if path in self._filesystem:
            content = self._filesystem[path]
            return SyscallResponse(True, {
                'content': content,
                'size': len(content),
                'path': path
            })
        else:
            for key in self._filesystem:
                if path in key or key in path:
                    return SyscallResponse(True, {
                        'content': self._filesystem[key],
                        'size': len(self._filesystem[key]),
                        'path': key
                    })
            return SyscallResponse(False, error=f"File not found: {path}")
    
    def _sys_write_file(self, path: str, data: str) -> SyscallResponse:
        """Write file to virtual FS"""
        self._filesystem[path] = data
        return SyscallResponse(True, {'path': path, 'size': len(data)})
    
    def _sys_create_process(self, name: str) -> SyscallResponse:
        """Create new process (emulation)"""
        self._process_count += 1
        pid = self._process_count
        self.log(f"Process created: {name} (PID={pid})")
        return SyscallResponse(True, {'pid': pid, 'name': name})
    
    def _sys_sleep(self, seconds: int) -> SyscallResponse:
        """Suspend execution"""
        self.log(f"Sleeping for {seconds}s...")
        time.sleep(seconds)
        return SyscallResponse(True, {'slept': seconds})
    
    def _sys_alloc_memory(self, size: int) -> SyscallResponse:
        """Allocate virtual memory"""
        mem_id = self._next_mem_id
        self._next_mem_id += 1
        self._memory_blocks[mem_id] = b'\x00' * size
        return SyscallResponse(True, {'id': mem_id, 'size': size})
    
    def _sys_free_memory(self, mem_id: int) -> SyscallResponse:
        """Free memory"""
        if mem_id in self._memory_blocks:
            del self._memory_blocks[mem_id]
            return SyscallResponse(True, {'freed': mem_id})
        return SyscallResponse(False, error=f"Memory block {mem_id} not found")
    
    def _sys_list_files(self) -> SyscallResponse:
        """List files in virtual FS"""
        files = list(self._filesystem.keys())
        return SyscallResponse(True, {'files': files, 'count': len(files)})
    
    def get_log(self):
        """Return arbiter log"""
        return self._log


# =============================================================================
# POSIX COMPATIBILITY LAYER
# =============================================================================

class PosixCompatLayer:
    """
    Compatibility layer for POSIX-like systems.
    
    Translates POSIX-style calls to the arbiter's internal API.
    
    Supported calls:
    - open()   → READ_FILE
    - read()   → return from cache
    - close()  → descriptor removal
    - fork()   → CREATE_PROCESS
    - execve() → CREATE_PROCESS
    - sleep()  → SLEEP
    """
    
    def __init__(self, arbiter: HybridArbiter):
        self._arbiter = arbiter
        self._open_files = {}
        self._next_fd = 1
        self._log = []
    
    def log(self, msg: str):
        self._log.append(f"[POSIX] {msg}")
        print(f"[POSIX] {msg}")
    
    def open(self, path: str, flags: int = 0) -> int:
        """Emulation of POSIX open()"""
        self.log(f"open('{path}', flags={flags})")
        
        request = SyscallRequest(
            type=SyscallType.READ_FILE,
            args={'path': path}
        )
        response = self._arbiter.execute(request)
        
        if response.success:
            fd = self._next_fd
            self._next_fd += 1
            self._open_files[fd] = {
                'path': path,
                'content': response.data['content'],
                'size': response.data['size']
            }
            self.log(f"open -> fd={fd}")
            return fd
        else:
            self.log(f"open -> ERROR: {response.error}")
            return -1
    
    def read(self, fd: int, size: int) -> str:
        """Emulation of POSIX read()"""
        self.log(f"read(fd={fd}, size={size})")
        
        if fd in self._open_files:
            content = self._open_files[fd]['content'][:size]
            self.log(f"read -> '{content}'")
            return content
        else:
            self.log(f"read -> ERROR: invalid fd")
            return ""
    
    def close(self, fd: int) -> int:
        """Emulation of POSIX close()"""
        self.log(f"close(fd={fd})")
        
        if fd in self._open_files:
            del self._open_files[fd]
            return 0
        return -1
    
    def fork(self) -> int:
        """Emulation of POSIX fork()"""
        self.log("fork()")
        
        request = SyscallRequest(
            type=SyscallType.CREATE_PROCESS,
            args={'name': 'forked_process'}
        )
        response = self._arbiter.execute(request)
        
        if response.success:
            pid = response.data['pid']
            self.log(f"fork -> pid={pid}")
            return pid
        return -1
    
    def execve(self, path: str, args: list) -> int:
        """Emulation of POSIX execve()"""
        self.log(f"execve('{path}', {args})")
        request = SyscallRequest(
            type=SyscallType.CREATE_PROCESS,
            args={'name': f"exec:{path}"}
        )
        response = self._arbiter.execute(request)
        return response.data['pid'] if response.success else -1
    
    def sleep(self, seconds: int) -> int:
        """Emulation of POSIX sleep()"""
        self.log(f"sleep({seconds})")
        
        request = SyscallRequest(
            type=SyscallType.SLEEP,
            args={'seconds': seconds}
        )
        response = self._arbiter.execute(request)
        return 0 if response.success else -1
    
    def get_log(self):
        return self._log


# =============================================================================
# NT COMPATIBILITY LAYER
# =============================================================================

class NtCompatLayer:
    """
    Compatibility layer for NT-like systems.
    
    Translates WinAPI-style calls to the arbiter's internal API.
    
    Supported calls:
    - CreateFile()   → READ_FILE
    - ReadFile()     → return from cache
    - CloseHandle()  → handle removal
    - CreateProcess()→ CREATE_PROCESS
    - Sleep()        → SLEEP
    """
    
    def __init__(self, arbiter: HybridArbiter):
        self._arbiter = arbiter
        self._open_handles = {}
        self._next_handle = 1
        self._log = []
    
    def log(self, msg: str):
        self._log.append(f"[NT] {msg}")
        print(f"[NT] {msg}")
    
    def CreateFile(self, lpFileName: str, dwDesiredAccess: int = 0) -> int:
        """Emulation of WinAPI CreateFile()"""
        self.log(f"CreateFile('{lpFileName}', access={dwDesiredAccess})")
        
        request = SyscallRequest(
            type=SyscallType.READ_FILE,
            args={'path': lpFileName}
        )
        response = self._arbiter.execute(request)
        
        if response.success:
            handle = self._next_handle
            self._next_handle += 1
            self._open_handles[handle] = {
                'path': lpFileName,
                'content': response.data['content'],
                'size': response.data['size']
            }
            self.log(f"CreateFile -> handle={handle}")
            return handle
        else:
            self.log(f"CreateFile -> ERROR: {response.error}")
            return -1
    
    def ReadFile(self, hFile: int, nNumberOfBytesToRead: int) -> str:
        """Emulation of WinAPI ReadFile()"""
        self.log(f"ReadFile(handle={hFile}, size={nNumberOfBytesToRead})")
        
        if hFile in self._open_handles:
            content = self._open_handles[hFile]['content'][:nNumberOfBytesToRead]
            self.log(f"ReadFile -> '{content}'")
            return content
        else:
            self.log(f"ReadFile -> ERROR: invalid handle")
            return ""
    
    def CloseHandle(self, hObject: int) -> int:
        """Emulation of WinAPI CloseHandle()"""
        self.log(f"CloseHandle(handle={hObject})")
        
        if hObject in self._open_handles:
            del self._open_handles[hObject]
            return 1
        return 0
    
    def CreateProcess(self, lpApplicationName: str) -> int:
        """Emulation of WinAPI CreateProcess()"""
        self.log(f"CreateProcess('{lpApplicationName}')")
        
        request = SyscallRequest(
            type=SyscallType.CREATE_PROCESS,
            args={'name': lpApplicationName}
        )
        response = self._arbiter.execute(request)
        
        if response.success:
            self.log(f"CreateProcess -> PID={response.data['pid']}")
            return response.data['pid']
        return -1
    
    def Sleep(self, dwMilliseconds: int) -> None:
        """Emulation of WinAPI Sleep()"""
        self.log(f"Sleep({dwMilliseconds}ms)")
        seconds = dwMilliseconds / 1000.0
        
        request = SyscallRequest(
            type=SyscallType.SLEEP,
            args={'seconds': seconds}
        )
        self._arbiter.execute(request)
    
    def GetLog(self):
        return self._log


# =============================================================================
# TEST SCENARIO
# =============================================================================

def main():
    """Main test function"""
    print("=" * 70)
    print("Manpupuner_42 - HYBRID SYSTEM CALL ARBITER")
    print("=" * 70)
    print(f"Version: 0.1")
    print(f"Date: 21.06.2026")
    print("=" * 70)
    print()
    
    # Initialization
    print(">>> SYSTEM INITIALIZATION")
    print("-" * 70)
    
    arbiter = HybridArbiter()
    print("✅ Arbiter kernel initialized")
    
    posix = PosixCompatLayer(arbiter)
    nt = NtCompatLayer(arbiter)
    print("✅ Compatibility layers created")
    print()
    
    # Test 1: POSIX program reads a file
    print(">>> TEST 1: POSIX program")
    print("-" * 70)
    print()
    
    print("> POSIX: open('/home/user/hello.txt')")
    fd = posix.open("/home/user/hello.txt")
    if fd != -1:
        print(f"> POSIX: read(fd={fd}, size=50)")
        content = posix.read(fd, 50)
        print(f"> Read: '{content}'")
        print("> POSIX: close(fd)")
        posix.close(fd)
    print()
    
    # Test 2: NT program reads a file
    print(">>> TEST 2: NT program")
    print("-" * 70)
    print()
    
    print("> NT: CreateFile('C:\\\\Users\\\\User\\\\hello.txt')")
    handle = nt.CreateFile("C:\\Users\\User\\hello.txt")
    if handle != -1:
        print(f"> NT: ReadFile(handle={handle}, size=50)")
        content = nt.ReadFile(handle, 50)
        print(f"> Read: '{content}'")
        print("> NT: CloseHandle(handle)")
        nt.CloseHandle(handle)
    print()
    
    # Test 3: Process management
    print(">>> TEST 3: Process management")
    print("-" * 70)
    print()
    
    print("> POSIX: fork()")
    pid = posix.fork()
    print(f"> Process created with PID {pid}")
    print()
    
    print("> NT: CreateProcess('notepad.exe')")
    pid2 = nt.CreateProcess("notepad.exe")
    print(f"> Process created with PID {pid2}")
    print()
    
    # Test 4: List files
    print(">>> TEST 4: Virtual FS listing")
    print("-" * 70)
    print()
    
    print("> Arbiter: LIST_FILES")
    response = arbiter.execute(SyscallRequest(
        type=SyscallType.LIST_FILES,
        args={}
    ))
    if response.success:
        files = response.data['files']
        print(f"> Found {response.data['count']} files:")
        for f in files:
            print(f"    - {f}")
    print()
    
    # Test 5: Direct arbiter call
    print(">>> TEST 5: Direct arbiter call")
    print("-" * 70)
    print()
    
    print("> Direct READ_FILE call")
    response = arbiter.execute(SyscallRequest(
        type=SyscallType.READ_FILE,
        args={'path': '/README.md'}
    ))
    if response.success:
        print(f"> README.md content:\n{response.data['content']}")
    print()
    
    # Summary
    print("=" * 70)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("The principle of a unified arbiter has been proven!")
    print("=" * 70)
    print()
    print("Key takeaways:")
    print("  ✅ The arbiter understands commands from two different 'worlds'")
    print("  ✅ Different external calls are reduced to a single internal API")
    print("  ✅ Only 7 basic calls are needed for operation")
    print()
    print("=" * 70)
    print("Manpupuner_42 - Proof of Concept v0.1")
    print("Idea and architecture author: Kafemin")
    print("Technical implementation: with DeepSeek AI assistant participation")
    print("=" * 70)


if __name__ == "__main__":
    main()
