# -*- coding: utf-8 -*-

"""
Модульные тесты для Manpupuner_42
"""

import unittest
import sys
import os

# Добавляем путь к корневой папке
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_arbiter_ru import HybridArbiter, PosixCompatLayer, NtCompatLayer
from hybrid_arbiter_ru import SyscallRequest, SyscallType


class TestHybridArbiter(unittest.TestCase):
    
    def setUp(self):
        """Создаём ядро и слои для каждого теста"""
        self.kernel = HybridArbiter()
        self.posix = PosixCompatLayer(self.kernel)
        self.nt = NtCompatLayer(self.kernel)
    
    def test_read_file_posix(self):
        """Тест: POSIX-чтение файла"""
        fd = self.posix.open("/home/user/hello.txt")
        self.assertNotEqual(fd, -1, "Файл должен открываться")
        content = self.posix.read(fd, 50)
        self.assertIn("Привет", content, "Содержимое должно содержать 'Привет'")
        self.posix.close(fd)
    
    def test_read_file_nt(self):
        """Тест: NT-чтение файла"""
        handle = self.nt.CreateFile("C:\\Users\\User\\hello.txt")
        self.assertNotEqual(handle, -1, "Файл должен открываться")
        content = self.nt.ReadFile(handle, 50)
        self.assertIn("Привет", content, "Содержимое должно содержать 'Привет'")
        self.nt.CloseHandle(handle)
    
    def test_create_process(self):
        """Тест: создание процесса"""
        pid = self.posix.fork()
        self.assertNotEqual(pid, -1, "Процесс должен создаваться")
    
    def test_list_files(self):
        """Тест: список файлов"""
        response = self.kernel.execute(SyscallRequest(
            type=SyscallType.LIST_FILES,
            args={}
        ))
        self.assertTrue(response.success, "Список файлов должен быть успешным")
        self.assertGreater(response.data['count'], 0, "Должен быть хотя бы один файл")


if __name__ == "__main__":
    unittest.main()
