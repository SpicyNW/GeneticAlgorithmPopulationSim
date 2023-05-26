# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:14:40 2022

CSC 4444: AI - Final Project
Genetic Algorithm Population Simulator

Author: Nick Williams
"""
import random


#------FUNCTIONS---------------------------------------------------------------


#WORLD GENERATOR: make a random world. Each index correlates with a certain world trait.
# 0 = vegetation density (1 means barely any plant life, 10 means a lot of plants)
# 1 = num of predators (1 means few predators, 10 means many predators)
# 2 = land mass coverage (1 means a lot of water, 10 means a lot of land)
# 3 = food scarcity (1 means food is abundant, 10 means food is sparse)
# 4 = temperature (1 is very hot, 10 is very cold)
def randWorld():
    traits = []
    for t in range(5):
        traits.append(random.randint(1, 10))
    return traits


#SINGLE ORGANISM GENERATOR: make a random individual whose genes do not sum up
#to more than 40. Each index correlates to a certain characteristic of the individual
# 0 = size (1 is small, 10 is large)
# 1 = mobility (1 is slow and stagnant, 10 is fast and agile)
# 2 = dehydration adaptations (1 needs water [like a fish], 10 doesn't rely on water as much [like a camel])
# 3 = socialization (1 is solitary, 10 is very social)
# 4 = cold tolerance (1 is not tolerant, 10 is very well equipped to deal with cold)
def randIndividual():
    numGenes = 5            #num of traits the individual has
    indiv = []
    vals = []
    #RANDOMLY GEN LIST OF NUMS THAT SUMS TO 40 OR LESS
    #generate 4 random nums
    for num in range(numGenes - 1):   
        vals.append((random.randint(1,10)))
    #generate the fifth random num
    #if the final val can be 10 without total exceeding 40 - use random num
    if sum(vals) <= 30:    
        vals.append(random.randint(1,10))
    else:
        finalVal = ((numGenes - 1) * 10) - sum(vals)    #if changing 40, change this
        vals.append(finalVal)
    #RANDOMLY ASSIGN THE RANDOM NUMBERS TO GENES OF INDIVIDUAL
    for x in range(len(vals)):
        toAdd = random.choice(vals)
        indiv.append(toAdd)
        vals.remove(toAdd)
    return indiv


#FITNESS FUNCTION: Takes in a world list and an individual specimen list
#Decides how well an individual is suited to the environment.
#Bigger fitness value means the individual is more fit.
def fitnessFunction(world, indiv):
    fitness = 0
    #loop thru individual, comparing personal traits to world traits
    for t in range(len(indiv)):
        #if a certain World trait is high - it must be adapted to
        if(world[t] >= 7):
            #if Indiv trait is greater than or equal to World trait, increase fitness
            if(indiv[t] >= world[t]):
                fitness += 10
            #else if Indiv trait is lower than World trait - 2, decrease fitness
            elif(indiv[t] <= (world[t] - 2)):
                fitness -= 5
                
        #if a certain World trait is mid - adaptations would be helpful, not necessary
        elif(world[t] >= 4):
            #if Indiv trait is greater than or equal to World trait, increase fitness
            if(indiv[t] >= world[t]):
                fitness += 5
            #else if Indiv trait is lower than World trait - 2, decrease fitness
            elif(indiv[t] <= (world[t] - 2)):
                fitness -= 3
        #if a certain trait has been adapted but isn't needed, decrease fitness
        if world[t] / indiv[t] <= 0.34:
            fitness -= 5
    return fitness


#GENETIC ALGORITHM: takes in a list of 5 nums that represent the traits of a world
#returns a list of individuals that are well suited to that world
def geneticAlgorithm(world):
    numGens = 100           #number of generations the algorithm will run for
    initialPopSize = 100    #number of individuals in the starting population
    initialPop = []

    #INITIAL POP---
    #randomly generate the initial population
    for indiv in range(initialPopSize):
        initialPop.append(randIndividual())
        
    #BEGIN GENETIC ALGORITHM
    for gen in range(numGens):
        
        #FITNESS---
        #calculate each individuals fitness to the world
        fitnessVals = []
        for i in range(len(initialPop)):
            fitness = fitnessFunction(world, initialPop[i])
            fitnessVals.append(fitness)
        #Deal with individuals with negative fitness
        positiveFitness = fitnessVals[:]
        for f in range(len(fitnessVals)):
            if fitnessVals[f] < 0:
                positiveFitness.remove(fitnessVals[f])
                fitnessVals[f] = 0              #set negative vals to 0 so they are not chosen
        fitnessTotal = sum(positiveFitness)     #reliable probability denominator
        #calc each individuals probability of reproducing
        reproductionPercentage = []
        for v in range(len(fitnessVals)):
            percentage = (fitnessVals[v] / fitnessTotal) * 100
            reproductionPercentage.append(percentage)
        
        #PARENT SELECTION---
        kids = []
        mostFit = []
        #Randomly choose parents based on probabilty weights
        mostFit = random.choices(initialPop, reproductionPercentage, k = 30)
        #nested for loops so that each individual makes two unique children 
        for mom in range(len(mostFit)):
            indivMom = mostFit[mom]
            for dad in range(len(mostFit)):
                child = []
                #make sure that an individual is not reproducing w themselves
                if mom != dad:          
                    indivDad = mostFit[dad]
                    #MAKE CHILD---
                    #pick crossover point - mom gives first 2 traits, dad gives last 3
                    for i in range(5):
                        if i < 2:
                            child.append(indivMom[i])
                        else:
                            child.append(indivDad[i])
                    kids.append(child)
                    
        #MUTATION---
        #potential for a random trait to mutate
        for kid in kids:
            mutationChance = random.randint(1, 100)
            if mutationChance <= 30:                    #percentage chance of mutation: Fun to change this number
                traitToChange = random.randint(0, 4)
                newTraitVal = random.randint(1, 10)
                kid[traitToChange] = newTraitVal
                
        initialPop = kids[:]
                
    return kids


#SURVIVAL RATE: takes in a world and a list of individual and determines the 
#percentage of individuals that would survive the world
def survivalRate(world, individuals):
    survivors = []
    for indiv in individuals:
        survive = True
        for char in range(len(indiv)):
            if indiv[char] < (world[char] - 1):
                survive = False
        if survive == True:
            survivors.append(indiv)
    survivalPercentage = round(((len(survivors) / len(individuals)) * 100), 2)
    
    return survivalPercentage


#INPUT CHECKER: checks the inputs to see if they are a number from 1 to 10
def checkCustomInputs(string):
    if string.isnumeric():
        if 1 <= int(string) and int(string) <= 10:
            return True
        else:
            print("please enter a number from 1 to 10")
            return False
    else:
        print("please enter a number from from 1 to 10")
        return False
        
        
#------MAIN--------------------------------------------------------------------


run = True
while run == True:
    customChoice = input("Would you like to create a custom world? (y/n)")
    customChoice = customChoice.lower()
    customWorld = []
    if "y" in customChoice:
        #zero trait
        check0 = False
        while check0 == False:
            vegDens = input("How much vegetation density? (scale of 1-10)")
            check0 = checkCustomInputs(vegDens)
        customWorld.append(int(vegDens))
        #first trait
        check1 = False
        while check1 == False:
            numPred = input("What should the density of predators in the world be? (scale of 1-10)")
            check1 = checkCustomInputs(numPred)
        customWorld.append(int(numPred))
        #second trait
        check2 = False
        while check2 == False:
            landMass = input("How much of the world should be covered by land? (scale of 1-10)")
            check2 = checkCustomInputs(landMass)
        customWorld.append(int(landMass))
        #third trait
        check3 = False
        while check3 == False:
            foodScarcity = input("How scarce should food be? (scale of 1-10; 10 is very hard to find food)")
            check3 = checkCustomInputs(foodScarcity)
        customWorld.append(int(foodScarcity))
        #fourth trait
        check4 = False
        while check4 == False:
            temp = input("How cold should the world be? (scale of 1-10)")
            check4 =checkCustomInputs(temp)
        customWorld.append(int(temp))
        
        print("customWorld: " + str(customWorld))
            
        kids = geneticAlgorithm(customWorld)
        print()
        print()
        print()
        print("WORLD TRAITS (All traits are on a scale from 1-10)")
        for trait in range(len(customWorld)):
            if trait == 0:
                print("Vegetation Density: " + str(customWorld[trait]))
            elif trait == 1:
                print("Density of Predators: " + str(customWorld[trait]))
            elif trait == 2:
                print("Land Mass Coverage: " + str(customWorld[trait]))
            elif trait == 3:
                print("Food Scarcity: " + str(customWorld[trait]))
            elif trait == 4:
                print("Temperature (10 is cold): " + str(customWorld[trait]))
        
        
        #average kid traits:
        avgList = [0, 0, 0, 0, 0]
        for kid in kids:
            for t in range(len(kid)):
                avgList[t] += kid[t]
        for avg in range(len(avgList)):
            avgList[avg] = round((avgList[avg] / len(kids)), 1)
        
        print()
        print("AVERAGE KID CHARACTERISTICS (All characteristics are on a scale from 1-10)")
        for character in range(len(avgList)):
            if character == 0:
                print("Size: " + str(avgList[character]))
            elif character == 1:
                print("Mobility: " + str(avgList[character]))
            elif character == 2:
                print("Dehydration Adaptations: " + str(avgList[character]))
            elif character == 3:
                print("Socialization: " + str(avgList[character]))
            elif character == 4:
                print("Cold Tolerance: " + str(avgList[character]))
        
        survivorPercentage = survivalRate(customWorld, kids)
        print()
        print("WORLD: " + str(customWorld))
        print("AVGKID: " + str(avgList))
        print("Survival Rate: " + str(survivorPercentage) + "%")
        
        run = False
    #Generate a random world
    elif "n" in customChoice:
        print()
        print()
        world = randWorld()     #generate the world the individuals will be adapting to
        kids = geneticAlgorithm(world)
        
        print("WORLD TRAITS (All traits are on a scale from 1-10)")
        for trait in range(len(world)):
            if trait == 0:
                print("Vegetation Density: " + str(world[trait]))
            elif trait == 1:
                print("Density of Predators: " + str(world[trait]))
            elif trait == 2:
                print("Land Mass Coverage: " + str(world[trait]))
            elif trait == 3:
                print("Food Scarcity: " + str(world[trait]))
            elif trait == 4:
                print("Temperature (10 is cold): " + str(world[trait]))
        print()
        
        #average kid traits:
        avgList = [0, 0, 0, 0, 0]
        for kid in kids:
            for t in range(len(kid)):
                avgList[t] += kid[t]
        for avg in range(len(avgList)):
            avgList[avg] = round((avgList[avg] / len(kids)), 1)
        
        print("AVERAGE KID CHARACTERISTICS (All characteristics are on a scale from 1-10)")
        for character in range(len(avgList)):
            if character == 0:
                print("Size: " + str(avgList[character]))
            elif character == 1:
                print("Mobility: " + str(avgList[character]))
            elif character == 2:
                print("Dehydration Adaptations: " + str(avgList[character]))
            elif character == 3:
                print("Socialization: " + str(avgList[character]))
            elif character == 4:
                print("Cold Tolerance: " + str(avgList[character]))
        
        
        survivorPercentage = survivalRate(world, kids)
        print()
        print("WORLD TRAITS: " + str(world))
        print("AVERAGE KID: " + str(avgList))
        print("Survival Rate: " + str(survivorPercentage) + "%")
        run = False
    else:
       print("Input not recognized")