import numpy as np
from random import randint

playerName = "myAgent"
nPercepts = 75  #This is the number of percepts
nActions = 5    #This is the number of actions

# Train against random for 5 generations, then against self for 1 generations
trainingSchedule = [("random", 1000)]

# This is the class for your creature/agent

class MyCreature:
    genome = []
    recessive_genome = []
    turn_count = 1
    game_num = 5
    final_fitness = np.zeros(game_num)
    survive_tracker = np.zeros(game_num)
    turn_tracker = np.zeros(game_num)
    size_tracker = np.zeros(game_num)
    strawberry_tracker = np.zeros(game_num)
    warrior_tracker = np.zeros(game_num)
    explore_tracker = np.zeros(game_num)
    bounce_tracker = np.zeros(game_num)
    game_fitness = 0

    def __init__(self):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values
        # first is friend, second is hungry, third is wall, fourth is enemy

        self.genome = []
        self.recessive_genome = []
        self.final_fitness = np.zeros((self.game_num))
        self.game_num = 5
        self.survive_tracker = np.zeros((self.game_num))
        self.turn_tracker = np.zeros((self.game_num))
        self.size_tracker = np.zeros((self.game_num))
        self.strawberry_tracker = np.zeros((self.game_num))
        self.warrior_tracker = np.zeros((self.game_num))
        self.explore_tracker = np.zeros((self.game_num))
        self.bounce_tracker = np.zeros((self.game_num))
        self.game_fitness = 0
        # initialise genome with 5 random chromosomes
        # initialise recessive genome in the same way
        for i in range(4):
            self.genome.append(createChromosome())
            self.recessive_genome.append(createChromosome())
        # initialise exploration chromosome
        # number correlates to a direction (0 for left)
        explore_chrom = []
        recessive_explore_chrom = []
        explore_chrom.append(randint(0, 4))
        recessive_explore_chrom.append(randint(0, 4))
        # initialise weight multiplier for the game
        for i in range(5):
            explore_chrom.append(round(np.random.uniform(0.00, 2.00), 2))
            recessive_explore_chrom.append(round(np.random.uniform(0.00, 2.00), 2))

        explore_chrom.append(randint(-100, 100))
        recessive_explore_chrom.append(randint(-100, 100))
        self.genome.append(explore_chrom)
        self.recessive_genome.append(recessive_explore_chrom)
        # initialise the turn number
        self.turn_count = 1


    def AgentFunction(self, percepts):

        # actions = np.zeros((nActions))
        actions = []
        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        # The 'actions' variable must be returned and it must be a 5-dim numpy vector or a
        # list with 5 numbers.
        #
        # The index of the largest numbers in the 'actions' vector/list is the action taken
        # with the following interpretation:
        # 0 - move left
        # 1 - move up
        # 2 - move right
        # 3 - move down
        # 4 - eat
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.

        # get actions for left
        actions.append(self.getAction(percepts, 0, 2, 0, 5))

        # get actions for up
        actions.append(self.getAction(percepts, 0, 5, 0, 2))

        # get actions for right
        actions.append(self.getAction(percepts, 3, 5, 0, 5))

        # get actions for down
        actions.append(self.getAction(percepts, 0, 5, 3, 5))

        # get action value for eat
        actions.append(self.getAction(percepts, 2, 3, 2, 3))

        # add "explore" modifier - pick a random direction to go when theres nothing in the vicinity
        mods = self.getTurnModifier()
        explore = self.genome[4][6]
        for n in mods:
            explore = explore * self.genome[4][n]
        actions[self.genome[4][0]] = actions[self.genome[4][0]] + explore

        self.turn_count = self.turn_count + 1

        return actions

    # returns a list of ints
    # checks the turn counter of self, relates that to the modifier for the chromosomes
    # i.e. genome[X][1-4]
    def getTurnModifier(self):
        result = []
        if(self.turn_count < 33):
            result.append(1)
        if(self.turn_count >= 25 and self.turn_count <=41):
            result.append(2)
        if(self.turn_count >= 33 and self.turn_count < 66):
            result.append(3)
        if(self.turn_count >= 58 and self.turn_count <= 74):
            result.append(4)
        if(self.turn_count >= 66):
            result.append(5)
        return result

    # get an action value for a direction. row_low, row_high, col_low and col_high are
    # used to define the area the creature is looking.
    # for example, if this was called to get the up value, it would look at the first 2 rows only
    # of the percepts.
    def getAction(self, percepts, row_low, row_high, col_low, col_high):
        result = 0
        # iterate through percepts (As a 3d array/list)
        # k, the third dimension of the array, has a value corresponding with the relevant chromosome
        # in the genome, e.g. i,j,0 is for creatures and genome[0] is the chromosome for friendly creatures
        for i in range(row_low, row_high):
            for j in range(col_low, col_high):
                for k in range(3):
                    # if the object at this position has a negative value, it must be an enemy creature
                    # pass into genome[3] - chromosome for enemies
                    if(percepts[i][j][k] < 0):
                        mods = self.getTurnModifier()
                        action = self.genome[3][0]
                        for n in mods:
                            action = action * self.genome[3][n]
                        size_mod = ((percepts[2][2][0] + 1) - abs(percepts[i][j][k])) * self.genome[3][6]
                        action = action * size_mod
                        result = result + action
                    elif(percepts[i][j][k] > 0):
                        mods = self.getTurnModifier()
                        action = self.genome[k][0]
                        for n in mods:
                            action = action * self.genome[k][n]
                        size_mod = ((percepts[2][2][0] + 1) - abs(percepts[i][j][k])) * self.genome[3][6]
                        action = action * size_mod
                        result = result + action
        return result


def newGeneration(old_population):

    # This function should return a list of 'new_agents' that is of the same length as the
    # list of 'old_agents'.  That is, if previous game was played with N agents, the next game
    # should be played with N agents again.

    # This function should also return average fitness of the old_population
    N = len(old_population)

    # Fitness for all agents
    fitness = np.zeros((N))

    # This loop iterates over your agents in the old population - the purpose of this boiler plate
    # code is to demonstrate how to fetch information from the old_population in order
    # to score fitness of each agent
    for n, creature in enumerate(old_population):

        # creature is an instance of MyCreature that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, the objects has attributes provided by the
        # game enginne:
        #
        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies
        # creature.squares_visited - how many different squares the creature visited
        # creature.bounces - how many times the creature bounced
        creature.game_num = creature.game_num - 1
        survival_multiplier = 1
        if(creature.alive):
            survival_multiplier = 1.5
            creature.survive_tracker[creature.game_num] = 1
        else:
            creature.survive_tracker[creature.game_num] = 0
        survival = creature.turn
        creature.turn_tracker[creature.game_num] = survival

        greedy = creature.strawb_eats * 2
        creature.strawberry_tracker[creature.game_num] = greedy

        gladiator = creature.enemy_eats * 3
        creature.warrior_tracker[creature.game_num] = gladiator

        tourist = creature.squares_visited/4
        creature.explore_tracker[creature.game_num] = tourist

        growth = creature.size
        creature.size_tracker[creature.game_num] = growth

        bouncy = (creature.bounces + 1) * 3
        creature.bounce_tracker[creature.game_num] = bouncy

        # baseline = pow(growth, (greedy + gladiator))

        # round(pow((pow((survival + tourist * growth), (greedy + gladiator)), (1 - bouncy))), 0)
        # round(pow((greedy + gladiator), growth), 0)
        # (greedy + gladiator) * growth
        # round(pow((greedy + gladiator), growth) / bouncy)
        if(creature.game_num == 0):
            survival = np.mean(creature.turn_tracker)
            growth = np.mean(creature.size_tracker)
            greedy = np.mean(creature.strawberry_tracker)
            gladiator = np.mean(creature.warrior_tracker)
            tourist = np.mean(creature.explore_tracker)
            bouncy = np.mean(creature.bounce_tracker)
            if(np.sum(creature.survive_tracker) > 3):
                survival_multiplier = 1.5
            else:
                survival_multiplier = 1
        # TODO fix the reporting fitness - difference: creature.final_fitness is being overwritten between games
        creature.game_fitness = (pow((greedy + gladiator),  growth) * survival_multiplier) * tourist
        creature.final_fitness[creature.game_num] = creature.game_fitness
        fitness[n] = creature.final_fitness[creature.game_num]


    new_population = list()
    avg_fitness = np.mean(fitness)

    game_fitness_map = open("Game_Fitness_plot.txt", "a")
    generation_fitness_map = open("Generation_fitness_plot.txt", "a")
    game_fitness_map.write(str(round(avg_fitness, 2)) + "\n")

    if(old_population[0].game_num > 0):
        print("interim fitness: ")
        return old_population, avg_fitness

    for x, creature in enumerate(old_population):
        fitness[x] = np.mean(creature.final_fitness)

    avg_fitness = np.mean(fitness)

    old_population.sort(reverse=True, key=lambda x: x.game_fitness)
    # elitism here
    elite_num = 3

    i = 0
    while(i < elite_num):
        # clone the elite chromosomes to initialise all other values
        new_creature = MyCreature()
        new_creature.genome = old_population[i].genome
        new_creature.recessive_genome = old_population[i].recessive_genome

        new_population.append(new_creature)
        i = i + 1

    # generate the weighted list for population breeding selection
    i = 0
    weighted_population = []
    while(i < N):
        counter = 0
        while(counter < (N - i) * 3):
            weighted_population.append(i)
            counter = counter + 1
        i = i+1

    tournament_size = 6

    while(len(new_population) < 20):
        breed_group = []
        temp_weight_pop = weighted_population.copy()
        while(len(breed_group) <= tournament_size):
            position = randint(0, len(temp_weight_pop) - 1)
            breed_group.append(old_population[temp_weight_pop[position]])
            temp = temp_weight_pop[position]
            temp_weight_pop = list(filter(lambda x: x != temp, temp_weight_pop))
        breed_group.sort(reverse=True, key=lambda x: x.game_fitness)
        new_creature = MyCreature()
        new_creature.genome, new_creature.recessive_genome = breed_superior(breed_group[0], breed_group[1])
        new_population.append(new_creature)

    while (len(new_population) < 28):
        breed_group = []
        temp_weight_pop = weighted_population.copy()
        i = 0
        while(i < elite_num):
            temp_weight_pop = list(filter(lambda x: x!= i, temp_weight_pop))
            i = i + 1
        while (len(breed_group) <= tournament_size):
            position = randint(0, len(temp_weight_pop) - 1)
            breed_group.append(old_population[temp_weight_pop[position]])
            temp = temp_weight_pop[position]
            temp_weight_pop = list(filter(lambda x: x != temp, temp_weight_pop))
        breed_group.sort(reverse=True, key=lambda x: x.game_fitness)
        new_creature = MyCreature()
        new_creature.genome, new_creature.recessive_genome = breed_superior(breed_group[0], breed_group[1])
        new_population.append(new_creature)

    while (len(new_population) < 34):
        breed_group = []
        temp_weight_pop = weighted_population.copy()
        while (len(breed_group) <= tournament_size):
            position = randint(0, len(temp_weight_pop) - 1)
            breed_group.append(old_population[temp_weight_pop[position]])
            temp = temp_weight_pop[position]
            temp_weight_pop = list(filter(lambda x: x != temp, temp_weight_pop))
        breed_group.sort(reverse=True, key=lambda x: x.game_fitness)
        new_creature = MyCreature()
        new_creature.genome, new_creature.recessive_genome = breed_inferior(breed_group[0], breed_group[1])
        new_population.append(new_creature)

    # At the end you need to compute average fitness and return it along with your new population

    generation_fitness_map.write(str(round(avg_fitness, 2)) + "\n")

    return (new_population, avg_fitness)


def createChromosome():
    result = []
    result.append(randint(-100, 100))
    for i in range(5):
        result.append(round(np.random.uniform(0.00, 2.00), 2))
    # add another gene for the size difference modifier
    result.append(randint(-100, 100))
    return result

def breed_inferior(mother, father):
    child_genome = []
    child_recessive_genome = []
    swap_pos = []
    recession_chance = 998
    mutation_chance = 998
    for i, chromosome in enumerate(mother.genome):
        child_chromosome = []
        child_recessive_chromosome = []
        num_swamps = randint(1, len(chromosome) - 2)
        while (len(swap_pos) < num_swamps):
            index = randint(0, 4)
            if(index not in swap_pos):
                swap_pos.append(index)

        decider = randint(-1, 1)
        while(decider == 0):
            decider = randint(-1, 1)
        swap_pos.sort()
        k = 0
        while(k < len(chromosome)):
            if(decider < 0):
                child_chromosome.append(father.genome[i][k])
                child_recessive_chromosome.append(father.recessive_genome[i][k])
            else:
                child_chromosome.append(mother.genome[i][k])
                child_recessive_chromosome.append(mother.recessive_genome[i][k])
            k = k + 1
            if(k in swap_pos):
                decider = decider * -1
        child_genome.append(child_chromosome)
        child_recessive_genome.append(child_recessive_chromosome)

    if(randint(0, 1000) > mutation_chance):
        chrom_num = randint(0, len(child_genome) - 1)
        gene_num = randint(0, len(child_genome[chrom_num]) - 1)
        recess_or_dom = randint(0, 1)
        if(gene_num == 0):
            # if chrom_number = 4, MUST BE BETWEEN 0 AND 3 inclusive
            if(recess_or_dom > 0):
                if(chrom_num == 4):
                    child_genome[chrom_num][0] = randint(0, 4)
                else:
                    child_genome[chrom_num][0] = randint(-100, 100)
            else:
                if(chrom_num == 4):
                    child_genome[chrom_num][0] = randint(0, 4)
                else:
                    child_recessive_genome[chrom_num][0] = randint(-100, 100)
        else:
            if(recess_or_dom > 0):
                if(gene_num == 6 and chrom_num == 4):
                    child_genome[chrom_num][gene_num] = randint(-100, 101)
                else:
                    child_genome[chrom_num][gene_num] = round(np.random.uniform(0.00, 2.00), 2)
            else:
                if(gene_num == 6 and chrom_num == 4):
                    child_genome[chrom_num][gene_num] = randint(-100, 100)
                else:
                    child_recessive_genome[chrom_num][gene_num] = round(np.random.uniform(0.00, 2.00), 2)
        print("A mutation has occurred!")

    if(randint(0, 1000) > recession_chance):
        chrom_num = randint(0, len(child_genome) - 1)
        gene_num = randint(0, len(child_genome[chrom_num]) - 1)
        temp_swap = child_genome[chrom_num][gene_num]
        child_genome[chrom_num][gene_num] = child_recessive_genome[chrom_num][gene_num]
        child_recessive_genome[chrom_num][gene_num] = temp_swap
        print("A recessive switch has occurred!")

    return child_genome, child_recessive_genome

def breed_superior(mother, father):
    child_genome = []
    child_recessive_genome = []
    swap_pos = []
    decider = randint(-1, 1)
    while(decider == 0):
        decider = randint(-1, 1)
    swap_nums = randint(1, 5)
    counter = 0
    while(counter < swap_nums):
        # 0 - 4
        temp = randint(0, 4)
        if(temp not in swap_pos):
            swap_pos.append(temp)
            counter = counter + 1
    for i, chromosome in enumerate(mother.genome):
        if(decider < 0):
            child_genome.append(mother.genome[i])
            child_recessive_genome.append(mother.recessive_genome[i])
        else:
            child_genome.append(father.genome[i])
            child_recessive_genome.append(father.recessive_genome[i])
        if(i in swap_pos):
            decider = decider * -1
    return child_genome, child_recessive_genome