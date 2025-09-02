class Matrix:
    def __init__(self, rows, columns, coefficient_matrix, variables):
        self.rows = rows
        self.columns = columns
        self.coefficient_matrix = coefficient_matrix
        self.variable_matrix = variables

    def replace(self, target_row, addend_row, multiplier):
        for column in range(self.columns):
            self.coefficient_matrix[target_row][column] += self.coefficient_matrix[addend_row][column] * multiplier

    def interchange(self, first_row, second_row):
        temp = self.coefficient_matrix[first_row]
        self.coefficient_matrix[first_row] = self.coefficient_matrix[second_row]
        self.coefficient_matrix[second_row] = temp

    def scale(self, row_num, multiplier):
        for column in range(self.columns):
            self.coefficient_matrix[row_num][column] *= multiplier

    def add_row(self, row):
        self.coefficient_matrix.append(row)
        self.rows += 1

    def add_column(self, new_vector):
        for row in range(self.rows):
            self.coefficient_matrix[row].append(new_vector[row])
        self.columns += 1

    def print_coefficient_matrix(self):
        for row in self.coefficient_matrix:
            for column in row:
                if column >= 0:
                    print(f" {column}", end=' ')
                else:
                    print(column, end=' ')
            print()

    def print_as_vector(self):
        pass