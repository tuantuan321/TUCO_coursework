# TUCO Assessment
# Question 1 Source Code
# Used DEAP as GA library

import random
import math
import numpy as np
import numbers
import xlwt

from deap import base
from deap import creator
from deap import tools

archives = np.zeros((1000, 2))
rule_set = np.zeros((256, 8))
archive_count = 0
rfcaIn = []
HISTORY_AMOUNT = 2000
cal_history = np.zeros((HISTORY_AMOUNT, 10))
history_count = 0

def fitness_calculation(ruleNum):
    attrLen = 0
    tranLen = 0
    tranLen, attrLen = rfca_evaluation(ruleNum)
    tranLen = tranLen + 1

    #print('tranLen = ' + str(tranLen))
    #print('attrLen = ' + str(attrLen))
    #print('-------------------')
    archive(ruleNum, tranLen, attrLen)

    fitness = novel_cal(tranLen, attrLen)

    #print(fitness)
    return fitness,

def rfca_generate():
    global rfcaIn
    for j in range(25):
        rfcaIn.append(random.randint(0, 1))

def rfca_evaluation(ruleNum):
    global cal_history
    global history_count

    aCount = 0
    tCount = 0
    attractor_found = False
    # assume that the transient length is less than 320
    rfcaAll = np.zeros((320, 25))
    rfca = []
    rfcaNew = []

    # calculate history
    calculated = False
    historyNum = 0
    for i in range(history_count + 1):
        temp_bool = True
        for j in range(8):
            if (cal_history[i][j] != ruleNum[j]):
                temp_bool = False
        if (temp_bool == True):
            calculated = True


    # use history to store calculated fitness
    # optimize purpose
    if (calculated == True):
        #print("history used")
        return cal_history[historyNum][8], cal_history[historyNum][9]

    for i in range(25):
        rfca.append(rfcaIn[i])

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
            #print("i = " + str(i))
            #print(num1)
            #print(num2)
            #print(num3)
            updateNum = rfca_rule(ruleNum[i], num1, num2, num3)

            rfcaNew.append(updateNum)

        #update node 25
        updateNum = rfca_rule(ruleNum[24], rfca[24], rfca[23], rfca[0])
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

        if (tCount > 300):
            tCount = 0
            attractor_found = True
            aCount = 0
        #print(rfcaAll)
        #print('attractor length = ' + str(attrCount))

    if (history_count < HISTORY_AMOUNT - 1) and (calculated == False):
        history_count = history_count + 1
        for i in range(8):
            cal_history[history_count][i] = ruleNum[i]
        cal_history[history_count][8] = tCount
        cal_history[history_count][9] = aCount
    #print(cal_history[history_count - 1])
    #print(history_count)
    return  tCount, aCount

###################### RFCA rules generator########################
# num1 is the node itself
# num2, 3 are the neighboring nodes
def rfca_rule(rule, num1, num2, num3):
    global rule_set
    inputNum = num1 * 100 + num2 * 10 + num3
    # receive rule from rule_generate function

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

##########################################################

def select_cross(ind1, ind2):
    # calculate fitness for each individual
    fitness1 = fitness_calculation(ind1)
    fitness2 = fitness_calculation(ind2)

    # compare
    if fitness1 >= fitness2:
        winner = ind1
        loser = ind2
    else:
        winner = ind2
        loser = ind1

    # infect loser
    loser = infect(winner, loser)
    return winner, loser

def infect(winner, loser):
    toolbox.mate(winner, loser)
    return loser

# calculate novel rate
def novel_cal(transient, attractor):
    novelScore = 0

    if (archive_count > 0):
        tempScore = 0
        for i in range(archive_count + 1):
            if (transient != archives[i][0]) and (attractor == archives[i][1]):
                tempScore = tempScore + 1
            if (transient == archives[i][0]) and (attractor == archives[i][1]):
                tempScore = tempScore - archive_count
            if (transient == archives[i][0]) and (attractor != archives[i][1]):
                tempScore = tempScore + 1
            if (transient != archives[i][0]) and (attractor != archives[i][1]):
                tempScore = tempScore + 2
            novelScore = tempScore/archive_count
    if (archive_count == 1):
        novelScore = 2
    #print(archive_count)
    print(novelScore)
    return novelScore

# archive
def archive(individual, transient, attractor):
    global archives
    global archive_count

    if (archive_count == 1):
        archives[archive_count][0] = transient
        archives[archive_count][1] = attractor
        archive_count = archive_count + 1

    meet_threshold = True
    if (archive_count > 0):
        for i in range(archive_count + 1):
            if (transient == archives[i][0]) and (attractor == archives[i][1]):
                meet_threshold = False

    if (meet_threshold == True):
        archives[archive_count][0] = transient
        archives[archive_count][1] = attractor
        archive_count = archive_count + 1

################ Main Generation Settings ################
IND_SIZE = 25
INT_MIN = 0
INT_MAX = 255

# initial toolbox
toolbox = base.Toolbox()

# create individual
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox.register("attr_int", random.randint, INT_MIN, INT_MAX)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_int, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", fitness_calculation)
toolbox.register("mate", tools.cxTwoPoint)
#toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

def save(data, path):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok = True)
    [h, l] = data.shape
    for i in range(h):
        for j in range(l):
            sheet1.write(i, j, data[i, j])
    f.save(path)

def main():

    global toolbox
    global IND_SIZE
    global archives
    global archive_count

    #rfcaInitial = []
    #rfcaFinal = []

    # deap parameters
    NGEN = 5
    POP = 100
    MUTPB = 0.1
    CXPB = 0.2

    # generate rules
    rule_generate()
    #print(rule_set)

    rfca_generate()

    population = toolbox.population(n = POP)

    # evaluate the population
    fitnesses = map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    # extract all the fitnesses
    fits = [ind.fitness.values[0] for ind in population]

    gen = 0

    # start generation
    while gen < NGEN:
        gen = gen + 1
        print("Generation: %i Processing" %gen)

        # select next generation
        #offspring = toolbox.select(population, len(population))
        #offspring = list(map(toolbox.clone, offspring))
        offspring = list(map(toolbox.clone, population))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                select_cross(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring

        fits = [ind.fitness.values[0] for ind in population]

        length = len(population)

    # for testing purpose!!!
    #for i in range(1, 26):
    #    num = np.random.randint(0, 2)
    #    rfcaInitial.append(num)

    #print(rfcaInitial)
    #a = fitness_calculation(rfcaInitial)

    #b = rfca_rule(0, 1, 0)
    #c = rfca_rule(1, 1, 1)
    #print('b = ' + str(b))
    #print('c = ' + str(c))

    print("  Archived Individual: %s" % archive_count)

    #print("  Archived Details")
    print(archives)
    save(archives, '1.xls')

    return population

if __name__ == '__main__':
    main()
