import random


def transposing(grid: list):
    """Транспонирует матрицу"""
    size = len(grid)
    res = [[grid[i][j] for i in range(size)] for j in range(size)]
    return res


def line_swap(grid: list, area: int, l1: int, l2: int):
    """Меняет местами две строки в зоне
    :param
    grid - таблица с судоку
    area - порядковый номер строки из малых квадратов
    l1 - номер первой строки
    l2 - номер второй строки"""
    size = int(len(grid)**0.5)
    grid[size * area + l1], grid[size * area + l2] = grid[size * area + l2], grid[size * area + l1]
    return grid

def line_area_swap(grid: list, area1: int, area2: int):
    """Меняет местами две строки из малых квадратов
    :param
    grid - таблица с судоку
    area1 - номер первой строки
    area2 - номер второй строки"""
    size = int(len(grid)**0.5)
    for i in range(size):
        grid[size*area1 + i], grid[size*area2 + i] = grid[size*area2 + i], grid[size*area1 + i]
    return grid

def randomize_grid(grid):
    """Перемешивает таблицу с судоку случайным образом, сохраняя её правильность"""
    ng = grid
    size = int(len(grid)**0.5)
    ar1, ar2 = random.randint(0, size - 1), random.randint(0, size - 1)
    line_area_swap(ng, ar1, ar2)
    ng = transposing(ng)
    ar1, ar2 = random.randint(0, size - 1), random.randint(0, size - 1)
    line_area_swap(ng, ar1, ar2)
    for i in range(200):
        a = random.randint(0, size - 1)
        line1, line2 = random.randint(0, size - 1), random.randint(0, size - 1)
        while line2 == line1:
            line2 = random.randint(0, size - 1)
        line_swap(ng, a, line1, line2)
        ng = transposing(ng)
    return ng


def crossed(x, y, size, grid):
    """Определяет, какие элементы находятся в одной строке, столбце, малом квадрате с данной клеткой
    :param
    x - координата по вертикали
    y - координата по горизонтали
    size - размер малых квадратов
    grid - таблица с судоку"""
    cr = set()
    for i in range(size ** 2):
        cr.add(grid[x][i])
        cr.add(grid[i][y])
    for i in range(x // size * size, (x // size + 1) * size):
        for j in range(y // size * size, (y // size + 1) * size):
            cr.add(grid[i][j])
    cr.discard(grid[x][y])
    cr.discard(0)
    return cr


def crossedlc(x, y, size, x1, y1, grid):
    """Находит числа, находящиеся в одной строке или столбце с заданным, не учитывая указанную клетку
    :param
    x, y - координаты числа
    size - размер малого кадрата
    x1, y1  - координаты не учитываемого числа
    grid - таблица с судоку"""
    cr = set()
    for i in range(size ** 2):
        if not i == y1:
            cr.add(grid[x][i])
        if not i == x1:
            cr.add(grid[i][y])
    cr.discard(0)
    return cr


def lonely(x, y, size, grid):
    """Проверяет, является ли число в указанная клетка единственно возможной позицией в данном квадрате для числа,
    стоящего в ней
    :param
    x, y - координаты клетки
    size - размер малого квадрата
    grid - таблица с судоку"""
    lon = True
    for i in range(x // size * size, (x // size + 1) * size):
        for j in range(y // size * size, (y // size + 1) * size):
            if grid[i][j] == 0:
                if not grid[x][y] in crossedlc(i, j, size, x, y, grid):
                    lon = False
    return lon


def generate(size: int, difficulty: int):
    """Создает случайное судоку заданного размера и сложности"""
    basic_grid_3 = [[5, 6, 4, 9, 1, 8, 3, 2, 7],
                    [2, 3, 1, 4, 7, 5, 8, 9, 6],
                    [7, 8, 9, 3, 2, 6, 1, 4, 5],
                    [9, 4, 2, 5, 3, 7, 6, 8, 1],
                    [3, 1, 8, 6, 4, 9, 5, 7, 2],
                    [6, 7, 5, 1, 8, 2, 9, 3, 4],
                    [4, 5, 3, 2, 9, 1, 7, 6, 8],
                    [1, 2, 7, 8, 6, 3, 4, 5, 9],
                    [8, 9, 6, 7, 5, 4, 2, 1, 3]]
    basic_grid_4 = [[2, 1, 13, 14, 8, 10, 9, 5, 16, 6, 3, 15, 12, 7, 11, 4],
                    [6, 3, 10, 9, 7, 15, 4, 12, 14, 5, 11, 1, 2, 13, 8, 16],
                    [15, 5, 4, 7, 11, 13, 3, 16, 2, 8, 9, 12, 1, 10, 14, 6],
                    [8, 11, 12, 16, 1, 14, 2, 6, 13, 4, 10, 7, 15, 5, 9, 3],
                    [16, 2, 3, 10, 9, 4, 8, 13, 6, 15, 12, 14, 11, 1, 7, 5],
                    [14, 4, 8, 12, 16, 6, 15, 7, 11, 1, 5, 10, 13, 3, 2, 9],
                    [13, 9, 11, 5, 2, 1, 12, 14, 3, 7, 8, 16, 6, 4, 15, 10],
                    [7, 6, 15, 1, 5, 3, 10, 11, 9, 2, 4, 13, 14, 12, 16, 8],
                    [12, 14, 5, 3, 6, 7, 16, 2, 1, 11, 15, 8, 10, 9, 4, 13],
                    [9, 15, 7, 2, 10, 11, 1, 4, 12, 13, 6, 3, 16, 8, 5, 14],
                    [11, 8, 16, 13, 3, 12, 5, 15, 10, 9, 14, 4, 7, 2, 6, 1],
                    [4, 10, 1, 6, 13, 9, 14, 8, 7, 16, 2, 5, 3, 11, 12, 15],
                    [10, 7, 2, 11, 15, 5, 6, 3, 4, 14, 1, 9, 8, 16, 13, 12],
                    [1, 12, 6, 4, 14, 16, 7, 9, 8, 10, 13, 11, 5, 15, 3, 2],
                    [5, 16, 9, 8, 12, 2, 13, 1, 15, 3, 7, 6, 4, 14, 10, 11],
                    [3, 13, 14, 15, 4, 8, 11, 10, 5, 12, 16, 2, 9, 6, 1, 7]]
    if size == 3:
        sudoku = randomize_grid(basic_grid_3)
    else:
        sudoku = randomize_grid(basic_grid_4)
    pot = []
    for x in range(size**2):
        pot.append([])
        for y in range(size**2):
            pot[x].append(crossed(x,y,size, sudoku))
    n = size**4
    if size == 3:
        difficulty = int(0.6*n - n/20*difficulty)
    else:
        difficulty = int(0.7 * n - n / 20 * difficulty)
    while n > difficulty:
        x, y = random.randint(0, size**2-1), random.randint(0, size**2-1)
        if len(pot[x][y]) == 8 and sudoku[x][y] != 0:
            sudoku[x][y] = 0
            for i in range(size**2):
                pot[x][i] = crossed(x, i, size, sudoku)
                pot[i][y] = crossed(i, y, size, sudoku)
            for i in range(x//size*size, (x//size+1)*size):
                for j in range(y // size * size, (y // size + 1) * size):
                    pot[i][j] = crossed(i, j, size, sudoku)
            n -= 1
        if lonely(x, y, size, sudoku) and sudoku[x][y] != 0:
            sudoku[x][y] = 0
            for i in range(size ** 2):
                pot[x][i] = crossed(x, i, size, sudoku)
                pot[i][y] = crossed(i, y, size, sudoku)
            for i in range(x // size * size, (x // size + 1) * size):
                for j in range(y // size * size, (y // size + 1) * size):
                    pot[i][j] = crossed(i, j, size, sudoku)
            n -= 1
    return sudoku


def checking(grid):
    """Проверяет верно ли заполнен квадрат.
    Если верно, возвращает True, иначе - координаты последней по счету найденной ошибки и код ошибки
    0 - неверно заполнена строка
    1 - неверно заполнен столбец
    2 - неверно заполнен малый квадрат
    3 - в ячейке нет значения"""
    size = len(grid)
    check = True
    mistake = [0, 0, -1]
    for i in range(size):
        for j in range(size):
            for i1 in range(size):
                if grid[i1][j] == grid[i][j] and i1 != i:
                    check = False
                    mistake = [i, j, 0]
            for j1 in range(size):
                if grid[i][j1] == grid[i][j] and j1 != j:
                    check = False
                    mistake = [i, j, 1]
    size = int(size**0.5)
    for i in range(size):
        for j in range(size):
            sq = set()
            for k in range(size):
                sq.update(set(grid[i*size+k][j*size:j*size+size]))
            if len(sq) != size**2:
                check = False
                mistake = [i, j, 2]
    for i in range(size**2):
        for j in range(size**2):
            if grid[i][j] == None:
                mistake = [i, j, 3]
                check = False
    if check == True:
        return check
    else:
        return mistake
