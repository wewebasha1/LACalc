import sys
from matrix import Matrix
from response import Response
from command import Command
import fractions


def main():
    matrix = Matrix(None, None, None, None)
    history = []
    while True:
        user_input = input(":")
        response = command_processor(user_input, matrix, history)
        matrix = response.get_matrix()
        if response.get_undo_command() is not None:
            history.append(response.get_undo_command())
        if response.get_message() is not None:
            print(response.get_message())


def command_processor(user_input, matrix, history):
    command = None
    try:
        if user_input == "quit":
            sys.exit()
        user_input_list = user_input.split(" ")
        command = Command(user_input_list[0], user_input_list[1:])
        match command.get_action():
            case "make":
                return make_matrix(command.get_parameter()[0],
                                   command.get_parameter()[1],
                                   command.get_parameter()[2])
            case "addr":
                if matrix is None:
                    raise TypeError
                return add_row_check(matrix,
                                     command.get_parameter()[0])
            case "addc":
                if matrix is None:
                    raise TypeError
                return add_column_check(matrix,
                                        command.get_parameter()[0])
            case "replace":
                if matrix is None:
                    raise TypeError
                response = replace_check(matrix,
                                         command.get_parameter()[0],
                                         command.get_parameter()[1],
                                         command.get_parameter()[2])
                response.set_undo_command(generate_undo_command(command))
                return response
            case "change":
                if matrix is None:
                    raise TypeError
                response = interchange_check(matrix,
                                             command.get_parameter()[0],
                                             command.get_parameter()[1])
                response.set_undo_command(generate_undo_command(command))
                return response
            case "scale":
                if matrix is None:
                    raise TypeError
                response = scale_check(matrix,
                                       command.get_parameter()[0],
                                       command.get_parameter()[1])
                response.set_undo_command(generate_undo_command(command))
                return response
            case "print":
                if matrix is None:
                    raise TypeError
                return print_matrix(matrix)
            case "undo":
                if not history:
                    return Response("oldest version", matrix)
                undo_command = history.pop()
                command_processor(undo_command, matrix, history)
                return Response(None, matrix)
            case _:
                return Response("command not recognized", matrix)
    except TypeError:
        return Response(f"no matrix to {command.get_action()}", matrix)
    except IndexError:
        return Response("Incorrect parameter count", matrix)


def make_matrix(dimensions, variable, values):
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
            row_num_list = list(map(fractions.Fraction, row_str_list))
            coefficient_matrix.append(row_num_list)
    except ValueError:
        return Response("incorrect values, matrix not created", None)
    except IndexError:
        return Response("incorrect values, matrix not created", None)

    # return matrix
    matrix = Matrix(rows, columns, coefficient_matrix, variables)
    return Response("matrix created", matrix)


def add_row_check(matrix, row):
    try:
        row_str_list = row.split(',')
        if len(row_str_list) != matrix.get_columns():
            return Response("incorrect column count, row not added", matrix)
        row_frac_list = list(map(fractions.Fraction, row_str_list))
        matrix.add_row(row_frac_list)
        return Response("row added", matrix)
    except ValueError:
        return Response("incorrect values, row not added", matrix)


def add_column_check(matrix, column):
    try:
        column_str_list = column.split(',')
        if len(column_str_list) != matrix.get_rows():
            return Response("incorrect row count, column not added", matrix)
        column_frac_list = list(map(fractions.Fraction, column_str_list))
        matrix.add_column(column_frac_list)
        return Response("column added", matrix)
    except ValueError:
        return Response("incorrect values, column not added", matrix)


def replace_check(matrix, target_row, addend_row, multiplier):
    try:
        target = int(target_row.replace("r", ""))
        addend = int(addend_row.replace("r", ""))
        matrix.replace((target - 1), (addend - 1), fractions.Fraction(multiplier))
        return Response(f"R{target} + ({multiplier}R{addend}) -> R{target}", matrix)
    except IndexError:
        return Response("could not find rows, matrix unchanged", matrix)
    except ValueError:
        return Response("incorrect values, row not replaced", matrix)


def interchange_check(matrix, first_row, second_row):
    try:
        first = int(first_row.replace("r", ""))
        second = int(second_row.replace("r", ""))
        matrix.interchange((first - 1), (second - 1))
        return Response(f"R{first} <-> R{second}", matrix)
    except IndexError:
        return Response("could not find rows, matrix unchanged", matrix)


def scale_check(matrix, row, multiplier):
    try:
        row_num = int(row.replace("r", ""))
        matrix.scale((row_num - 1), fractions.Fraction(multiplier))
        return Response(f"{multiplier}R{row_num} -> R{row_num}", matrix)
    except IndexError:
        return Response("could not find rows, matrix unchanged", matrix)
    except ValueError:
        return Response("incorrect values, row not scaled", matrix)


def print_matrix(matrix):
    matrix.print_coefficient_matrix()
    message = '.' * (5 * matrix.get_columns())
    return Response(message, matrix)


def generate_undo_command(command):
    match command.get_action():
        case "addr":
            pass
        case "addc":
            pass
        case "replace":
            multiplier = fractions.Fraction(command.get_parameter()[2]) * -1
            undo_command = (command.get_action()
                            + ' '
                            + command.get_parameter()[0]
                            + ' '
                            + command.get_parameter()[1]
                            + ' '
                            + str(multiplier))
            return undo_command
        case "change":
            undo_command = (command.get_action()
                            + ' '
                            + command.get_parameter()[0]
                            + ' '
                            + command.get_parameter()[1])
            return undo_command
        case "scale":
            multiplier = fractions.Fraction(command.get_parameter()[1])
            multiplier = fractions.Fraction(multiplier.denominator, multiplier.numerator)
            undo_command = (command.get_action()
                            + ' '
                            + command.get_parameter()[0]
                            + ' '
                            + str(multiplier))
            return undo_command
        case _:
            pass


if __name__ == '__main__':
    main()
