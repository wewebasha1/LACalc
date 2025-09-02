import sys
import pytest
import la
import matrix

def test_make():
    matrix_1 = ("1;2;3:"
              "1;2;3:"
              "1;2;3:")
    assert la.menu(f"make 3x3 x {matrix_1}") == "matrix created"
    matrix_2 = ("0;-72;3:"
                "-01;3.2;-0.0:"
                "5.21;0;2:"
                "-20000;5;8:")
    assert la.menu(f"make 4x3 x {matrix_2}") == "matrix created"
    matrix_3 = ("0;-72;3;0;0;12;7;-61000")
    assert la.menu(f"make 1x8 x {matrix_3}") == "matrix created"

def test_make_error():
    pass

def test_print():
    matrix_3 = ("0;-72;3;0;0;12;7;-61000")
    assert la.menu(f"make 1x8 x {matrix_3}") == "matrix created"
    assert la.menu("print") == ""