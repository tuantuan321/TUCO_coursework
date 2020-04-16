# TUCO Assessment
# Question 1 Source Code Part 2
# For quation 1.6

import random
import math
import numpy as np
import numbers
import xlwt
from matplotlib import pyplot as plt

archive_count = 0
rule_set = np.zeros((256, 8))
evaluate_record = np.zeros((600, 25))
evaluateNum = 0
TRAN_LIMIT = 350

def evaluate_calculation(ruleNum, rfca):
    attrLen = 0
    tranLen = 0
    tranLen, attrLen = rfca_evaluation(ruleNum, rfca)

    print('Transient Length: ' + str(tranLen))
    print('Attractor Length: ' + str(attrLen))

def rfca_evaluation(ruleNum, rfca):
    global evaluateNum
    global TRAN_LIMIT

    aCount = 0
    tCount = 0
    attractor_found = False
    # assume that the transient length is less than 320
    rfcaAll = np.zeros((TRAN_LIMIT, 25))
    rfcaNew = []

    while (attractor_found == False):

        # before each loop, clear rfcaNew
        if (len(rfcaNew) != 0):
            for p in range(25):
                rfcaNew.pop()
                updateNum = 0

        #update node 1
        updateNum = rfca_rule(ruleNum[0], rfca[0], rfca[24], rfca[1])
        rfcaNew.append(updateNum)

        # update node 2 - 24
        for i in range(1, 24):
            num1 = rfca[i]
            num2 = rfca[i - 1]
            num3 = rfca[i + 1]
            updateNum = rfca_rule(ruleNum[i], num1, num2, num3)

            rfcaNew.append(updateNum)

        #update node 25
        updateNum = rfca_rule(ruleNum[24], rfca[24], rfca[23], rfca[0])
        rfcaNew.append(updateNum)

        for i in range(25):
            rfca[i] = rfcaNew[i]

        print(rfca)
        lens = len(rfcaAll)

        # compare the latest rfca individual with the privous ones
        for i in range(lens):
            rfca_find_same = True
            for j in range(25):
                if (int(rfcaAll[i][j]) != rfcaNew[j]):
                    rfca_find_same = False
            if (rfca_find_same == True):
                aCount = tCount - i
                attractor_found = True

        for i in range(25):
            rfcaAll[tCount][i] = rfcaNew[i]

        tCount = tCount + 1

        if (tCount > TRAN_LIMIT):
            tCount = 0
            attractor_found = True
            aCount = 0

        for i in range(25):
            evaluate_record[evaluateNum][i] = rfca[i]

        evaluateNum = evaluateNum + 1

    tCount = tCount - aCount

    return  tCount, aCount


###################### RFCA rules generator########################
# num1 is the node itself
# num2, 3 are the neighboring nodes
def rfca_rule(rule, num1, num2, num3):
    global rule_set
    inputNum = num1 * 100 + num2 * 10 + num3

    ru0 = rule_set[rule][0]
    ru1 = rule_set[rule][1]
    ru2 = rule_set[rule][2]
    ru3 = rule_set[rule][3]
    ru4 = rule_set[rule][4]
    ru5 = rule_set[rule][5]
    ru6 = rule_set[rule][6]
    ru7 = rule_set[rule][7]

    rules = {
        # left side => input
        # right side => output
        # 000
        0: ru0,
        # 001
        1: ru1,
        # 010
        10: ru2,
        100: ru3,
        # 011
        11: ru4,
        101: ru5,
        110: ru6,
        111: ru7,
    }

    return rules.get(inputNum, None)

def rule_generate():
    global rule_set
    count = 0
    for k in range(4):
        for k2 in range(4):
            for k3 in range(4):
                for k4 in range(4):
                    rule_set[count][0], rule_set[count][1] = cal_sec(k)
                    rule_set[count][2], rule_set[count][3] = cal_sec(k2)
                    rule_set[count][4], rule_set[count][5] = cal_sec(k3)
                    rule_set[count][6], rule_set[count][7] = cal_sec(k4)
                    count = count + 1

def cal_sec(num):
    if (num == 0):
        return 0, 0
    if (num == 1):
        return 0, 1
    if (num == 2):
        return 1, 0
    if (num == 3):
        return 1, 1

def save(data, path):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok = True)
    [h, l] = data.shape
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, data[i, j])
    f.save(path)

def main():

    rule_generate()

    rfca =[1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
    # 63 - 120
    rfcaNum = [198,207,113,225,142,27,242,185,110,145,101,10,213,241,140,212,210,95,245,132,173,160,196,183,185]
    # 9 - 280
    #rfcaNum = [198,207,113,225,142,27,159,133,119,145,101,10,213,241,140,212,43,95,245,132,173,241,196,183,86]
    # 1 - 24
    #rfcaNum = [198,207,113,	225, 142, 27,159,211,119,145,101 ,10 ,213,241,140,1,43,95,245,132,181,241,196,183,37]
    # 26 - 140
    #rfcaNum = [176,207,113,225,142,27,159,1,119,177, 101, 10,213, 241,140,146,43 ,95,245,132,173 ,241,196 ,86,86]
    evaluate_calculation(rfcaNum, rfca)

    plt.imsave('w.png', evaluate_record, cmap='gray')
    save(evaluate_record, 'record.xls')


if __name__ == '__main__':
    main()
