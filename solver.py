import sys


class Matrix:

    def __init__(self):
        file = open(sys.argv[2], 'r')
        # file = open("in.txt", 'r')
        lines = file.readlines()
        print(lines[0])
        file.close()
        first_line = lines[0].split()
        self.number_of_rows = int(first_line[1])
        self.number_of_columns = int(first_line[0]) + 1
        self.count_of_variables = int(first_line[0])
        self.matrix = []
        for row_index in range(self.number_of_rows):
            new_list = [complex(x) for x in lines[row_index + 1].split()]
            self.matrix.append(new_list)
        self.print_matrix()
        self.order = {}
        for i in range(self.count_of_variables):
            self.order[i] = i

    @staticmethod
    def divide_line(row):
        coefficient = 0
        for q in range(len(row)):
            if coefficient != 0:
                row[q] = row[q] / coefficient
            elif row[q] != 0:
                coefficient = row[q]
                row[q] = 1

    def divide_rows(self, line_master, line_divided, index):
        coefficient = -line_divided[index]
        for k in range(self.number_of_columns):
            line_divided[k] = line_master[k] * coefficient + line_divided[k]

    def print_matrix(self):
        for e in self.matrix:
            print(e)

    def swap_rows(self, i, j):
        temp = self.matrix[i]
        self.matrix[i] = self.matrix[j]
        self.matrix[j] = temp

    def find_not_zero_in_columns(self, u):
        for o in range(u + 1, self.number_of_rows):
            if self.matrix[o][u] == 0:
                continue
            self.swap_rows(u, o)
            return True
        return False

    def swap_columns(self, i, j):
        for q in range(self.number_of_rows):
            temp = self.matrix[q][i]
            self.matrix[q][i] = self.matrix[q][j]
            self.matrix[q][j] = temp
        self.order[i] = j
        self.order[j] = i

    def find_not_zero_in_rows(self, i):
        for o in range(i + 1, self.count_of_variables):
            if self.matrix[i][o] == 0:
                continue
            self.swap_columns(o, i)
            return True
        return False

    def find_not_zero(self, w):
        for i in range(w + 1, self.number_of_rows):
            for j in range(w + 1, self.number_of_columns - 1):
                if self.matrix[i][j] != 0:
                    self.swap_columns(w, j)
                    self.swap_rows(w, i)
                    return True
        return False

    def have_solution(self):
        last_non_zero_row = None
        for i in range(self.number_of_rows):
            if self.all_zero(self.matrix[i][0:self.count_of_variables]):
                if self.matrix[i][self.count_of_variables] != 0:
                    file_out = open(sys.argv[4], 'w', encoding='utf-8')
                    file_out.write('No solutions')
                    file_out.close()
                    return False
            elif last_non_zero_row is None or last_non_zero_row < i:
                last_non_zero_row = i
        if last_non_zero_row is None\
                or (self.count_of_variables > self.number_of_rows or last_non_zero_row + 1 < self.count_of_variables):
            file_out = open(sys.argv[4], 'w', encoding='utf-8')
            file_out.write('Infinitely many solutions')
            file_out.close()
            return False
        return True

    @staticmethod
    def all_zero(row):
        for i in row:
            if i != 0:
                return False
        return True

    def calculate(self):
        print("Start solving the equation.")
        for w in range(self.number_of_rows):
            if self.matrix[w][w] == 0:
                if not self.find_not_zero_in_columns(w) and not self.find_not_zero_in_rows(w)\
                        and not self.find_not_zero(w):
                    break
            if self.matrix[w][w] != 1:
                self.divide_line(self.matrix[w])
                print(f"R{w + 1} -> 1")
                self.print_matrix()
            for i in range(w + 1, self.number_of_rows):
                if self.matrix[i][w] != 0:
                    print(f"{-self.matrix[i][w]} * R{w + 1} + R{i + 1}")
                    self.divide_rows(self.matrix[w], self.matrix[i], w)
                    self.print_matrix()
        if not self.have_solution():
            return None

        for y in range(self.count_of_variables - 1, 0, -1):
            for t in range(y - 1, -1, -1):
                if self.matrix[t][y] != 0:
                    print(f"{-self.matrix[t][y]} * R{y + 1} + R{t + 1}")
                    self.divide_rows(self.matrix[y], self.matrix[t], y)
                    self.print_matrix()

        file_out = open(sys.argv[4], 'w', encoding='utf-8')
        for value in self.order.values():
            complex_number = self.matrix[value][self.number_of_columns - 1]
            if complex_number.imag == 0:
                print(str(complex_number.real))
                file_out.write(str(complex_number.real) + '\n')
            else:
                print(str(self.matrix[value][self.number_of_columns - 1]))
                file_out.write(str(self.matrix[value][self.number_of_columns - 1]) + '\n')
        file_out.close()


matrix = Matrix()
matrix.calculate()
