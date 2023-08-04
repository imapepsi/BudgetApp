from Budget import Budget
from functools import partial
import tkinter as tk

class Window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("My Budget")
        self.window.geometry("500x400")  # height x width
        self.parent_frame = tk.Frame()
        self.parent_frame.columnconfigure(0, minsize=30)
        self.parent_frame.columnconfigure(1, minsize=5)
        self.parent_frame.columnconfigure(2, minsize=30)
        self.parent_frame.columnconfigure(3, minsize=30)
        self.parent_frame.pack()

        self.width = 25
        self.column_labels = 0
        self.column_money = 2
        self.column_buttons = 3
        # self.labels = {}
        self.budget = Budget()

        self.income_frame()

        # Start the main event loop
        self.window.mainloop()

    def make_label(self, content, row, column):
        """Return a new label and place in frame grid"""
        label = tk.Label(master=self.parent_frame, text=f"{content:<{self.width}}")
        label.grid(row=row, column=column, sticky=tk.W)  # tk.W = align west or left, tk.W = align North or top, etc.
        # self.labels[name] = label

    def fill_empty(self, row, column):
        """Make an empty space for padding"""
        empty = tk.Label(self.parent_frame)
        empty.grid(row=row, column=column)
        return empty

    def dollar_sign(self, row):
        """Make a dollar sign label"""
        label_dollar = tk.Label(master=self.parent_frame, text=f"{'$':<{3}}")
        label_dollar.grid(row=row, column=1, sticky=tk.W)  # tk.W = align west or left, tk.W = align North or top, etc.
        return label_dollar

    def update_income(self, entry):
        """Get the update income from entry and update the difference between income and spending"""
        # Get the text and format to number
        text = entry.get()
        entry.delete(0, len(text))
        text = text.replace(",", "")
        entry.insert(0, f"{float(text):,.2f}")

        try:
            # Update budget
            self.budget.adjust_income(float(text))
            # Calculate difference between income and spending
            difference = self.budget.income - self.budget.total_spending()
            # Update the label
            self.make_label(f"{difference:<,.2f}", 2, 2)

            print("Updated Income:", float(text))

        except ValueError as error:
            print("Error: entry included alpha-characters")

    def add_category(self, entry, start_row, amount=0.0):
        """Add a budget Category"""
        text = entry.get()
        entry.delete(0, len(text))

        self.budget.add_category(text, amount)
        row = len(self.budget.categories) + start_row

        self.make_label(text, row, 0)
        self.dollar_sign(row)

        entry_amount = tk.Entry(master=self.parent_frame, fg="white", bg="grey", width=self.width)
        entry_amount.insert(0, f"{self.budget.categories[text]:,.2f}")
        entry_amount.grid(row=row, column=self.column_money, sticky=tk.W)

        button = tk.Button(master=self.parent_frame, text="Save", command=partial(self.update_category, text, entry_amount))
        button.grid(row=row, column=self.column_buttons, sticky=tk.W)

        print("User added:", text)

        return entry_amount

    def update_category(self, category, entry):
        # Get the text and format to number
        text = entry.get()
        entry.delete(0, len(text))
        text = text.replace(",", "")
        entry.insert(0, f"{float(text):,.2f}")

        self.budget.categories[category] = float(text)

        # Update spending
        self.make_label(f"{self.budget.total_spending():<,.2f}", 1, self.column_money)
        # Update difference
        self.make_label(f"{self.budget.income - self.budget.total_spending():<,.2f}", 2, 2)

        print("Updated Category:", category, float(text))

    def income_frame(self):
        self.make_label("Income", 0, 0)
        self.dollar_sign(0)

        entry_income = tk.Entry(master=self.parent_frame, fg="white", bg="grey", width=self.width)
        entry_income.grid(row=0, column=2, sticky=tk.W)

        button = tk.Button(master=self.parent_frame, text="Save", command=partial(self.update_income, entry_income))
        button.grid(row=0, column=3, sticky=tk.W)

        self.make_label("Spending", 1, 0)
        self.dollar_sign(1)

        self.make_label(f"{self.budget.total_spending():<,.2f}", 1, 2)

        self.make_label("Difference", 2, 0)
        self.dollar_sign(2)

        self.fill_empty(3, 0)

        row_category = 4
        self.make_label("Categories", row_category, 0)

        entry_category = tk.Entry(master=self.parent_frame, fg="white", bg="grey", width=self.width)
        entry_category.grid(row=row_category, column=self.column_money, sticky=tk.W)

        button = tk.Button(master=self.parent_frame, text="Add Category", command=partial(self.add_category, entry_category, row_category))
        button.grid(row=row_category, column=3, sticky=tk.W)


if __name__ == "__main__":
    window = Window()
    window.income_frame()
