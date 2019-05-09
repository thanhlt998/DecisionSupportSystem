import numpy
import connect_db as con
from settings import TOPSIS_WEIGHT, NO_ATTRIBUTES


def sumSq(row):
    sum = 0
    for i in row:
        sum += i * i
    return numpy.sqrt(sum)


def arrSumSq(matrix):
    arrSum = []
    for row in matrix:
        arrSum.append(sumSq(row))
    return arrSum


def topsis(matrix, optionNum, w, wNum):
    # Step 1,2
    arrSum = arrSumSq(numpy.transpose(matrix))

    for i in range(wNum):
        for j in range(optionNum):
            matrix[j][i] = w[i] * matrix[j][i] / arrSum[i]

    # Step 3
    aP = []
    aM = []
    for row in numpy.transpose(matrix):
        aP.append(numpy.amax(row))
        aM.append(numpy.amin(row))

    # Step 4
    sP = []
    sM = []
    for row in matrix:
        tempP = []
        tempM = []
        for i in range(len(row)):
            tempP.append(row[i] - aP[i])
            tempM.append(row[i] - aM[i])
        sP.append(sumSq(tempP))
        sM.append(sumSq(tempM))

    # Step 5
    c = []
    for i in range(len(sP)):
        c.append(sM[i] / (sP[i] + sM[i]))

    return c


def bestPrice(matrix):
    # Price, area, floor, bedroom
    w = [0.4, 0.25, 0.15, 0.2]

    for i in range(len(matrix)):
        matrix[i][0] = 1. / matrix[i][0]

    return topsis(matrix, len(matrix), w, 4)


def bestArea(matrix):
    w = [0.3, 0.35, 0.1, 0.25]

    return topsis(matrix, len(matrix), w, 4)


# optionNum x wNum
# matrix = [[690, 3.1, 9, 7, 4],
#           [590, 3.9, 7, 6, 10],
#           [600, 3.6, 8, 8, 7],
#           [620, 3.8, 7, 10, 6],
#           [700, 2.8, 10, 4, 6],
#           [650, 4.0, 6, 9, 8]]
# print(type(matrix))
# matrix = con.turn_to_matrix()
# print(type(matrix))
# w = [0.3, 0.2, 0.2, 0.15]
# print(topsis(matrix, len(matrix), TOPSIS_WEIGHT, NO_ATTRIBUTES))
