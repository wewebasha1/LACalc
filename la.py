import sys
from matrix import Matrix
from response import Response
from command import Command
from fractions import Fraction


def main():
    matrix = Matrix(None, None, None, None)
    while True:
        user_input = input(":")
        response = command_processor(user_input, matrix)
        matrix = response.get_matrix()
        print(response.get_message())


def command_processor(user_input, matrix):
    if user_input == "quit":
        sys.exit()
    user_input_list = user_input.split(" ")
    command = Command(user_input_list[0], user_input_list[1:])
    match command.get_action():
        case "make":
            return make_array(command.get_parameter()[0], command.get_parameter()[1], command.get_parameter()[2])
        case "addr":
            return addr(matrix, command.get_parameter()[0])
        case "addc":
            return addc(matrix, command.get_parameter()[0])
        case "replace":
            return replace(matrix, command.get_parameter()[0], command.get_parameter()[1], command.get_parameter()[2])
        case "change":
            pass
        case "scale":
            pass
        case "print":
            matrix.print_coefficient_matrix()
            return Response("", matrix)
        case "undo":
            pass
        case _:
            return Response("command not recognized", matrix)


def make_array(dimensions, variable, values):
    # save dimensions
    dimensions_list = dimensions.split('x')
    if len(dimensions_list) != 2:
        return Response("incorrect dimensions, matrix not created", None)
    if not dimensions_list[0].isdigit or not dimensions_list[1].isdigit:
        return Response("incorrect dimensions, matrix not created", None)
    rows = int(dimensions_list[0])
    columns = int(dimensions_list[1])
    if rows <= 0 or columns <= 0:
        return Response("incorrect dimensions, matrix not created", None)

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
        return Response("incorrect values, matrix not created", None)
    except IndexError:
        return Response("incorrect values, matrix not created", None)

    # return matrix
    matrix = Matrix(rows, columns, coefficient_matrix, variables)
    return Response("matrix created", matrix)


def addr(matrix, row):
    try:
        row_str_list = row.split(',')
        if len(row_str_list) != matrix.get_columns():
            return Response("incorrect column count, row not added", matrix)
        row_int_list = list(map(int, row_str_list))
        matrix.add_row(row_int_list)
        return Response("row added", matrix)
    except ValueError:
        return Response("incorrect values, row not added", matrix)


def addc(matrix, column):
    try:
        column_str_list = column.split(',')
        if len(column_str_list) != matrix.get_rows():
            return Response("incorrect row count, column not added", matrix)
        column_int_list = list(map(int, column_str_list))
        matrix.add_column(column_int_list)
        return Response("column added", matrix)
    except ValueError:
        return Response("incorrect values, column not added", matrix)


def replace(matrix, target_row, addend_row, multiplier):
    target = int(target_row.replace("r", ""))
    addend = int(addend_row.replace("r", ""))
    matrix.replace((target-1), (addend-1), float(multiplier))
    return Response(f"R{target} + ({multiplier}R{addend}) -> R{target}", matrix)


if __name__ == '__main__':
    main()
