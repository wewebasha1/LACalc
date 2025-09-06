import la


def test_command_processor():
    assert la.command_processor(f"fsdglnjkh", None, None).get_message() == "command not recognized"
    assert la.command_processor(f"print", None, None).get_message() == "no matrix to print"


def test_make_dimensions():
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 0x-1 _ {matrix}", None, None).get_message() == (
        "incorrect dimensions, matrix not "
        "created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 6x0 _ {matrix}", None, None).get_message() == ("incorrect dimensions, "
                                                                                      "matrix not created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 0-1 _ {matrix}", None, None).get_message() == ("incorrect dimensions, "
                                                                                      "matrix not created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 33 _ {matrix}", None, None).get_message() == ("incorrect dimensions, "
                                                                                     "matrix not created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make xxx _ {matrix}", None, None).get_message() == ("incorrect dimensions, "
                                                                                      "matrix not created")
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 6x6x6x6x6x6x6 _ {matrix}", None, None).get_message() == ("incorrect dimensions, "
                                                                                                "matrix not created")


def test_make_variable():
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3 ear {matrix}", None, None).get_message() == "matrix created"
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3 3 {matrix}", None, None).get_message() == "matrix created"
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3  {matrix}", None, None).get_message() == "matrix created"


def test_make_values():
    matrix = ("1,2,3:"
              "1,2,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3 x {matrix}", None, None).get_message() == "matrix created"
    matrix = ("0,-72,3:"
              "-01,3/2,-0:"
              "5/21,0,2:"
              "-20000,5,8:")
    assert la.command_processor(f"make 4x3 x {matrix}", None, None).get_message() == "matrix created"
    matrix = "0,-72,3,0,0,12,7,-61000"
    assert la.command_processor(f"make 1x8 x {matrix}", None, None).get_message() == "matrix created"
    matrix = (",2,3:"
              "1,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3 x {matrix}", None,
                                None).get_message() == "incorrect values, matrix not created"
    matrix = "34"
    assert la.command_processor(f"make 3x3 x {matrix}", None,
                                None).get_message() == "incorrect values, matrix not created"
    matrix = ','
    assert la.command_processor(f"make 3x3 x {matrix}", None,
                                None).get_message() == "incorrect values, matrix not created"
    matrix = ("1,2,3:"
              "1,glk,3:"
              "1,2,3:")
    assert la.command_processor(f"make 3x3 x {matrix}", None,
                                None).get_message() == "incorrect values, matrix not created"


def test_add_row_check():
    # correct parameters
    coefficient_matrix = ("1,2,3:"
                          "1,2,3:"
                          "1,2,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None, None).get_matrix()
    assert la.add_row_check(matrix, "1,2,3").get_message() == "row added"

    coefficient_matrix = ("0,-72,3:"
                          "-01,3/2,-0:"
                          "5/21,0,2:"
                          "-20000,5,8:")
    matrix = la.command_processor(f"make 4x3 x {coefficient_matrix}", None, None).get_matrix()
    assert la.add_row_check(matrix, "1,2/9,3").get_message() == "row added"

    coefficient_matrix = "0,-72,3,0,0,12,7,-61000"
    matrix = la.command_processor(f"make 1x8 x {coefficient_matrix}", None, None).get_matrix()
    assert la.add_row_check(matrix, "1,2,3,4/7,5,6,7,8").get_message() == "row added"

    # incorrect parameters
    coefficient_matrix = ("1,2,3:"
                          "1,2,3:"
                          "1,2,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None, None).get_matrix()
    assert la.add_row_check(matrix, "1,2,3,4").get_message() == "incorrect column count, row not added"

    coefficient_matrix = ("0,-72,3:"
                          "-01,3/2,-0:"
                          "5/21,0,2:"
                          "-20000,5,8:")
    matrix = la.command_processor(f"make 4x3 x {coefficient_matrix}", None, None).get_matrix()
    assert la.add_row_check(matrix, "1,23").get_message() == "incorrect column count, row not added"

    coefficient_matrix = "0,-72,3,0,0,12,7,-61000"
    matrix = la.command_processor(f"make 1x8 x {coefficient_matrix}", None, None).get_matrix()
    assert la.add_row_check(matrix, "1,2,3,4,5,x,7,8").get_message() == "incorrect values, row not added"

    coefficient_matrix = "0,-72,3,0,0,12,7,-61000"
    matrix = la.command_processor(f"make 1x8 x {coefficient_matrix}", None, None).get_matrix()
    assert la.add_row_check(matrix, "1,2,3,4,5,,7,8").get_message() == "incorrect values, row not added"


def test_replace_check():
    correct_coefficient_matrix = ("11,11,11:"
                                  "2,2,2:"
                                  "3,3,3")
    coefficient_matrix = ("1,1,1:"
                          "2,2,2:"
                          "3,3,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None, None).get_matrix()
    response = la.command_processor("replace r1 r2 5", matrix, None)
    assert response.get_message() == "R1 + (5R2) -> R1"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix_str() == correct_coefficient_matrix

    correct_coefficient_matrix = ("0,-72,3:"
                                  "-1,3,0:"
                                  "-19995,3,10:"
                                  "-20000,5/2,8")
    coefficient_matrix = ("0,-72,3:"
                          "-1,3,0:"
                          "5,1/2,2:"
                          "-20000,5/2,8:")
    matrix = la.command_processor(f"make 4x3 x {coefficient_matrix}", None, None).get_matrix()
    response = la.command_processor("replace r3 r4 1", matrix, None)
    assert response.get_message() == "R3 + (1R4) -> R3"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix_str() == correct_coefficient_matrix

    coefficient_matrix = ("0,-72,3:"
                          "-1,3,0:"
                          "5,0,2:"
                          "-20000,5,8")
    matrix = la.command_processor(f"make 4x3 x {coefficient_matrix}", None, None).get_matrix()
    response = la.command_processor("replace r3 r5 1", matrix, None)
    assert response.get_message() == "could not find rows, matrix unchanged"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix_str() == coefficient_matrix


def test_interchange_check():
    correct_coefficient_matrix = ("2,2,2:"
                                  "1,1,1:"
                                  "3,3,3")
    coefficient_matrix = ("1,1,1:"
                          "2,2,2:"
                          "3,3,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None, None).get_matrix()
    response = la.command_processor("change r1 r2", matrix, None)
    assert response.get_message() == "R1 <-> R2"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix_str() == correct_coefficient_matrix

    correct_coefficient_matrix = ("3,3,3:"
                                  "2,2,2:"
                                  "1,1,1")
    coefficient_matrix = ("1,1,1:"
                          "2,2,2:"
                          "3,3,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None, None).get_matrix()
    response = la.command_processor("change r3 r1", matrix, None)
    assert response.get_message() == "R3 <-> R1"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix_str() == correct_coefficient_matrix

    coefficient_matrix = ("1,1,1:"
                          "2,2,2:"
                          "3,3,3")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None, None).get_matrix()
    response = la.command_processor("change r1 r8", matrix, None)
    assert response.get_message() == "could not find rows, matrix unchanged"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix_str() == coefficient_matrix


def test_scale_check():
    correct_coefficient_matrix = ("5,5,5:"
                                  "2,2,2:"
                                  "3,3,3")
    coefficient_matrix = ("1,1,1:"
                          "2,2,2:"
                          "3,3,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None, None).get_matrix()
    response = la.command_processor("scale r1 5", matrix, None)
    assert response.get_message() == "5R1 -> R1"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix_str() == correct_coefficient_matrix

    correct_coefficient_matrix = ("1,1,1:"
                                  "1,1,1:"
                                  "3,3,3")
    coefficient_matrix = ("1,1,1:"
                          "2,2,2:"
                          "3,3,3:")
    matrix = la.command_processor(f"make 3x3 x {coefficient_matrix}", None, None).get_matrix()
    response = la.command_processor("scale r2 0.5", matrix, None)
    assert response.get_message() == "0.5R2 -> R2"
    matrix = response.get_matrix()
    assert matrix.get_coefficient_matrix_str() == correct_coefficient_matrix


def test_undo():
    history = []
    matrix = la.command_processor("make 2x2 x 1,1:1,1", None, None).get_matrix()
    response = la.command_processor("scale r2 2", matrix, None)
    matrix = response.get_matrix()
    history.append(response.get_undo_command())
    response = la.command_processor("change r1 r2", matrix, history)
    matrix = response.get_matrix()
    history.append(response.get_undo_command())
    response = la.command_processor("replace r2 r1 3", matrix, history)
    matrix = response.get_matrix()
    history.append(response.get_undo_command())
    response = la.command_processor("undo", matrix, history)
    assert response.get_matrix().get_coefficient_matrix_str() == "2,2:1,1"
    assert response.get_message() is None
    response = la.command_processor("undo", matrix, history)
    assert response.get_matrix().get_coefficient_matrix_str() == "1,1:2,2"
    assert response.get_message() is None
    response = la.command_processor("undo", matrix, history)
    assert response.get_matrix().get_coefficient_matrix_str() == "1,1:1,1"
    assert response.get_message() is None
    response = la.command_processor("undo", matrix, history)
    assert response.get_matrix().get_coefficient_matrix_str() == "1,1:1,1"
    assert response.get_message() == "oldest version"
