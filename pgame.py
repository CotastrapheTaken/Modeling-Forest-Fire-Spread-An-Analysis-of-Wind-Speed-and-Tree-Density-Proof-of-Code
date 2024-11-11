import pygame
import numpy as np
import random
import os

# colors in rgb
BLACK = (0, 0, 0)       # Empty
GREEN = (34, 139, 34)   # Tree
ORANGE = (255, 165, 0)  # Burning
RED = (255, 0, 0)       # Burnt

# starting the pygame
pygame.init()
size = (800, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("forest fire simulator")

# function to create the forest


def create_forest(grid_size, tree_density):
    forest = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            if random.random() < tree_density:
                forest[i][j] = 1  # tree
    return forest  # corrected indentation here

# start the fire at a random location


def start_fire(forest):  # changed to start_fire for consistency
    x, y = random.randint(
        0, forest.shape[0] - 1), random.randint(0, forest.shape[1] - 1)
    forest[x][y] = 2  # burning
    return forest

# spread fire rules


def spread_fire(forest, wind_speed):
    new_forest = np.copy(forest)
    fire_spread = False
    burnt_trees = 0

    for i in range(forest.shape[0]):
        for j in range(forest.shape[1]):
            if forest[i][j] == 2:  # burning
                new_forest[i][j] = 3  # burnt
                burnt_trees += 1

                # check neighbors to spread fire
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for ni, nj in neighbors:
                    if 0 <= ni < forest.shape[0] and 0 <= nj < forest.shape[1]:
                        if forest[ni][nj] == 1:
                            prob_spread = wind_speed / 10
                            if random.random() < prob_spread:
                                new_forest[ni][nj] = 2  # start burning
                                fire_spread = True
    return new_forest, fire_spread, burnt_trees

# draw the forest function


def draw_forest(forest, cell_size):
    for i in range(forest.shape[0]):
        for j in range(forest.shape[1]):
            color = BLACK
            if forest[i][j] == 1:
                color = GREEN
            elif forest[i][j] == 2:
                color = ORANGE
            elif forest[i][j] == 3:
                color = RED
            pygame.draw.rect(screen, color, (j * cell_size,
                             i * cell_size, cell_size, cell_size))


# logging function
def write_log(burnt_trees, steps):
    log_folder = 'logs'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_number = 1
    while os.path.exists(f'{log_folder}/log_{log_number}.txt'):
        log_number += 1

    with open(f'{log_folder}/log_{log_number}.txt', 'w') as file:
        file.write(f"Burnt trees: {burnt_trees}, Steps: {steps}\n")


# simulation
def simulate_fire(grid_size, tree_density, wind_speed, max_steps):
    forest = create_forest(grid_size, tree_density)
    forest = start_fire(forest)

    cell_size = size[0] // grid_size
    step = 0
    total_burnt_trees = 0
    running = True

    while running and step < max_steps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)  # clears the screen
        draw_forest(forest, cell_size)
        pygame.display.flip()  # updates the display

        forest, fire_spread, burnt_trees = spread_fire(forest, wind_speed)
        total_burnt_trees += burnt_trees

        if not fire_spread:
            print("The fire stopped spreading.")
            break  # end simulation when fire stops spreading

        step += 1
        pygame.time.delay(300)  # delay for smoother visualization

    # call write_log only once after the simulation ends
    write_log(total_burnt_trees, step)
    pygame.quit()


# run simulation
simulate_fire(grid_size=50, tree_density=0.7, wind_speed=5, max_steps=50)
