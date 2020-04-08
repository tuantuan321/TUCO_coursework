import random
import math
import numpy as np
import numbers

def fitness_calculation(rfca):
    attrLen = 0
    tranLen = 0
    tranLen, attrLen = rfca_evaluation(rfca)
    tranLen = tranLen + 1
    print('tranLen = ' + str(tranLen))
    print('attrLen = ' + str(attrLen))
    return tranLen, attrLen

def rfca_evaluation(rfca):
    aCount = 0
    tCount = 0
    attractor_found = False
    rfcaAll = np.zeros((50, 25))

    rfcaNew = []
    while (attractor_found == False):

        # before each loop, clear rfcaNew
        if (len(rfcaNew) != 0):
            for p in range(25):
                rfcaNew.pop()
        updateNum = 0

        # update node 1
        updateNum = rfca_rule(rfca[0], rfca[24], rfca[1])
        rfcaNew.append(updateNum)

        # update node 2 - 24
        for i in range(1, 24):
            updateNum = rfca_rule(rfca[i], rfca[i - 1], rfca[i + 1])
            rfcaNew.append(updateNum)

        #update node 25
        updateNum = rfca_rule(rfca[24], rfca[23], rfca[0])
        rfcaNew.append(updateNum)

        for i in range(25):
            rfca[i] = rfcaNew[i]

        lens = len(rfcaAll)

        # compare the latest rfca individual with the privous ones
        for i in range(lens):
            rfca_find_same = True
            for j in range(25):
                if (int(rfcaAll[i][j]) != rfcaNew[j]):
                    rfca_find_same = False
            if (rfca_find_same == True):
                attractor_found = True
                aCount = tCount - i - 1

        for i in range(25):
            rfcaAll[tCount][i] = rfcaNew[i]

        tCount = tCount + 1

        #print(rfcaAll)
        #print('attractor length = ' + str(attrCount))

    return  tCount, aCount

# num1 is the node itself
# num2, 3 are the neighboring nodes
def rfca_rule(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        # input the left side numbers
        # right side number is the output
        000: 1,
        # 001
        1: 0,
        # 010
        10: 1,
        100: 1,
        # 011
        11: 0,
        101: 1,
        110: 0,
        111: 1,
    }

    return rules.get(inputNum, None)

def main():

    rfcaInitial = []
    rfcaFinal = []

    # for testing purpose!!!
    for i in range(1, 26):
        num = np.random.randint(0, 2)
        rfcaInitial.append(num)

    #print(rfcaInitial)
    a = fitness_calculation(rfcaInitial)

    #b = rfca_rule(0, 1, 0)
    #c = rfca_rule(1, 1, 1)
    #print('b = ' + str(b))
    #print('c = ' + str(c))


if __name__ == '__main__':
    main()
