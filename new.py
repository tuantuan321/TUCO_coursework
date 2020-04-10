import random
import math
import numpy as np
import numbers
import multiprocessing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

archives = np.zeros((100, 2))
archive_count = 0
THRESHOLD = 0

def fitness_calculation(rfca):
    attrLen = 0
    tranLen = 0
    tranLen, attrLen = rfca_evaluation(rfca)
    tranLen = tranLen + 1

    #print('tranLen = ' + str(tranLen))
    #print('attrLen = ' + str(attrLen))
    #print('-------------------')
    archive(rfca, tranLen, attrLen)

    fitness = novel_cal(tranLen, attrLen)

    #print(fitness)
    return fitness,

def rfca_evaluation(rfca):
    aCount = 0
    tCount = 0
    attractor_found = False
    # assume that the transient length is less than 200
    rfcaAll = np.zeros((300, 25))

    rfcaNew = []
    while (attractor_found == False):

        # before each loop, clear rfcaNew
        if (len(rfcaNew) != 0):
            for p in range(25):
                rfcaNew.pop()
                updateNum = 0

        # update node 1
        updateNum = rfca_rule2(rfca[0], rfca[24], rfca[1])
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
            if (i == 1) or (i == 3) or (i == 5) or (i == 9):
                updateNum = rfca_rule3(num1, num2, num3)
                #print("Update = " + str(updateNum))
            else:
                if (i == 2) or (i == 19) or (i == 6) or (i == 13):
                    updateNum = rfca_rule6(num1, num2, num3)
                else:
                    if (i == 12) or (i == 23) or (i == 16):
                        updateNum = rfca_rule5(num1, num2, num3)
                    else:
                        if (i == 11) or (i == 8) or (i == 21):
                            updateNum = rfca_rule7(num1, num2, num3)
                        else:
                            if ( i == 17) or (i == 4) or (i == 15):
                                updateNum = rfca_rule2(num1, num2, num3)
                            else:
                                if (i == 18) or (i == 14):
                                    updateNum = rfca_rule8(num1, num2, num3)
                                else:
                                    if (i == 7) or (i == 21):
                                        updateNum = rfca_rule(num1, num2, num3)
                                    else:
                                        updateNum = rfca_rule9(num1, num2, num3)

            rfcaNew.append(updateNum)

        #update node 25
        updateNum = rfca_rule4(rfca[24], rfca[23], rfca[0])
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


###################### RFCA rules ########################
# num1 is the node itself
# num2, 3 are the neighboring nodes
def rfca_rule(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        # left side => input
        # right side => output
        # 000
        0: 1,
        # 001
        1: 1,
        # 010
        10: 0,
        100: 0,
        # 011
        11: 1,
        101: 0,
        110: 0,
        111: 1,
    }
    return rules.get(inputNum, None)

def rfca_rule2(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        0: 1,
        1: 0,
        10: 1,
        100: 1,
        11: 1,
        101: 1,
        110: 0,
        111: 1,
    }
    return rules.get(inputNum, None)

def rfca_rule3(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        0: 0,
        1: 0,
        10: 1,
        100: 0,
        11: 1,
        101: 0,
        110: 1,
        111: 0,
    }
    return rules.get(inputNum, None)

def rfca_rule4(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        0: 1,
        1: 0,
        10: 1,
        100: 1,
        11: 1,
        101: 1,
        110: 0,
        111: 0,
    }
    return rules.get(inputNum, None)

def rfca_rule5(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        0: 0,
        1: 1,
        10: 0,
        100: 1,
        11: 0,
        101: 1,
        110: 1,
        111: 0,
    }
    return rules.get(inputNum, None)

def rfca_rule6(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        0: 0,
        1: 1,
        10: 0,
        100: 0,
        11: 0,
        101: 0,
        110: 1,
        111: 1,
    }
    return rules.get(inputNum, None)

def rfca_rule7(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        0: 1,
        1: 0,
        10: 0,
        100: 0,
        11: 0,
        101: 1,
        110: 1,
        111: 1,
    }
    return rules.get(inputNum, None)

def rfca_rule8(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        0: 1,
        1: 1,
        10: 1,
        100: 0,
        11: 1,
        101: 0,
        110: 0,
        111: 1,
    }
    return rules.get(inputNum, None)

def rfca_rule9(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        0: 0,
        1: 1,
        10: 1,
        100: 1,
        11: 1,
        101: 0,
        110: 0,
        111: 0,
    }
    return rules.get(inputNum, None)

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
        for i in range(archive_count + 1):
            if (transient != archives[i][0]) and (attractor == archives[i][1]):
                novelScore = novelScore + 1
            if (transient == archives[i][0]) and (attractor == archives[i][1]):
                novelScore = novelScore - 10
            if (transient == archives[i][0]) and (attractor != archives[i][1]):
                novelScore = novelScore + 1
    if (archive_count == 0):
        novelScore = 0
    return novelScore

# archive
def archive(individual, transient, attractor):
    global archives
    global THRESHOLD
    global archive_count

    meet_threshold = True
    if (archive_count > 0):
        for i in range(archive_count + 1):
            if (transient == archives[i][0]) and (attractor == archives[i][1]):
                meet_threshold = False

    if (meet_threshold == True):
        archives[archive_count][0] = transient
        archives[archive_count][1] = attractor
        archive_count = archive_count + 1

    if (archive_count == 0):
        archives[archive_count][0] = transient
        archives[archive_count][1] = attractor
        archive_count = archive_count + 1

################ Main Generation Settings ################
IND_SIZE = 25
INT_MIN = 0
INT_MAX = 1
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

## Multiprocessing
## code from: https://deap.readthedocs.io/en/master/tutorials/basic/part4.html
pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

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
        print("Current Generation: %i" %gen)

        # select next generation
        offspring = list(map(toolbox.clone, population))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            select_cross(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            population[:] = offspring

        fits = [ind.fitness.values[0] for ind in population]

        length = len(population)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Max: %s" % max(fits))
        print("  Avg: %s " % mean)
        print("  Std: %s " % std)

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

    print("  Archived Details")
    print(archives)
    #print(archives)
    return population

if __name__ == '__main__':
    main()
