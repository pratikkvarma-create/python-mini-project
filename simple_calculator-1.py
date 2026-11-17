"""
Simple GUI Calculator
A beginner-friendly calculator built with Python's Tkinter library.

Features:
- Addition, subtraction, multiplication, division, modulus, and powers
- Parentheses and decimal numbers
- Clear, backspace, and keyboard support
- Safe expression evaluation (does not use eval)
"""

import ast
import operator
import tkinter as tk
from tkinter import messagebox


# Only these mathematical operations are allowed.
BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate_expression(expression):
    """Safely calculate an arithmetic expression."""
    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate_node(tree.body)

        if isinstance(result, complex):
            raise ValueError("Complex results are not supported.")

        if isinstance(result, float) and (result != result or abs(result) == float("inf")):
            raise ValueError("The result is too large.")

        return result
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero.")
    except (SyntaxError, TypeError, OverflowError):
        raise ValueError("Invalid calculation.")
    except RecursionError:
        raise ValueError("Calculation is too complex.")


def _evaluate_node(node):
    """Evaluate only approved numeric and arithmetic AST nodes."""
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPERATORS:
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)

        # Prevent accidentally enormous power calculations.
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent is too large.")

        return BINARY_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPERATORS:
        return UNARY_OPERATORS[type(node.op)](_evaluate_node(node.operand))

    raise ValueError("Invalid calculation.")


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Python Calculator")
        self.root.geometry("360x520")
        self.root.minsize(320, 460)
        self.root.configure(bg="#171923")

        self.expression = ""
        self.just_calculated = False

        self.display_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="Ready")

        self.create_widgets()
        self.root.bind("<Key>", self.handle_keyboard)

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="PYTHON CALCULATOR",
            font=("Arial", 15, "bold"),
            bg="#171923",
            fg="#E2E8F0",
            pady=14,
        )
        title.pack(fill="x")

        display_frame = tk.Frame(self.root, bg="#242938", padx=14, pady=18)
        display_frame.pack(fill="x", padx=16, pady=(4, 12))

        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 27),
            justify="right",
            state="readonly",
            readonlybackground="#242938",
            fg="#FFFFFF",
            bd=0,
            insertwidth=0,
        )
        self.display.pack(fill="x", ipady=10)

        status = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg="#171923",
            fg="#A0AEC0",
            anchor="e",
            padx=20,
        )
        status.pack(fill="x", pady=(0, 8))

        button_frame = tk.Frame(self.root, bg="#171923")
        button_frame.pack(expand=True, fill="both", padx=16, pady=(0, 16))

        for column in range(4):
            button_frame.columnconfigure(column, weight=1, uniform="column")
        for row in range(5):
            button_frame.rowconfigure(row, weight=1, uniform="row")

        buttons = [
            ("C", 0, 0, "#C05621", self.clear),
            ("⌫", 0, 1, "#4A5568", self.backspace),
            ("(", 0, 2, "#4A5568", lambda: self.add_to_expression("(")),
            (")", 0, 3, "#4A5568", lambda: self.add_to_expression(")")),

            ("7", 1, 0, "#2D3748", lambda: self.add_to_expression("7")),
            ("8", 1, 1, "#2D3748", lambda: self.add_to_expression("8")),
            ("9", 1, 2, "#2D3748", lambda: self.add_to_expression("9")),
            ("÷", 1, 3, "#2B6CB0", lambda: self.add_to_expression("/")),

            ("4", 2, 0, "#2D3748", lambda: self.add_to_expression("4")),
            ("5", 2, 1, "#2D3748", lambda: self.add_to_expression("5")),
            ("6", 2, 2, "#2D3748", lambda: self.add_to_expression("6")),
            ("×", 2, 3, "#2B6CB0", lambda: self.add_to_expression("*")),

            ("1", 3, 0, "#2D3748", lambda: self.add_to_expression("1")),
            ("2", 3, 1, "#2D3748", lambda: self.add_to_expression("2")),
            ("3", 3, 2, "#2D3748", lambda: self.add_to_expression("3")),
            ("−", 3, 3, "#2B6CB0", lambda: self.add_to_expression("-")),

            ("0", 4, 0, "#2D3748", lambda: self.add_to_expression("0")),
            (".", 4, 1, "#2D3748", lambda: self.add_to_expression(".")),
            ("=", 4, 2, "#2F855A", self.calculate),
            ("+", 4, 3, "#2B6CB0", lambda: self.add_to_expression("+")),
        ]

        for label, row, column, color, command in buttons:
            button = tk.Button(
                button_frame,
                text=label,
                command=command,
                font=("Arial", 17, "bold"),
                bg=color,
                fg="#FFFFFF",
                activebackground="#718096",
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                cursor="hand2",
            )
            button.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=4,
                pady=4,
                ipadx=2,
                ipady=8,
            )

    def add_to_expression(self, value):
        if self.just_calculated and value not in "+-*/%":
            self.expression = ""

        self.just_calculated = False
        self.expression += value
        self.display_var.set(self.expression or "0")
        self.status_var.set("Enter an expression")

    def clear(self):
        self.expression = ""
        self.just_calculated = False
        self.display_var.set("0")
        self.status_var.set("Cleared")

    def backspace(self):
        self.expression = self.expression[:-1]
        self.just_calculated = False
        self.display_var.set(self.expression or "0")
        self.status_var.set("Ready")

    def calculate(self):
        if not self.expression:
            return

        try:
            result = calculate_expression(self.expression)
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.expression = str(result)
            self.display_var.set(self.expression)
            self.status_var.set("Calculation successful")
            self.just_calculated = True
        except ValueError as error:
            self.display_var.set("Error")
            self.status_var.set(str(error))
            self.expression = ""
            self.just_calculated = False

    def handle_keyboard(self, event):
        char = event.char

        if char in "0123456789.+-*/()%":
            self.add_to_expression(char)
        elif event.keysym in ("Return", "KP_Enter"):
            self.calculate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear()


if __name__ == "__main__":
    window = tk.Tk()
    app = Calculator(window)
    window.mainloop()
