import la


def test_make_dimensions():
    matrix_1 = ("1,2,3:"
                "1,2,3:"
                "1,2,3:")
    assert la.command_processor(f"make 0x-1 _ {matrix_1}", None)[1] == "incorrect dimensions, matrix not created"
    matrix_2 = ("1,2,3:"
                "1,2,3:"
                "1,2,3:")
    assert la.command_processor(f"make 6x0 _ {matrix_2}", None)[1] == "incorrect dimensions, matrix not created"
    matrix_3 = ("1,2,3:"
                "1,2,3:"
                "1,2,3:")
    assert la.command_processor(f"make 0-1 _ {matrix_3}", None)[1] == "incorrect dimensions, matrix not created"
    matrix_4 = ("1,2,3:"
                "1,2,3:"
                "1,2,3:")
    assert la.command_processor(f"make 33 _ {matrix_4}", None)[1] == "incorrect dimensions, matrix not created"
    matrix_5 = ("1,2,3:"
                "1,2,3:"
                "1,2,3:")
    assert la.command_processor(f"make xxx _ {matrix_5}", None)[1] == "incorrect dimensions, matrix not created"
    matrix_5 = ("1,2,3:"
                "1,2,3:"
                "1,2,3:")
    assert la.command_processor(f"make 6x6x6x6x6x6x6 _ {matrix_5}", None)[1] == ("incorrect dimensions, matrix not "
                                                                                 "created")


def test_make_variable():
    matrix_1 = ("1,2,3:"
                "1,2,3:"
                "1,2,3:")
    assert la.command_processor(f"make 3x3 ear {matrix_1}", None)[1] == "matrix created"
    matrix_1 = ("1,2,3:"
                "1,2,3:"
                "1,2,3:")
    assert la.command_processor(f"make 3x3 3 {matrix_1}", None)[1] == "matrix created"


def test_make_values():
    matrix_1 = ("1,2,3:"
                "1,2,3:"
                "1,2,3:")
    assert la.command_processor(f"make 3x3 x {matrix_1}", None)[1] == "matrix created"
    matrix_2 = ("0,-72,3:"
                "-01,3.2,-0.0:"
                "5.21,0,2:"
                "-20000,5,8:")
    assert la.command_processor(f"make 4x3 x {matrix_2}", None)[1] == "matrix created"
    matrix_3 = "0,-72,3,0,0,12,7,-61000"
    assert la.command_processor(f"make 1x8 x {matrix_3}", None)[1] == "matrix created"
    matrix_4 = (",2,3:"
                "1,3:"
                "1,2,3:")
    assert la.command_processor(f"make 3x3 x {matrix_4}", None)[1] == "incorrect values, matrix not created"
    matrix_5 = "34"
    assert la.command_processor(f"make 3x3 x {matrix_5}", None)[1] == "incorrect values, matrix not created"
    matrix_6 = ','
    assert la.command_processor(f"make 3x3 x {matrix_6}", None)[1] == "incorrect values, matrix not created"


def test_addr_matrix():
    coefficient_matrix_1 = ("1,2,3:"
                            "1,2,3:"
                            "1,2,3:")
    matrix_1 = la.command_processor(f"make 3x3 x {coefficient_matrix_1}", None)[0]
    assert la.addr(matrix_1, "1,2,3")[1] == "row added"
    coefficient_matrix_2 = ("0,-72,3:"
                            "-01,3.2,-0.0:"
                            "5.21,0,2:"
                            "-20000,5,8:")
    matrix_2 = la.command_processor(f"make 4x3 x {coefficient_matrix_2}", None)[0]
    assert la.addr(matrix_2, "1,2,3")[1] == "row added"
    coefficient_matrix_3 = "0,-72,3,0,0,12,7,-61000"
    matrix_3 = la.command_processor(f"make 1x8 x {coefficient_matrix_3}", None)[0]
    assert la.addr(matrix_3, "1,2,3,4,5,6,7,8")[1] == "row added"

    # add commands with incorrect parameters for addr
