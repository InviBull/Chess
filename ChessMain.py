import pygame


# ChessEngine

class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    def make_move(self, move, is_enpassant):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.pieceMoved
        if is_enpassant == 1:
            self.board[move.start_row][move.end_col] = "--"

        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def get_sq_covered(self):
        sqs_covered = [
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ]
        for i, x in enumerate(self.board):
            for j, y in enumerate(x):
                start_row, start_col = i, j
                start = y
                if start[1] == "P":
                    if start[0] == "w":
                        try:
                            sqs_covered[start_row - 1][start_col + 1] += "w"
                        except IndexError:
                            pass
                        try:
                            sqs_covered[start_row - 1][start_col - 1] += "w"
                        except IndexError:
                            pass
                    if start[0] == "b":
                        try:
                            sqs_covered[start_row + 1][start_col + 1] += "b"
                        except IndexError:
                            pass
                        try:
                            sqs_covered[start_row + 1][start_col - 1] += "b"
                        except IndexError:
                            pass
                if start[1] == "R" or start[1] == "Q":
                    for c in range(0, j):
                        sqs_covered[start_row][c] += start[0]
                        if self.board[start_row][c] != "--":
                            break
                    for c in range(j, 8):
                        sqs_covered[start_row][c] += start[0]
                        if self.board[start_row][c] != "--":
                            break
                    for c in range(0, i):
                        sqs_covered[c][start_col] += start[0]
                        if self.board[c][start_col] != "--":
                            break
                    for c in range(i, 8):
                        sqs_covered[c][start_col] += start[0]
                        if self.board[c][start_col] != "--":
                            break
                if start[1] == "B" or start[1] == "Q":
                    for c in range(0, min(8 - i, 8 - j)):
                        sqs_covered[i + c][j + c] += start[0]
                        if self.board[i + c][j + c] != "--":
                            break
                    for c in range(0, min(i, 8 - j)):
                        sqs_covered[i - c][j + c] += start[0]
                        if self.board[i - c][j + c] != "--":
                            break
                    for c in range(0, min(8 - i, j)):
                        sqs_covered[i + c][j - c] += start[0]
                        if self.board[i + c][j - c] != "--":
                            break
                    for c in range(0, min(i, j)):
                        sqs_covered[i - c][j - c] += start[0]
                        if self.board[i - c][j - c] != "--":
                            break
                if start[1] == "N":
                    try:
                        sqs_covered[i + 2][j + 1] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i - 2][j + 1] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i - 2][j - 1] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i + 2][j - 1] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i + 1][j + 2] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i + 1][j - 2] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i - 1][j + 2] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i - 1][j + 2] += start[0]
                    except IndexError:
                        pass
                if start[1] == "K":
                    try:
                        sqs_covered[i + 1][j + 1] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i + 1][j] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i + 1][j - 1] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i][j - 1] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i - 1][j - 1] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i - 1][j] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i - 1][j + 1] += start[0]
                    except IndexError:
                        pass
                    try:
                        sqs_covered[i][j + 1] += start[0]
                    except IndexError:
                        pass

        for i, x in enumerate(self.board):
            for j, y in enumerate(x):
                if sqs_covered[i][j].count("w") >= 1 and sqs_covered[i][j].count("b") >= 1:
                    sqs_covered[i][j] = "None"
        print(sqs_covered)
        return sqs_covered

    def is_valid(self, move):
        start_row, start_col, end_row, end_col, = move.start_row, move.start_col, move.end_row, move.end_col
        start, end = move.pieceMoved, move.pieceCaptured

        if (start_row, start_col) == (end_row, end_col):
            return False, -1

        if self.whiteToMove:
            if start[0] != "w":
                return False, -1
        else:
            if start[0] != "b":
                return False, -1

        if end != "--":
            if start[0] == end[0]:
                return False, -1
            if end[1] == "K":
                return False, -1

        x, y = end_col - start_col, end_row - start_row
        if start[1] == "P":
            if abs(x) >= 2 or abs(y) >= 3:
                return False, -1

            if (start[0] == "w" and y >= 0) or (start[0] == 'b' and y <= 0):
                return False, -1

            if abs(x) == 1 and abs(y) == 1:
                if end == "--":
                    enpassant = self.board[start_row][end_col]
                    if enpassant == "--" or enpassant[1] != "P" or enpassant[0] == start[0] or enpassant != \
                            self.moveLog[-1].pieceMoved:
                        return False, -1
                    if start_row != 3 and start_row != 4:
                        return False, -1
                    if start_row == 3 and enpassant[0] != "b":
                        return False, -1
                    if start_row == 4 and enpassant[0] != "w":
                        return False, -1
                    if start_row != 3 and start_row != 4:
                        return False, -1
                    return True, 1
            else:
                if end != "--":
                    return False, -1

            if abs(y) == 2:
                if start_row != 1 and start_row != 6:
                    return False, -1
                if start_row == 1 and start[0] != "b":
                    return False, -1
                if start_row == 6 and start[0] != "w":
                    return False, -1

        if start[1] == "R":
            if x != 0 and y != 0:
                return False, -1
            if y == 0:
                for i in range(1, abs(x)):
                    if self.board[start_row][start_col + i * int(x / abs(x))] != "--":
                        return False, -1
            if x == 0:
                for i in range(1, abs(y)):
                    if self.board[start_row + i * int(y / abs(y))][start_col] != "--":
                        return False, -1

        if start[1] == "B":
            if abs(x) != abs(y):
                return False, -1
            for i in range(1, abs(x)):
                if self.board[start_row + i * int(y / abs(y))][start_col + i * int(x / abs(x))] != "--":
                    return False, -1

        if start[1] == "N":
            if not ((abs(x) == 2 and abs(y) == 1) or (abs(x) == 1 and abs(y) == 2)):
                return False, -1

        if start[1] == "Q":
            if y == 0:
                for i in range(1, abs(x)):
                    if self.board[start_row][start_col + i * int(x / abs(x))] != "--":
                        return False, -1
            elif x == 0:
                for i in range(1, abs(y)):
                    if self.board[start_row + i * int(y / abs(y))][start_col] != "--":
                        return False, -1
            elif abs(x) == abs(y):
                for i in range(1, abs(x)):
                    if self.board[start_row + i * int(y / abs(y))][start_col + i * int(x / abs(x))] != "--":
                        return False, -1
            else:
                return False, -1

        if start[1] == "K":
            is_castle = False
            if abs(x) > 1 or abs(y) > 1:
                if abs(x) == 2 and abs(y) == 0:
                    is_castle = True
                else:
                    return False, -1
            sqs_covered = self.get_sq_covered()
            if sqs_covered[end_row][end_col] == "None" or sqs_covered[end_row][end_col] != start[0]:
                return False, -1

        return True, 0


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.board = board
        self.pieceMoved = board[self.start_row][self.start_col]
        self.pieceCaptured = board[self.end_row][self.end_col]

    def get_rank_file(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)


#####


WW = WH = 512
SQ_Size = WH // 8
FPS = 15
IMAGES = {}


def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bP", "wP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN",
              "wR"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_Size, SQ_Size))


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [(235, 235, 208), (119, 148, 85)]
    for r in range(8):
        for c in range(8):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_Size, r * SQ_Size, SQ_Size, SQ_Size))


def draw_pieces(screen, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_Size, r * SQ_Size, SQ_Size, SQ_Size))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WW, WH))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = GameState()
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // SQ_Size
                row = location[1] // SQ_Size
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    move = Move(player_clicks[0], player_clicks[1], gs.board)
                    is_valid = gs.is_valid(move)
                    if is_valid[0]:
                        gs.make_move(move, is_valid[1])
                        print(move.get_chess_notation())
                    else:
                        print("Invalid!!")

                    sq_selected = ()
                    player_clicks = []

        draw_game_state(screen, gs)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
