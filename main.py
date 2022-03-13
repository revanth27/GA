# Python3 program to create target string, starting from
# random string using Genetic Algorithm

import random, os, json
from client import *

# Number of individuals in each generation
population_size = 10
generations = 10
key = 'IRDzab0r8NVz42nWKGxFrI9qJLX7aEwZ1tbHLzRXotkhA4OLoD'
overfit_vect = [0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10]
output_file = open('trace.txt', 'a')


class Individual(object):
    '''
    Class representing individual in population
    '''
    def __init__(self, chromosome, generation):
        self.chromosome = chromosome
        self.fitness = [-1, -1]
        self.generation = generation

    def cal_fitness(self):
        fitness = get_errors(key, self.chromosome)
        #fitness = [1,1]
        return fitness

def create_gnome():
        ret = overfit_vect.copy()

        for _ in range(4):
            k = random.randint(0, 10)
            ret[k] += random.uniform(-ret[k]*0.0001, ret[k]*0.0001)

        return ret


def mate(population):
        par1 = 0
        par2 = 0

        while(par1 == par2):
            par1 = random.randint(0, population_size//5)
            par2 = random.randint(0, population_size//5)

        parent1 = population[par1].chromosome.copy()
        parent2 = population[par2].chromosome.copy()

        child1 = parent1.copy()
        child2 = parent2.copy()

        for idx in range(0, len(parent2)):
            if random.uniform(0.0, 1.0) < 0.6:
                child1[idx] = parent2[idx]
                child2[idx] = parent1[idx]


        output_file.write("Parent " + str(par1) + " -> " + str(parent1) + "\n")
        output_file.write("Parent " + str(par2) + " -> " + str(parent2) + "\n")
        output_file.write("1st offspring vector after mutation -> " + str(child1) + "\n")
        output_file.write("2nd offspring vector after mutation -> " + str(child2) + "\n\n")

        return child1, child2

def mutated_genes(chromosome):
        erval = 0.00000000001
        f = 0
        for idx in range(0, len(chromosome)):
            f = 1
            if random.uniform(0.0, 1.0) <= 0.3:
                chromosome[idx] += random.uniform(-erval, erval)

        return chromosome, f

# Driver code
def main():
    global population_size
    global overfit_vect
    global generations
    generation = 1

    found = False
    population = []
    best_vect = []

    for i in range(population_size):
        gnome = create_gnome()
        population.append(Individual(gnome, generation))

    while not found:
        print(generation)

        for i in range(population_size):
            if population[i].fitness[0] + population[i].fitness[1] == -2:
                population[i].fitness = population[i].cal_fitness()
            if generation == 1:
                best_vect.append(population[i])

        population = sorted(population, key = lambda x: x.fitness[0] + x.fitness[1])

        output_file.write("\nRound Number : " + str(generation) + "\n")
        output_file.write("\nPopulation : \n")
        for i in range(population_size):
                output_file.write(str(i+1) + ". Vector -> " + str("population[") + str(i) + str("].chromosome = ") + str(population[i].chromosome) + "\n" + str("population[") + str(i) + str("].fitness = ") + str(population[i].fitness) + " Fitness score -> " + str(population[i].fitness[0]+population[i].fitness[1]) + "\n")


        new_generation = []

        output_file.write("\nTop 20% Individuals directly enter next generation\n")

        s = int((20*population_size)/100)
        for i in range(s):
            new_generation.append(population[i])
            output_file.write(str(population[i].chromosome) + " Errors -> " + str(population[i].fitness) + " Fitness -> " + str(population[i].fitness[0] + population[i].fitness[1]) + "\n")


        output_file.write("\nRest 80% Inviduals come from crossing\n")
        s = int((40*population_size)/100)
        output_file.write("\nOffsprings " + "\n\n")
        for _ in range(s):
            child1, child2 = mate(population)
            new_generation.append(Individual(child1, generation+1))
            new_generation.append(Individual(child2 ,generation+1))

        population = new_generation

        for i in range(population_size):
            output_file.write("\nAfter mutation of" + str(population[i].chromosome) + "is\n")
            population[i].chromosome, f = mutated_genes(population[i].chromosome)
            if f:
                population[i].generation = generation + 1
                if i < 2:
                    best_vect.append(population[i])
                population[i].fitness = population[i].cal_fitness()
            if i > 1:
                best_vect.append(population[i])
            output_file.write(str(population[i].chromosome) + "\n")

        population = sorted(population, key = lambda x: x.fitness[0] + x.fitness[1])

        output_file.write("\nNew generation : \n")
        for i in range(population_size):
            output_file.write(str("population[") + str(i) + str("].chromosome = ") + str(population[i].chromosome) + "\n" + str("population[") + str(i) + str("].fitness = ") + str(population[i].fitness) + " Fitness score -> " + str(population[i].fitness[0]+population[i].fitness[1]) + "\n")


        if generation > generations:
            found = True
            best_vect = sorted(best_vect, key = lambda x: x.fitness[0] + x.fitness[1])
            for h in range(0, 11):
                output_file.write("Chromosome -> " + str(best_vect[h].chromosome) + "\n" + "Generation - " + str(best_vect[h].generation) + "\n" + "Fitness - " + str(best_vect[h].fitness[0]) + " " + str(best_vect[h].fitness[1]) + " =" + str(best_vect[h].fitness[0] + best_vect[h].fitness[1]) + "\n")
            break

        generation += 1


if __name__ == '__main__':
    main()