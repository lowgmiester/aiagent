from functions.get_files_info import *
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


def test_main():
    result = run_python_file("calculator", "main.py")
    print(result)

def test_tests():
    result = run_python_file("calculator", "tests.py")
    print(result)

def test_er_main():
    result = run_python_file("calculator", "../main.py")
    print(result)

def test_er_non():
    result = run_python_file("calculator", "nonexistent.py")
    print(result)


if __name__ == "__main__":
    test_main()
    test_tests()
    test_er_main()
    test_er_non()
