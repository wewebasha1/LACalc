import sys
from matrix import Matrix
from fractions import Fraction


def main():
    matrix = None
    while True:
        command = input(":")
        response = command_processor(command, matrix)
        print(response[1])


def command_processor(command, matrix):
    if command == "quit":
        sys.exit()
    commands = command.split(" ")
    match commands[0]:
        case "make":
            response = make_array(commands[1], commands[2], commands[3])
            return response[0], response[1]
        case "addr":
            response = addr(commands[1], commands[2])
            return response[0], response[1]
        case "addc":
            pass
        case "replace":
            pass
        case "change":
            pass
        case "scale":
            pass
        case "print":
            matrix.print_coefficient_matrix()
            return matrix, ""
        case _:
            return matrix, "command not recognized"


def make_array(dimensions, variable, values):
    # save dimensions
    dimensions_list = dimensions.split('x')
    if len(dimensions_list) != 2:
        return None, "incorrect dimensions, matrix not created"
    if not dimensions_list[0].isdigit or not dimensions_list[1].isdigit:
        return None, "incorrect dimensions, matrix not created"
    rows = int(dimensions_list[0])
    columns = int(dimensions_list[1])
    if rows <= 0 or columns <= 0:
        return None, "incorrect dimensions, matrix not created"

    # make variables
    variables = None
    sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    for index in range(columns):
        variables = variable + str(index) + ' '
    variables.translate(sub)
    variables.strip()

    # make coefficient matrix
    try:
        row_list = values.split(':')
        coefficient_matrix = []
        for row in range(rows):
            row_str_list = row_list[row].split(',')
            row_num_list = list(map(float, row_str_list))
            coefficient_matrix.append(row_num_list)
    except ValueError:
        return None, "incorrect values, matrix not created"
    except IndexError:
        return None, "incorrect values, matrix not created"

    # return matrix
    matrix = Matrix(rows, columns, coefficient_matrix, variables)
    return matrix, "matrix created"


def addr(matrix, row):
    row_str_list = row.split(',')
    row_int_list = list(map(int, row_str_list))
    matrix.add_row(row_int_list)
    return matrix, "row added"


if __name__ == '__main__':
    main()
