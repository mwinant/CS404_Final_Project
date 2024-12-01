class Menu:
    def __init__(self, data):
        self.data = data

    def apply_promotion(self, item, promotion_type):
        """
        Calculates the profit after applying the given promotion type to the
            item.

        item: str, the name of the item.
        promotion_type: int, the type of promotion
            (0: No promotion, 1: Discount, 2: BOGO).

        Returns: float, the profit after applying the promotion.
        """
        base_profit = self.data[self.data['Item'] == item]['Profit'].sum()

        if promotion_type == 0:  # No promotion
            return base_profit
        elif promotion_type == 1:  # Discount
            return base_profit * 1.1  # 10% increase due to discount
        elif promotion_type == 2:  # Buy-one-get-one-free (BOGO)
            return base_profit * 1.2  # 20% increase due to BOGO

    def promotion_cost(self, item, promotion_type):
        """
        Estimates the cost of applying a promotion to an item based on
            its profit.

        item: str, the name of the item.
        promotion_type: int, the type of promotion
            (0: No promotion, 1: Discount, 2: BOGO).

        Returns: float, the estimated cost of the promotion.
        """
        base_profit = self.data[self.data['Item'] == item]['Profit'].sum()

        if promotion_type == 0:  # No promotion
            return 0
        elif promotion_type == 1:  # Discount
            return base_profit * 0.05  # 5% of the profit as cost for discount
        elif promotion_type == 2:  # BOGO
            return base_profit * 0.1  # 10% of the profit as cost for BOGO

    def analyze_profitability(self):
        """
        Analyze the profitability of each item and return a fitness score.

        Returns:
            pd.DataFrame: A summary DataFrame with total profit,
            average profit, transaction count, and a fitness score.
        """
        # Group by 'Item' and aggregate metrics
        summary = self.data.groupby('Item').agg(
            total_profit=('Profit', 'sum'),
            average_profit=('Profit', 'mean'),
            count=('Transaction', 'nunique')
        ).reset_index()

        # Calculate fitness score: total profit * average profit * count
        summary['fitness'] = (
            summary['total_profit'] *
            summary['average_profit'] *
            summary['count']
        )

        # Sort by fitness descending for ranking
        summary = summary.sort_values(
            by='fitness', ascending=False).reset_index(drop=True)

        summary.fillna(0, inplace=True)
        return summary

    def get_menu_names(self, solution, menu_data):
        """
        Convert the best solution (binary array) into corresponding menu items.

        solution: A binary array where 1 indicates the item is selected.
        menu_data: A DataFrame containing the menu items.

        Returns: A list of selected menu item names.
        """
        # Get unique menu items
        unique_items = menu_data['Item'].unique()

        # Select items based on the solution
        selected_items = [unique_items[i] for i in range(len(solution))
                          if solution[i] == 1]

        return selected_items
