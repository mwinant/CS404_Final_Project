import pygad
import random
from menu import Menu
from process_data import add_profit_column_to_csv, preprocess_data

LEN_MENU = 20

# Load data into a DataFrame
filename = add_profit_column_to_csv('bakery_sales_revised_items_removed.csv')
df = preprocess_data(filename)

# Create a Menu instance
menu = Menu(df)


def fitness_func(ga_instance, solution, solution_idx):
    global menu

    # Convert solution indices to selected items
    unique_items = menu.data['Item'].unique()
    selected_items = [unique_items[i]
                      for i, gene in enumerate(solution) if gene == 1]

    # Get profitability DataFrame
    profitability = menu.analyze_profitability()

    # Calculate total profit for selected items
    total_profit = 0
    for item in selected_items:
        match = profitability.loc[profitability['Item'] == item, 'fitness']
        if not match.empty:
            total_profit += match.values[0]
        else:
            print(f"Warning: Item '{item}' not found in profitability data.")

    return total_profit


def custom_mutation(ga_instance, offspring):
    for chromosome in offspring:
        # Ensure desired menu length genes are `1`
        indices = [i for i, gene in enumerate(chromosome) if gene == 1]

        # If more than desired length, randomly set excess genes to 0
        while len(indices) > LEN_MENU:
            idx_to_remove = random.choice(indices)
            chromosome[idx_to_remove] = 0
            indices.remove(idx_to_remove)

        # If fewer than desired length, randomly set additional genes to 1
        while len(indices) < LEN_MENU:
            idx_to_add = random.choice([i for i in range(len(chromosome))
                                        if chromosome[i] == 0])
            chromosome[idx_to_add] = 1
            indices.append(idx_to_add)

    return offspring


def main():

    ga_instance = pygad.GA(
                num_generations=50,
                num_parents_mating=10,
                fitness_func=fitness_func,
                sol_per_pop=50,
                num_genes=len(menu.data['Item'].unique()),
                gene_type=int,
                gene_space=[0, 1],
                parent_selection_type="sus",
                keep_parents=1,
                crossover_probability=0.7,
                mutation_probability=0.1,
                on_mutation=custom_mutation
    )

    # Run the GA
    ga_instance.run()

    # Get the best solution
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    selected_menu_items = menu.get_menu_names(solution, df)
    print("Selected Menu Items: ", selected_menu_items)
    print("Best Fitness: ", solution_fitness)
    ga_instance.plot_fitness()


if __name__ == "__main__":
    main()
