import la
from matrix import Matrix


def test_make_dimensions():
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 0x-1 _ {matrix}", None).get_message() == ("incorrect dimensions, matrix not "
                                                                                 "created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 6x0 _ {matrix}", None).get_message() == ("incorrect dimensions, "
                                                                                "matrix not created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 0-1 _ {matrix}", None).get_message() == ("incorrect dimensions, "
                                                                                "matrix not created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 33 _ {matrix}", None).get_message() == ("incorrect dimensions, "
                                                                               "matrix not created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make xxx _ {matrix}", None).get_message() == ("incorrect dimensions, "
                                                                                "matrix not created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 6x6x6x6x6x6x6 _ {matrix}", None).get_message() == ("incorrect dimensions, "
                                                                                          "matrix not created")


def test_make_variable():
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3 ear {matrix}", None).get_message() == "matrix created"
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3 3 {matrix}", None).get_message() == "matrix created"
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3  {matrix}", None).get_message() == "matrix created"


def test_make_values():
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3 x {matrix}", None).get_message() == "matrix created"
    matrix = ("0,-72,3:"
              "-01,3.2,-0.0:"
              "5.21,0,2:"
              "-20000,5,8:")
    assert la.command_processor(f"make 4x3 x {matrix}", None).get_message() == "matrix created"
    matrix = "0,-72,3,0,0,12,7,-61000"
    assert la.command_processor(f"make 1x8 x {matrix}", None).get_message() == "matrix created"
    matrix = (",2,3:"
              "1,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3 x {matrix}", None).get_message() == "incorrect values, matrix not created"
    matrix = "34"
    assert la.command_processor(f"make 3x3 x {matrix}", None).get_message() == "incorrect values, matrix not created"
    matrix = ','
    assert la.command_processor(f"make 3x3 x {matrix}", None).get_message() == "incorrect values, matrix not created"


def test_addr_matrix():
    # correct parameters
    coefficient_matrix = ("1,2,3:"
                          "1,2,3:"
                          "1,2,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None).get_matrix()
    assert la.addr(matrix, "1,2,3").get_message() == "row added"

    coefficient_matrix = ("0,-72,3:"
                          "-01,3.2,-0.0:"
                          "5.21,0,2:"
                          "-20000,5,8:")
    matrix = la.command_processor(f"make 4x3 x {coefficient_matrix}", None).get_matrix()
    assert la.addr(matrix, "1,2,3").get_message() == "row added"

    coefficient_matrix = "0,-72,3,0,0,12,7,-61000"
    matrix = la.command_processor(f"make 1x8 x {coefficient_matrix}", None).get_matrix()
    assert la.addr(matrix, "1,2,3,4,5,6,7,8").get_message() == "row added"

    # incorrect parameters
    coefficient_matrix = ("1,2,3:"
                          "1,2,3:"
                          "1,2,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None).get_matrix()
    assert la.addr(matrix, "1,2,3,4").get_message() == "incorrect column count, row not added"

    coefficient_matrix = ("0,-72,3:"
                          "-01,3.2,-0.0:"
                          "5.21,0,2:"
                          "-20000,5,8:")
    matrix = la.command_processor(f"make 4x3 x {coefficient_matrix}", None).get_matrix()
    assert la.addr(matrix, "1,23").get_message() == "incorrect column count, row not added"

    coefficient_matrix = "0,-72,3,0,0,12,7,-61000"
    matrix = la.command_processor(f"make 1x8 x {coefficient_matrix}", None).get_matrix()
    assert la.addr(matrix, "1,2,3,4,5,x,7,8").get_message() == "incorrect values, row not added"

    coefficient_matrix = "0,-72,3,0,0,12,7,-61000"
    matrix = la.command_processor(f"make 1x8 x {coefficient_matrix}", None).get_matrix()
    assert la.addr(matrix, "1,2,3,4,5,,7,8").get_message() == "incorrect values, row not added"


def test_replace():
    correct_coefficient_matrix = ("11.0,11.0,11.0:"
                                  "2.0,2.0,2.0:"
                                  "3.0,3.0,3.0")
    coefficient_matrix = ("1,1,1:"
                          "2,2,2:"
                          "3,3,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None).get_matrix()
    response = la.command_processor("replace r1 r2 5", matrix)
    assert response.get_message() == "R1 + (5R2) -> R1"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix() == correct_coefficient_matrix

    correct_coefficient_matrix = ("0.0,-72.0,3.0:"
                                  "-1.0,3.2,0.0:"
                                  "-19994.79,5.0,10.0:"
                                  "-20000.0,5.0,8.0")
    coefficient_matrix = ("0,-72,3:"
                          "-01,3.2,0.0:"
                          "5.21,0,2:"
                          "-20000,5,8:")
    matrix = la.command_processor(f"make 4x3 x {coefficient_matrix}", None).get_matrix()
    response = la.command_processor("replace r3 r4 1", matrix)
    assert response.get_message() == "R3 + (1R4) -> R3"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix() == correct_coefficient_matrix
