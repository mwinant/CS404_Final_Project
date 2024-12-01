import pandas as pd
import pygad
import matplotlib.pyplot as plt
from menu import Menu

# Load data
df = pd.read_csv('optimal_menu.csv')

# Create a Menu instance
menu = Menu(df)


def fitness_func(ga_instance, solution, solution_idx):
    global menu
    total_profit = 0
    total_cost = 0
    max_budget = 1000  # Example budget constraint

    unique_items = menu.data['Item'].unique()

    # Compute total profit and cost
    for i, promotion_type in enumerate(solution):
        item = unique_items[i]
        total_profit += menu.apply_promotion(item, promotion_type)
        total_cost += menu.promotion_cost(item, promotion_type)

    # Penalize solutions that exceed the budget
    if total_cost > max_budget:
        total_profit -= (total_cost - max_budget) * 10  # Penalty factor

    # Store cost and profit for tradeoff visualization
    if hasattr(ga_instance, "cost_profit_data"):
        ga_instance.cost_profit_data.append((total_cost, total_profit))

    return total_profit


# Define the number of items
num_items = len(df['Item'].unique())

# Create a GA instance
ga_instance = pygad.GA(
    num_generations=50,
    num_parents_mating=10,
    fitness_func=fitness_func,
    sol_per_pop=50,
    num_genes=num_items,
    gene_type=int,
    gene_space=[0, 1, 2],  # Promotion types: 0: None, 1: Discount, 2: BOGO
    parent_selection_type="sus",
    keep_parents=1,
    crossover_probability=0.7,
    mutation_probability=0.1
)

# Initialize storage for cost vs. profit data
ga_instance.cost_profit_data = []

# Run the GA
ga_instance.run()

# Get the best solution
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Optimal Promotions: ", solution)
print(f"Fitness value of the best solution = {solution_fitness}")

# Convert the best solution to a DataFrame
optimal_promotions = pd.DataFrame({
    'Item': df['Item'].unique(),
    'Promotion Type': solution
})
print(optimal_promotions)

# Plot fitness over generations
ga_instance.plot_fitness()

# Plot Histogram of Final Promotion Types
plt.figure(figsize=(8, 6))
plt.hist(solution, bins=[-0.5, 0.5, 1.5, 2.5], rwidth=0.8, color='skyblue')
plt.xticks([0, 1, 2], labels=["No Promotion", "Discount", "BOGO"])
plt.xlabel("Promotion Type")
plt.ylabel("Frequency")
plt.title("Distribution of Promotion Types in Optimal Solution")
plt.show()
