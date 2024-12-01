import pandas as pd
import numpy as np


def add_profit_column_to_csv(file_name: str) -> str:
    """Add profit column to filename and generate profit values from $1 - $3.

    Args:
        file_name (str): name of original csv file.

    Returns:
        str: name of revised csv file with added profit columns.
    """
    df = pd.read_csv(file_name)
    unique_items = df['Item'].unique()
    profit_values = np.random.uniform(1, 3, size=len(unique_items))
    item_profit_dict = dict(zip(unique_items, profit_values))
    df['Profit'] = df['Item'].map(item_profit_dict).round(2)
    df.to_csv('bakery_sales_revised_with_profit.csv', index=False)
    return 'bakery_sales_revised_with_profit.csv'


def calculate_baseline_profit():
    """
    Calculates the baseline profit for each item in the dataset,
        assuming no promotions.

    data: pd.DataFrame, the sales data containing item information and profit.

    Returns: float, the total baseline profit (sum of profit for all items).
    """
    data = pd.read_csv('optimal_menu.csv')
    # Ensure 'Profit' column is available in the dataset
    if 'Profit' not in data.columns:
        raise ValueError("The dataset must contain a 'Profit' column.")

    # Sum up the profit for each item (without any promotion applied)
    total_baseline_profit = data['Profit'].sum()

    return total_baseline_profit


def preprocess_data(file_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_name)
    return df


def optimal_menu():
    optimal_items = ['Bread', 'Hot chocolate', 'Coffee', 'Pastry', 'Medialuna',
                     'Tea', 'Fudge', 'Juice', 'Soup', 'Smoothies', 'Cake',
                     'Focaccia', 'Sandwich', 'Alfajores', 'Brownie', 'Toast',
                     'Scone', 'Crepes', 'Vegan mincepie', 'Baguette']

    df = pd.read_csv('bakery_sales_revised_with_profit.csv')
    df = df[df['Item'].isin(optimal_items)]
    df.to_csv('optimal_menu.csv', index=False)


def remove_items_from_csv(csv_file_path):
    # List of items to remove
    items_to_remove = [
        'Gift voucher', 'Half slice Monster', 'Argentina Night',
        'Christmas common', 'Nomad bag', 'Vegan Feast', "Valentine's card",
        'Duck egg', 'Extra Salami or Feta',
        'Afternoon with the baker', 'Pintxos', 'Gingerbread syrup', 'Siblings',
        'Jammie Dodgers', 'Tiffin', 'Olum & polenta', 'Polenta', 'The Nomad',
        'Hack the stack', 'Bakewell', 'Chimichurri Oil', 'Adjustment',
        'Keeping It Local', 'Art Tray', 'Bowl Nic Pitt', 'Fairy Doors',
        'The BART', "Ella's Kitchen Pouches", 'Basket', 'Farm House',
        'Hearty & Seasonal', 'Pick and Mix Bowls', 'Mortimer', 'Tshirt',
        'Postcard', 'Postcard', 'My-5 Fruit Shoot'
    ]

    df = pd.read_csv(csv_file_path)
    df = df[~df['Item'].isin(items_to_remove)]


def assign_profit(df: pd.DataFrame):
    """
    Dictionary mapping items to their dollar amounts.

    df: pd.DataFrame.

    Returns: pd.Dataframe, df with profit column."""
    profit_mapping = {
        'Bread': 2, 'Scandinavian': 2.5, 'Hot chocolate': 2.5, 'Jam': 1.25,
        'Cookies': 1.5, 'Muffin': 2, 'Coffee': 2, 'Pastry': 2.5,
        'Tea': 2, 'Tartine': 3, 'Mineral water': 1.5, 'Fudge': 2, 'Juice': 2,
        'Victorian Sponge': 3, 'Frittata': 3, 'Soup': 3, 'Smoothies': 2.5,
        'Cake': 3, 'Mighty Protein': 2, 'Chicken sand': 3.5, 'Coke': 1,
        'Focaccia': 2.5, 'Sandwich': 3.5, 'Alfajores': 1.5, 'Eggs': 1.5,
        'Brownie': 2, 'Dulce de Leche': 1.5, 'Honey': 1.25, 'Granola': 2,
        'Empanadas': 2.5, 'Bread Pudding': 2.5, 'Truffles': 2, 'Bacon': 1,
        'Spread': 1.25, 'Kids biscuit': 1, 'Caramel bites': 1.5,
        'Lemon and coconut': 2, 'Toast': 1, 'Scone': 2, 'Crepes': 2.5,
        'Vegan mincepie': 2, 'Bare Popcorn': 1.5, 'Muesli': 2, 'Crisps': 1,
        'Panettone': 3, 'Brioche and salami': 3, 'Salad': 3, 'Chicken Stew': 3,
        'Spanish Brunch': 4, 'Raspberry shortbread sandwich': 2, 'Baguette': 2,
        'Chocolates': 2, 'Coffee granules': 1.5,
        'Cherry me Dried fruit': 1.25, 'Raw bars': 2, 'Tacos-Fajita': 3,
        'Medialuna': 1.5, 'Drinking chocolate spoons': 2
    }

    # Create a new column 'profit' by mapping item names to their profit values
    df['profit'] = df['Item'].map(profit_mapping)

    return df


def main():
    # df = remove_items_from_csv('bakery_sales_revised.csv')
    # df = assign_profit(df)
    # df.to_csv('bakery_sales_revised_items_removed.csv', index=False)
    # optimal_menu()
    base_profit = calculate_baseline_profit()
    print(base_profit)


if __name__ == "__main__":
    main()
