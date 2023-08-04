from Budget import Budget
from functools import partial
import tkinter as tk

# Create the main window
window = tk.Tk()

# Set window title
window.title("My Budget")

# Set window dimensions
window.geometry("500x400")  # height x width

def fill_empty(parent, row, column):
    """Make an empty space for padding"""
    empty = tk.Label(parent)
    empty.grid(row=row, column=column)
    return empty


def dollar_sign(parent, row, column):
    """Make a dollar sign label"""
    label_dollar = tk.Label(master=parent, text=f"{'$':<{3}}")
    label_dollar.grid(row=row, column=column, sticky=tk.W)  # tk.W = align west or left, tk.W = align North or top, etc.
    return label_dollar


def setup_frame():
    """Setup frame and column dimensions"""
    frame = tk.Frame()
    frame.columnconfigure(0, minsize=30)
    frame.columnconfigure(1, minsize=5)
    frame.columnconfigure(2, minsize=30)
    frame.columnconfigure(3, minsize=30)
    return frame


def make_label(parent_frame, name, row, column, width=20):
    """Return a new label and place in frame grid"""
    label = tk.Label(master=parent_frame, text=f"{name:<{width}}")
    label.grid(row=row, column=column, sticky=tk.W)  # tk.W = align west or left, tk.W = align North or top, etc.
    return label


def add_category(budget, parent_frame, entry, start_row, amount=0.0):
    """Add a budget Category"""
    text = entry.get()

    budget.add_category(text, amount)
    row = len(myBudget.categories) + start_row

    make_label(parent_frame, text, row, 0, 20)
    dollar_sign(parent_frame, row, 1)

    entry_amount = tk.Entry(master=parent_frame, fg="white", bg="grey", width=20)
    entry_amount.insert(0, f"{myBudget.categories[text]:,.2f}")
    entry_amount.grid(row=row, column=2, sticky=tk.W)

    button = tk.Button(master=parent_frame, text="Save", command=partial(update_category, budget, text, parent_frame, entry_amount, 20))
    button.grid(row=row, column=3, sticky=tk.W)

    print("User added:", text)

    return entry_amount


def update_category(budget, category, parent_frame, entry, width):
    text = entry.get()
    text = text.replace(",", "")
    budget.categories[category] = float(text)

    # Update spending
    make_label(parent_frame, f"{budget.total_spending():<,.2f}", 1, 2, width)
    # Update difference
    make_label(parent_frame, f"{budget.income - budget.total_spending():<,.2f}", 2, 2, width)

    print("Updated Category:", category, float(text))


def update_income(budget, frame, entry, width):
    text = entry.get()
    text = text.replace(",", "")
    budget.adjust_income(float(text))
    make_label(frame, f"{myBudget.income - myBudget.total_spending():<,.2f}", 2, 2, width)
    print("Updated Income:", float(text))


def income_frame(budget: Budget):
    frame = setup_frame()

    column_width = 20

    make_label(frame, "Income", 0, 0, column_width)
    dollar_sign(frame, 0, 1)

    entry_income = tk.Entry(master=frame, fg="white", bg="grey", width=column_width)
    entry_income.grid(row=0, column=2, sticky=tk.W)

    button = tk.Button(master=frame, text="Save", command=partial(update_income, budget, frame, entry_income, column_width))
    button.grid(row=0, column=3, sticky=tk.W)

    make_label(frame, "Spending", 1, 0, column_width)
    dollar_sign(frame, 1, 1)

    make_label(frame, f"{myBudget.total_spending():<,.2f}", 1, 2, column_width)

    make_label(frame, "Difference", 2, 0, column_width)
    dollar_sign(frame, 2, 1)

    fill_empty(frame, 3, 0)

    row_category = 4
    make_label(frame, "Categories", row_category, 0, column_width)

    entry_category = tk.Entry(master=frame, fg="white", bg="grey", width=20)
    entry_category.grid(row=row_category, column=2, sticky=tk.W)

    button = tk.Button(master=frame, text="Add Category", command=partial(add_category, budget, frame, entry_category, row_category))
    button.grid(row=row_category, column=3, sticky=tk.W)

    return frame


myBudget = Budget()
frame_a = income_frame(myBudget)
frame_a.pack()

# Start the main event loop
window.mainloop()
