import random
import math
import numpy as np
import numbers

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

def fitness_calculation(rfca):
    attrLen = 0
    tranLen = 0
    tranLen, attrLen = rfca_evaluation(rfca)
    tranLen = tranLen + 1
    print('tranLen = ' + str(tranLen))
    print('attrLen = ' + str(attrLen))
    print('-------------------')

    return tranLen,

def rfca_evaluation(rfca):
    aCount = 0
    tCount = 0
    attractor_found = False
    rfcaAll = np.zeros((150, 25))

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
            if (i == 2) or (i == 4) or (i == 7) or (i == 14) or (i == 17):
                updateNum = rfca_rule(rfca[i], rfca[i - 1], rfca[i + 1])
            else:
                updateNum = rfca_rule3(rfca[i], rfca[i - 1], rfca[i + 1])
            rfcaNew.append(updateNum)

        #update node 25
        updateNum = rfca_rule2(rfca[24], rfca[23], rfca[0])
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
def rfca_rule(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        000: 1,
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

# num1 is the node itself
# num2, 3 are the neighboring nodes
def rfca_rule2(num1, num2, num3):
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
        11: 1,
        101: 1,
        110: 0,
        111: 1,
    }
    return rules.get(inputNum, None)

def rfca_rule3(num1, num2, num3):
    inputNum = num1 * 100 + num2 * 10 + num3
    rules = {
        000: 0,
        # 001
        1: 0,
        # 010
        10: 1,
        100: 0,
        # 011
        11: 1,
        101: 0,
        110: 1,
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
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)

def main():

    global toolbox
    global IND_SIZE
    #rfcaInitial = []
    #rfcaFinal = []

    # deap parameters
    NGEN = 1
    CXPB = 0.5
    MUTPB = 0.7
    POP = 30

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
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

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

    return population

if __name__ == '__main__':
    main()
