import random


class Board:
    top_left_matrix = [[0 for x in range(4)] for y in range(4)]
    top_right_matrix = [[0 for x in range(4)] for y in range(4)]
    center_matrix = [[0 for x in range(4)] for y in range(4)]
    bottom_left_matrix = [[0 for x in range(4)] for y in range(4)]
    bottom_right_matrix = [[0 for x in range(4)] for y in range(4)]

    def __init__(self):
        for matrix in range(5):
            for i in range(4):
                for j in range(4):
                    if not matrix == 2 and \
                            ((i == 0 and j == 0) or (i == 0 and j == 3) or (i == 3 and j == 0) or (i == 3 and j == 3)):
                        has_value = random.randint(0, 100)
                        random_int = random.randint(1, 4)
                        if has_value < 75:
                            value = 2 ** random_int
                            if matrix == 0:
                                self.top_left_matrix[i][j] = value
                            elif matrix == 1:
                                self.top_right_matrix[i][j] = value
                            elif matrix == 2:
                                self.center_matrix[i][j] = value
                            elif matrix == 3:
                                self.bottom_left_matrix[i][j] = value
                            elif matrix == 4:
                                self.bottom_right_matrix[i][j] = value


    def print_board(self):
        result = ""
        for i in range(4):
            for j in range(4):
                result += str(self.top_left_matrix[i][j]) + " "
            if i != 3:
                result += "    "
            else:
                result += str(self.center_matrix[0][1]) + " " + str(self.center_matrix[0][2]) + " "

            for j in range(4):
                result += str(self.top_right_matrix[i][j]) + " "
            result += "\n"


        for i in range(1,3):
            result += "      "
            for j in range(4):
                result += str(self.center_matrix[i][j]) + " "
            result += "\n"

        for i in range(4):
            for j in range(4):
                result += str(self.bottom_left_matrix[i][j]) + " "
            if i != 0:
                result += "    "
            else:
                result += str(self.center_matrix[3][1]) + " " + str(self.center_matrix[3][2]) + " "
            for j in range(4):
                result += str(self.bottom_right_matrix[i][j]) + " "
            result += "\n"

        print(result)


my_board = Board()
my_board.print_board()
