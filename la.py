import sys
from matrix import Matrix
from fractions import Fraction
def main():
    while(True):
        command = input(":")
        response = menu(command)
        print(response[1])

def menu(command):
    global matrix
    if command == "quit":
        sys.exit()
    commands = command.split(" ")
    match commands[0]:
        case "make":
            matrix = make_array(commands[1], commands[2], commands[3])
            return matrix, "matrix created"
        case "addr":
            pass
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
def make_array(dimensions, variable, nums):
    global variables

    dimensions_list = dimensions.split('x')
    rows = int(dimensions_list[0])
    columns = int(dimensions_list[1])

    # make coefficient matrix
    row_list = nums.split(':')

    coefficient_matrix = []
    for row in range(rows):
        row_str_list = row_list[row].split(';')
        row_num_list = list(map(float, row_str_list))
        coefficient_matrix.append(row_num_list)

    # make variables
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    for index in range(columns):
        variables = variable + str(index) + ' '
    variables.translate(SUB)
    variables.strip()

    # return matrix
    matrix = Matrix(rows, columns, coefficient_matrix, variables)
    return matrix

def addr():
    row_str_list = input(':').split(' ')
    row_int_list = list(map(int, row_str_list))
    matrix.add_row(row_int_list)

if __name__ == '__main__':
    main()