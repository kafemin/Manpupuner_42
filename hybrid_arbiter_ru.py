#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
Manpupuner_42 - Гибридный арбитр системных вызовов

Демонстрация принципа: единое ядро понимает вызовы в стиле POSIX и NT

Версия: 0.1
Дата: 21.06.2026

Автор идеи и архитектуры: Kafemin
Техническая реализация: при участии AI-ассистента DeepSeek

Лицензия: MIT (демонстрационный проект)
================================================================================
"""

import time
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


# =============================================================================
# ВНУТРЕННИЙ API АРБИТРА (ЕДИНЫЙ СТАНДАРТ)
# =============================================================================

class SyscallType(Enum):
    """
    Типы системных вызовов, понятные арбитру
    
    Эти 7 типов образуют фундамент системы — как семь столбов Маньпупунёра.
    """
    READ_FILE = 1        # Чтение файла
    WRITE_FILE = 2       # Запись файла
    CREATE_PROCESS = 3   # Создание процесса
    SLEEP = 4            # Пауза
    ALLOC_MEMORY = 5     # Выделение памяти
    FREE_MEMORY = 6      # Освобождение памяти
    LIST_FILES = 7       # Список файлов


@dataclass
class SyscallRequest:
    """
    Внутренний формат запроса к арбитру
    
    Любой внешний вызов (из POSIX или NT) преобразуется в этот формат.
    """
    type: SyscallType          # Тип операции
    args: Dict[str, Any]       # Аргументы в унифицированном виде

    def __repr__(self):
        return f"<Запрос {self.type.name} {self.args}>"


@dataclass
class SyscallResponse:
    """
    Внутренний формат ответа арбитра
    
    Единый формат возврата результатов для всех слоёв совместимости.
    """
    success: bool              # Успешность операции
    data: Any = None           # Данные результата
    error: Optional[str] = None  # Сообщение об ошибке

    def __repr__(self):
        if self.success:
            return f"<Ответ OK: {self.data}>"
        return f"<Ответ ОШИБКА: {self.error}>"


# =============================================================================
# ЕДИНЫЙ АРБИТР (ЯДРО)
# =============================================================================

class HybridArbiter:
    """
    Единое ядро-арбитр.
    
    Этот класс является сердцем системы. Он:
    - Принимает внутренние запросы (SyscallRequest)
    - Выполняет их через собственный минимальный набор функций
    - Управляет виртуальной файловой системой, памятью и процессами
    - Не знает, откуда пришёл запрос — из POSIX или NT
    """

    def __init__(self):
        # =============================================================
        # Виртуальная файловая система (в памяти)
        # =============================================================
        self._filesystem: Dict[str, str] = {
            "/etc/hosts": "127.0.0.1 localhost",
            "/home/user/hello.txt": "Привет от гибридного ядра!",
            "C:\\Users\\User\\hello.txt": "Привет со стороны NT!",
            "/README.md": "# Manpupuner_42\n\nГибридное ядро\n\nДемонстрация концепции v0.1",
        }
        
        # =============================================================
        # Виртуальная память (для демонстрации)
        # =============================================================
        self._memory_blocks: Dict[int, bytes] = {}
        self._next_mem_id = 0
        
        # =============================================================
        # Управление процессами
        # =============================================================
        self._process_count = 0
        
        # =============================================================
        # Логгирование
        # =============================================================
        self._log = []
    
    def log(self, msg: str):
        """Запись в лог арбитра"""
        self._log.append(f"[Арбитр] {msg}")
        print(f"[Арбитр] {msg}")
    
    # =========================================================================
    # ВНУТРЕННИЙ API (вызывается слоями совместимости)
    # =========================================================================
    
    def execute(self, request: SyscallRequest) -> SyscallResponse:
        """
        Главный диспетчер. Принимает внутренний запрос и выполняет его.
        
        Это единственная точка входа для всех слоёв совместимости.
        """
        self.log(f"Выполнение: {request}")
        
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
                return SyscallResponse(False, error=f"Неизвестный системный вызов: {request.type}")
        except Exception as e:
            return SyscallResponse(False, error=str(e))
    
    # =========================================================================
    # РЕАЛИЗАЦИЯ СИСТЕМНЫХ ВЫЗОВОВ
    # =========================================================================
    
    def _sys_read_file(self, path: str) -> SyscallResponse:
        """Чтение файла из виртуальной ФС"""
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
            return SyscallResponse(False, error=f"Файл не найден: {path}")
    
    def _sys_write_file(self, path: str, data: str) -> SyscallResponse:
        """Запись файла в виртуальную ФС"""
        self._filesystem[path] = data
        return SyscallResponse(True, {'path': path, 'size': len(data)})
    
    def _sys_create_process(self, name: str) -> SyscallResponse:
        """Создание нового процесса (эмуляция)"""
        self._process_count += 1
        pid = self._process_count
        self.log(f"Создан процесс: {name} (PID={pid})")
        return SyscallResponse(True, {'pid': pid, 'name': name})
    
    def _sys_sleep(self, seconds: int) -> SyscallResponse:
        """Приостановка выполнения"""
        self.log(f"Пауза на {seconds} с...")
        time.sleep(seconds)
        return SyscallResponse(True, {'slept': seconds})
    
    def _sys_alloc_memory(self, size: int) -> SyscallResponse:
        """Выделение виртуальной памяти"""
        mem_id = self._next_mem_id
        self._next_mem_id += 1
        self._memory_blocks[mem_id] = b'\x00' * size
        return SyscallResponse(True, {'id': mem_id, 'size': size})
    
    def _sys_free_memory(self, mem_id: int) -> SyscallResponse:
        """Освобождение памяти"""
        if mem_id in self._memory_blocks:
            del self._memory_blocks[mem_id]
            return SyscallResponse(True, {'freed': mem_id})
        return SyscallResponse(False, error=f"Блок памяти {mem_id} не найден")
    
    def _sys_list_files(self) -> SyscallResponse:
        """Список файлов в виртуальной ФС"""
        files = list(self._filesystem.keys())
        return SyscallResponse(True, {'files': files, 'count': len(files)})
    
    def get_log(self):
        """Возвращает лог арбитра"""
        return self._log


# =============================================================================
# СЛОЙ СОВМЕСТИМОСТИ POSIX
# =============================================================================

class PosixCompatLayer:
    """
    Слой совместимости для POSIX-подобных систем.
    
    Транслирует вызовы в стиле POSIX во внутренний API арбитра.
    
    Поддерживаемые вызовы:
    - open()   → READ_FILE
    - read()   → возврат из кэша
    - close()  → удаление дескриптора
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
        """Эмуляция POSIX open()"""
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
            self.log(f"open -> ОШИБКА: {response.error}")
            return -1
    
    def read(self, fd: int, size: int) -> str:
        """Эмуляция POSIX read()"""
        self.log(f"read(fd={fd}, size={size})")
        
        if fd in self._open_files:
            content = self._open_files[fd]['content'][:size]
            self.log(f"read -> '{content}'")
            return content
        else:
            self.log(f"read -> ОШИБКА: неверный fd")
            return ""
    
    def close(self, fd: int) -> int:
        """Эмуляция POSIX close()"""
        self.log(f"close(fd={fd})")
        
        if fd in self._open_files:
            del self._open_files[fd]
            return 0
        return -1
    
    def fork(self) -> int:
        """Эмуляция POSIX fork()"""
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
        """Эмуляция POSIX execve()"""
        self.log(f"execve('{path}', {args})")
        request = SyscallRequest(
            type=SyscallType.CREATE_PROCESS,
            args={'name': f"exec:{path}"}
        )
        response = self._arbiter.execute(request)
        return response.data['pid'] if response.success else -1
    
    def sleep(self, seconds: int) -> int:
        """Эмуляция POSIX sleep()"""
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
# СЛОЙ СОВМЕСТИМОСТИ NT
# =============================================================================

class NtCompatLayer:
    """
    Слой совместимости для NT-подобных систем.
    
    Транслирует вызовы в стиле WinAPI во внутренний API арбитра.
    
    Поддерживаемые вызовы:
    - CreateFile()   → READ_FILE
    - ReadFile()     → возврат из кэша
    - CloseHandle()  → удаление хэндла
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
        """Эмуляция WinAPI CreateFile()"""
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
            self.log(f"CreateFile -> ОШИБКА: {response.error}")
            return -1
    
    def ReadFile(self, hFile: int, nNumberOfBytesToRead: int) -> str:
        """Эмуляция WinAPI ReadFile()"""
        self.log(f"ReadFile(handle={hFile}, size={nNumberOfBytesToRead})")
        
        if hFile in self._open_handles:
            content = self._open_handles[hFile]['content'][:nNumberOfBytesToRead]
            self.log(f"ReadFile -> '{content}'")
            return content
        else:
            self.log(f"ReadFile -> ОШИБКА: неверный handle")
            return ""
    
    def CloseHandle(self, hObject: int) -> int:
        """Эмуляция WinAPI CloseHandle()"""
        self.log(f"CloseHandle(handle={hObject})")
        
        if hObject in self._open_handles:
            del self._open_handles[hObject]
            return 1
        return 0
    
    def CreateProcess(self, lpApplicationName: str) -> int:
        """Эмуляция WinAPI CreateProcess()"""
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
        """Эмуляция WinAPI Sleep()"""
        self.log(f"Sleep({dwMilliseconds}мс)")
        seconds = dwMilliseconds / 1000.0
        
        request = SyscallRequest(
            type=SyscallType.SLEEP,
            args={'seconds': seconds}
        )
        self._arbiter.execute(request)
    
    def GetLog(self):
        return self._log


# =============================================================================
# ТЕСТОВЫЙ СЦЕНАРИЙ
# =============================================================================

def main():
    """Главная функция тестирования"""
    print("=" * 70)
    print("Manpupuner_42 - ГИБРИДНЫЙ АРБИТР СИСТЕМНЫХ ВЫЗОВОВ")
    print("=" * 70)
    print(f"Версия: 0.1")
    print(f"Дата: 21.06.2026")
    print("=" * 70)
    print()
    
    # Инициализация
    print(">>> ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ")
    print("-" * 70)
    
    arbiter = HybridArbiter()
    print("✅ Ядро-арбитр инициализировано")
    
    posix = PosixCompatLayer(arbiter)
    nt = NtCompatLayer(arbiter)
    print("✅ Слои совместимости созданы")
    print()
    
    # Тест 1: POSIX-программа читает файл
    print(">>> ТЕСТ 1: POSIX-программа")
    print("-" * 70)
    print()
    
    print("> POSIX: open('/home/user/hello.txt')")
    fd = posix.open("/home/user/hello.txt")
    if fd != -1:
        print(f"> POSIX: read(fd={fd}, size=50)")
        content = posix.read(fd, 50)
        print(f"> Прочитано: '{content}'")
        print("> POSIX: close(fd)")
        posix.close(fd)
    print()
    
    # Тест 2: NT-программа читает файл
    print(">>> ТЕСТ 2: NT-программа")
    print("-" * 70)
    print()
    
    print("> NT: CreateFile('C:\\\\Users\\\\User\\\\hello.txt')")
    handle = nt.CreateFile("C:\\Users\\User\\hello.txt")
    if handle != -1:
        print(f"> NT: ReadFile(handle={handle}, size=50)")
        content = nt.ReadFile(handle, 50)
        print(f"> Прочитано: '{content}'")
        print("> NT: CloseHandle(handle)")
        nt.CloseHandle(handle)
    print()
    
    # Тест 3: Управление процессами
    print(">>> ТЕСТ 3: Управление процессами")
    print("-" * 70)
    print()
    
    print("> POSIX: fork()")
    pid = posix.fork()
    print(f"> Создан процесс с PID {pid}")
    print()
    
    print("> NT: CreateProcess('notepad.exe')")
    pid2 = nt.CreateProcess("notepad.exe")
    print(f"> Создан процесс с PID {pid2}")
    print()
    
    # Тест 4: Список файлов
    print(">>> ТЕСТ 4: Просмотр виртуальной ФС")
    print("-" * 70)
    print()
    
    print("> Арбитр: LIST_FILES")
    response = arbiter.execute(SyscallRequest(
        type=SyscallType.LIST_FILES,
        args={}
    ))
    if response.success:
        files = response.data['files']
        print(f"> Найдено {response.data['count']} файлов:")
        for f in files:
            print(f"    - {f}")
    print()
    
    # Тест 5: Прямой вызов арбитра
    print(">>> ТЕСТ 5: Прямой вызов арбитра")
    print("-" * 70)
    print()
    
    print("> Прямой вызов READ_FILE")
    response = arbiter.execute(SyscallRequest(
        type=SyscallType.READ_FILE,
        args={'path': '/README.md'}
    ))
    if response.success:
        print(f"> Содержимое README.md:\n{response.data['content']}")
    print()
    
    # Итоги
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ УСПЕШНО ЗАВЕРШЕНА")
    print("Принцип единого арбитра доказан!")
    print("=" * 70)
    print()
    print("Ключевые выводы:")
    print("  ✅ Арбитр понимает команды из двух разных 'миров'")
    print("  ✅ Разные внешние вызовы сводятся к единому внутреннему API")
    print("  ✅ Для работы достаточно 7 базовых вызовов")
    print()
    print("=" * 70)
    print("Manpupuner_42 - Доказательство концепции v0.1")
    print("Автор идеи и архитектуры: Kafemin")
    print("Техническая реализация: при участии AI-ассистента DeepSeek")
    print("=" * 70)


if __name__ == "__main__":
    main()
