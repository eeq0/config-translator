"""Автотесты транслятора.

При импорте пакета tests папка src добавляется в путь поиска модулей,
поэтому тесты импортируют модули транслятора напрямую.
"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
