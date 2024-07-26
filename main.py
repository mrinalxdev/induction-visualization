import matplotlib.pyplot as plt
import numpy as np
import json
import os
import math
from matplotlib.widgets import Slider

def get_formula(prompt):
    """Prompts the user for a formula and returns a function that computes it."""
    formula = input(prompt)
    def formula_func(n):
        return eval(formula)
    return formula_func, formula

def base_case(base_n, base_formula):
    """Verifies the base case for n=base_n"""
    try:
        return base_formula(base_n)
    except Exception as e:
        print(f"Error in base case formula: {e}")
        return None

def induction_step(induction_hypothesis, induction_formula, k):
    """Verifies the induction step"""
    try:
        return induction_formula(k + 1) == induction_hypothesis(k) + (k + 1)
    except Exception as e:
        print(f"Error in induction step formula: {e}")
        return None

def visualize_induction(base_formula, induction_formula, max_n):
    """Visualizes the base case and induction step"""
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    x = np.arange(1, max_n + 1)
    y_formula = np.vectorize(base_formula)(x)
    y_induction = np.vectorize(induction_formula)(x)

    l1, = plt.plot(x, y_formula, label='Formula')
    l2, = plt.plot(x, y_induction, label='Induction Step')
    plt.xlabel('n')
    plt.ylabel('Value')
    plt.legend()
    plt.title('Mathematical Induction Visualization')

    axcolor = 'lightgoldenrodyellow'
    axmaxn = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    smaxn = Slider(axmaxn, 'Max n', 1, 100, valinit=max_n, valstep=1)

    def update(val):
        max_n = int(smaxn.val)
        x = np.arange(1, max_n + 1)
        y_formula = np.vectorize(base_formula)(x)
        y_induction = np.vectorize(induction_formula)(x)
        l1.set_xdata(x)
        l1.set_ydata(y_formula)
        l2.set_xdata(x)
        l2.set_ydata(y_induction)
        ax.relim()
        ax.autoscale_view()
        plt.draw()

    smaxn.on_changed(update)

    plt.show()

def save_formula(name, formula_str):
    """Saves the formula to a JSON file"""
    if os.path.exists("formulas.json"):
        with open("formulas.json", "r") as f:
            formulas = json.load(f)
    else:
        formulas = {}

    formulas[name] = formula_str

    with open("formulas.json", "w") as f:
        json.dump(formulas, f)

def load_formula(name):
    """Loads a formula from a JSON file"""
    if os.path.exists("formulas.json"):
        with open("formulas.json", "r") as f:
            formulas = json.load(f)
        if name in formulas:
            formula_str = formulas[name]
            def formula_func(n):
                return eval(formula_str)
            return formula_func, formula_str
    return None, None

def select_predefined_formula():
    """Displays a menu for selecting predefined formulas"""
    predefined_formulas = {
        "Sum of first n natural numbers": "n * (n + 1) // 2",
        "Sum of first n squares": "(n * (n + 1) * (2 * n + 1)) // 6",
        "Sum of first n cubes": "(n * (n + 1) // 2) ** 2"
    }

    print("Select a predefined formula:")
    for i, key in enumerate(predefined_formulas.keys(), 1):
        print(f"{i}. {key}")

    choice = int(input("Enter your choice: "))
    selected_key = list(predefined_formulas.keys())[choice - 1]
    formula_str = predefined_formulas[selected_key]
    def formula_func(n):
        return eval(formula_str)
    return formula_func, formula_str

def guided_mode():
    """Guides the user through the induction process step-by-step"""
    print("\nGuided Mode:")
    print("1. Select a predefined formula")
    print("2. Enter a custom formula")
    choice = input("Choose an option: ")

    if choice == "1":
        base_formula, base_formula_str = select_predefined_formula()
        induction_formula, induction_formula_str = base_formula, base_formula_str
    elif choice == "2":
        print("Enter the formula for the base case (e.g., 'n * (n + 1) // 2' for sum of natural numbers):")
        base_formula, base_formula_str = get_formula("Base case formula: ")

        print("\nEnter the formula for the induction step (e.g., 'n * (n + 1) // 2' for sum of natural numbers):")
        induction_formula, induction_formula_str = get_formula("Induction step formula: ")
    else:
        print("Invalid choice.")
        return

    # Verify the base case
    base_n = int(input("\nEnter the value of n for the base case (e.g., 1): "))
    base_result = base_case(base_n, base_formula)
    print(f"Base Case Verification for n={base_n}: {base_result}")

    if base_result is None:
        print("Base case verification failed.")
        return

    # Verify the induction step
    k = int(input("\nEnter the value of k for the induction step verification (e.g., 5): "))
    is_valid = induction_step(base_formula, induction_formula, k)
    print(f"Induction Step Verification for k={k}: {is_valid}")

    if not is_valid:
        print("Induction step verification failed. Here's a detailed breakdown:")
        try:
            k_plus_1 = induction_formula(k + 1)
            hypo_k = base_formula(k)
            print(f"Induction formula for k+1: {k_plus_1}")
            print(f"Induction hypothesis for k: {hypo_k}")
            print(f"Expected value for k+1: {hypo_k + (k + 1)}")
            print(f"Actual value for k+1: {k_plus_1}")
        except Exception as e:
            print(f"Error during induction step verification: {e}")
        return

    # Visualize the induction process
    max_n = int(input("\nEnter the maximum value of n for visualization (e.g., 10): "))
    visualize_induction(base_formula, induction_formula, max_n)

# Main Program
def main():
    while True:
        print("\nOptions:")
        print("1. Enter a new formula")
        print("2. Load a saved formula")
        print("3. Select a predefined formula")
        print("4. Guided mode")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            print("Enter the formula for the base case (e.g., 'n * (n + 1) // 2' for sum of natural numbers):")
            base_formula, base_formula_str = get_formula("Base case formula: ")

            print("\nEnter the formula for the induction step (e.g., 'n * (n + 1) // 2' for sum of natural numbers):")
            induction_formula, induction_formula_str = get_formula("Induction step formula: ")

            save = input("\nDo you want to save these formulas? (yes/no): ").strip().lower()
            if save == "yes":
                name = input("Enter a name for the formulas: ").strip()
                save_formula(name + "_base", base_formula_str)
                save_formula(name + "_induction", induction_formula_str)

        elif choice == "2":
            name = input("Enter the name of the formulas to load: ").strip()
            base_formula, base_formula_str = load_formula(name + "_base")
            induction_formula, induction_formula_str = load_formula(name + "_induction")
            if not base_formula or not induction_formula:
                print("Formulas not found.")
                continue

        elif choice == "3":
            base_formula, base_formula_str = select_predefined_formula()
            induction_formula, induction_formula_str = base_formula, base_formula_str

        elif choice == "4":
            guided_mode()
            continue

        elif choice == "5":
            break

        else:
            print("Invalid option. Please try again.")
            continue

        base_n = int(input("\nEnter the value of n for the base case (e.g., 1): "))
        base_result = base_case(base_n, base_formula)
        print("Base Case Verification:", base_result is not None and base_result == base_formula(base_n))

        # Verify the induction step
        k = int(input("\nEnter the value of k for the induction step verification (e.g., 5): "))
        is_valid = induction_step(base_formula, induction_formula, k)
        print("Induction Step Verification for k={}: {}".format(k, is_valid))

        if not is_valid:
            print("Induction step verification failed. Here's a detailed breakdown:")
            try:
                k_plus_1 = induction_formula(k + 1)
                hypo_k = base_formula(k)
                print(f"Induction formula for k+1: {k_plus_1}")
                print(f"Induction hypothesis for k: {hypo_k}")
                print(f"Expected value for k+1: {hypo_k + (k + 1)}")
                print(f"Actual value for k+1: {k_plus_1}")
            except Exception as e:
                print(f"Error during induction step verification: {e}")
        max_n = int(input("\nEnter the maximum value of n for visualization (e.g., 10): "))
        visualize_induction(base_formula, base_formula, max_n)

if __name__ == "__main__":
    main()
