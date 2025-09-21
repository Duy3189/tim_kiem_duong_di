import random
import copy

def fitness_non_conflict(state):
    """Fitness = số cặp hậu không tấn công nhau (max = 28 với 8 hậu)."""
    n = len(state)
    total_pairs = n * (n - 1) // 2
    conflicts = 0
    for i in range(n):
        for j in range(i+1, n):
            if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
                conflicts += 1
    return total_pairs - conflicts

def random_individual(n=8):
    return [random.randrange(n) for _ in range(n)]

def initial_population(pop_size=50, n=8):
    return [random_individual(n) for _ in range(pop_size)]

def tournament_selection(population, fitnesses, k=3):
    selected_idx = random.sample(range(len(population)), k)
    best = selected_idx[0]
    for idx in selected_idx[1:]:
        if fitnesses[idx] > fitnesses[best]:
            best = idx
    return copy.deepcopy(population[best])

def one_point_crossover(parent1, parent2):
    n = len(parent1)
    if n < 2:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)
    cut = random.randint(1, n-1)
    child1 = parent1[:cut] + parent2[cut:]
    child2 = parent2[:cut] + parent1[cut:]
    return child1, child2

def mutate_random_reset(individual, mutation_rate=0.1):
    n = len(individual)
    for i in range(n):
        if random.random() < mutation_rate:
            individual[i] = random.randrange(n)
    return individual

def genetic_algorithm(n=8, pop_size=100, generations=500,
                      crossover_rate=0.8, mutation_rate=0.1,
                      tournament_k=3, elitism=1, seed=None):
    """
    Genetic Algorithm cho 8 hậu.
    Trả về (best_ind, states) để hiển thị.
    """
    if seed is not None:
        random.seed(seed)

    population = initial_population(pop_size, n)
    fitnesses = [fitness_non_conflict(ind) for ind in population]

    states = []  
    total_pairs = n * (n - 1) // 2

    for gen in range(generations):
        best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
        best_ind = copy.deepcopy(population[best_idx])
        best_fit = fitnesses[best_idx]
        states.append(best_ind)

        if best_fit == total_pairs:
            return best_ind, states

        new_population = []
        if elitism > 0:
            ranked_idx = sorted(range(len(population)), key=lambda i: fitnesses[i], reverse=True)
            for i in range(min(elitism, len(population))):
                new_population.append(copy.deepcopy(population[ranked_idx[i]]))

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses, k=tournament_k)
            parent2 = tournament_selection(population, fitnesses, k=tournament_k)

            if random.random() < crossover_rate:
                child1, child2 = one_point_crossover(parent1, parent2)
            else:
                child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)

            child1 = mutate_random_reset(child1, mutation_rate)
            if len(new_population) < pop_size:
                new_population.append(child1)

            child2 = mutate_random_reset(child2, mutation_rate)
            if len(new_population) < pop_size:
                new_population.append(child2)

        population = new_population
        fitnesses = [fitness_non_conflict(ind) for ind in population]

    best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
    best_ind = copy.deepcopy(population[best_idx])
    states.append(best_ind)
    return best_ind, states
