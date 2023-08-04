class Budget:
    def __init__(self, income=0):
        self.income = income
        self.categories = {}

    def __str__(self):
        margins = 15
        output = f"{'Income:':<{margins}} $ {self.income:,.2f}\n"
        output += f"{'Spending:':<{margins}} $ {self.total_spending():,.2f}\n"
        output += f"-----------------------------------\n"
        for key in self.categories:
            output += f"{key+':':<{margins}} $ {self.categories[key]:,.2f}\n"
        return output

    def total_spending(self):
        total = 0
        for amount in self.categories.values():
            total += amount
        return total

    def adjust_income(self, updated_income):
        self.income = updated_income

    def add_category(self, name, amount=0):
        if name in self.categories:
            print("This category already exists")
        else:
            self.categories[name] = amount


if __name__ == "__main__":
    my_budget = Budget()
    my_budget.add_category("Tithing", 80)
    print(my_budget)
    