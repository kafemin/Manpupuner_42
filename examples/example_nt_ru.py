#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Пример использования NT-слоя совместимости
Демонстрирует работу с WinAPI-стилем вызовов

Версия: 0.1
Дата: 21.06.2026
"""

from hybrid_arbiter_ru import HybridArbiter, NtCompatLayer


def main():
    """
    Демонстрация работы NT-слоя
    """
    print("=" * 60)
    print("Пример: NT-программа (WinAPI-стиль)")
    print("=" * 60)
    print()

    # Создаём ядро-арбитр
    print("> Создание ядра-арбитра...")
    kernel = HybridArbiter()
    
    # Создаём NT-слой совместимости
    print("> Создание NT-слоя совместимости...")
    nt = NtCompatLayer(kernel)
    print()

    # =============================================================
    # 1. Открытие файла (CreateFile)
    # =============================================================
    print(">>> 1. Открытие файла (CreateFile)")
    print("-" * 40)
    
    handle = nt.CreateFile("C:\\Users\\User\\hello.txt")
    if handle != -1:
        print(f"✅ Файл открыт, HANDLE: {handle}")
    else:
        print("❌ Ошибка открытия файла")
        return
    print()

    # =============================================================
    # 2. Чтение файла (ReadFile)
    # =============================================================
    print(">>> 2. Чтение файла (ReadFile)")
    print("-" * 40)
    
    content = nt.ReadFile(handle, 50)
    if content:
        print(f"✅ Прочитано: '{content}'")
    else:
        print("❌ Ошибка чтения файла")
    print()

    # =============================================================
    # 3. Закрытие файла (CloseHandle)
    # =============================================================
    print(">>> 3. Закрытие файла (CloseHandle)")
    print("-" * 40)
    
    result = nt.CloseHandle(handle)
    if result == 1:
        print("✅ Файл закрыт")
    else:
        print("❌ Ошибка закрытия файла")
    print()

    # =============================================================
    # 4. Создание процесса (CreateProcess)
    # =============================================================
    print(">>> 4. Создание процесса (CreateProcess)")
    print("-" * 40)
    
    pid = nt.CreateProcess("notepad.exe")
    if pid != -1:
        print(f"✅ Процесс создан, PID: {pid}")
    else:
        print("❌ Ошибка создания процесса")
    print()

    # =============================================================
    # 5. Пауза (Sleep)
    # =============================================================
    print(">>> 5. Пауза (Sleep)")
    print("-" * 40)
    
    nt.Sleep(2000)  # 2000 мс = 2 секунды
    print("✅ Пауза выполнена")
    print()

    print("=" * 60)
    print("Демонстрация завершена")
    print("=" * 60)


if __name__ == "__main__":
    main()
