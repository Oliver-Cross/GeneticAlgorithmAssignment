import matplotlib.pyplot as plt

game_fitness = []
generation_fitness = []

gen_file = open("Generation_fitness_plot.txt","r")
game_file = open("Game_Fitness_plot.txt", "r")

for line in gen_file:
    line = line.strip()
    generation_fitness.append(float(line))

for line in game_file:
    line = line.strip()
    game_fitness.append(float(line))

plt.plot(generation_fitness)
plt.axis([0, 50, 0, 25])
plt.show()
