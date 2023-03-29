import musicalbeeps
from typing import List, Set, Tuple
import random as rd
from util.config import POPULATION_SIZE, NUMBER_OF_NOTES, MUTATION_RATE, REPRODUCTION_RATE, CROSSOVER_RATE, \
    MAX_NUMBER_OF_GENERATIONS, MAX_FITNESS_VALUE, target_note, target_dict, LIST_OF_POSSIBLE_NOTES

from entities.Individual import Individual


def generate_initial_population(count=POPULATION_SIZE) -> List[Individual]:
    population: Set[Individual] = set()

    # generate_initial_population
    while len(population) != count:
        notes: List[str] = [
            rd.choice(LIST_OF_POSSIBLE_NOTES)
            for _ in range(NUMBER_OF_NOTES)
        ]
        population.add(Individual(notes))

    return list(population)


# k-tournament selection, N = 2
def selection(population: List[Individual]) -> List[Individual]:
    parents_temp: List[Individual] = []
    parents: List[Individual] = []

    k: int = int(POPULATION_SIZE * (1 / 3))
    n = 2

    for _ in range(n):
        for j in range(k):
            idx = rd.randint(0, len(population) - 1)
            parents_temp.append(population[idx])

        max_idx, max_value = 0, -1
        for j in range(len(parents_temp)):
            if parents_temp[j].fitness() > max_value:
                max_value = parents_temp[j].fitness()
                max_idx = j

        parents.append(parents_temp[max_idx])

    return parents


# one-point crossover
def crossover(parents: List[Individual]) -> List[Individual]:
    crossover_point = rd.randint(1, NUMBER_OF_NOTES - 2)

    child1: List[str] = parents[0].notes[:crossover_point] + parents[1].notes[crossover_point:]
    child2: List[str] = parents[0].notes[crossover_point:] + parents[1].notes[:crossover_point]

    return [Individual(child1), Individual(child2)]


# one-gene mutation
def mutate(individuals: List[Individual]) -> None:
    mutation_type = rd.choice(['swap', 'replace'])

    for individual in individuals:
        if mutation_type == 'swap':
            idx1, idx2 = rd.sample(range(len(individual.notes)), 2)
            individual.notes[idx1], individual.notes[idx2] = individual.notes[idx2], individual.notes[idx1]
        else:
            idx = rd.randint(0, len(individual.notes) - 1)
            individual.notes[idx] = rd.choice(LIST_OF_POSSIBLE_NOTES)


def next_generation(population: List[Individual]) -> List[Individual]:
    next_gen = []
    while len(next_gen) < len(population):
        children = []

        parents = selection(population)

        if rd.random() < REPRODUCTION_RATE:
            children = parents
        else:
            if rd.random() < CROSSOVER_RATE:
                children = crossover(parents)

            if rd.random() < MUTATION_RATE:
                mutate(children)

        next_gen.extend(children)

    return next_gen[:len(population)]


def print_generation(population: List[Individual]):
    for individual in population:
        print(individual.notes, individual.fitness(), individual.dict_notes, individual.number_of_shared_items())


def best_fitness(population: List[Individual]) -> Tuple[Individual, int]:
    max_idx, max_fitness = 0, 0
    for idx, i in enumerate(population):
        if i.fitness() > max_fitness:
            max_fitness = i.fitness()
            max_idx = idx

    return population[max_idx], max_fitness

def play_notes(notes: List[str]):
    player = musicalbeeps.Player(volume=0.15, mute_output=False)

    for note in notes:
        note_to_play = ''
        duration_note = ''
        flag = 0
        for c in note:
            if c != '-' and flag == 0:
                note_to_play += c
            elif c == '-':
                flag = 1
            else:
                duration_note += c

        player.play_note(note_to_play, float(duration_note))

def solve_melody() -> Tuple[Individual, int]:
    population: List[Individual] = generate_initial_population()

    best_fitness_in_gen = 0
    best_individual_in_gen: Individual = population[0]
    number_of_evolutions = 0

    for _ in range(MAX_NUMBER_OF_GENERATIONS):
        best_individual_in_gen, best_fitness_in_gen = best_fitness(population)
        if number_of_evolutions % 1000 == 0:
            print(target_note, MAX_FITNESS_VALUE, target_dict, "----> target_note")
            print_generation(population)

            print("|\n|\n|>>>>\n")

            play_notes(best_individual_in_gen.notes)
            print("\n")

        if best_fitness_in_gen == MAX_FITNESS_VALUE:
            break
        else:
            population = next_generation(population)
            number_of_evolutions += 1

    print_generation(population)
    print("|\n|\n|>>>>\n")

    play_notes(best_individual_in_gen.notes)
    print("\n")

    return best_individual_in_gen, number_of_evolutions

