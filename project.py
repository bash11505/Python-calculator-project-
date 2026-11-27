import ast
import operator
import tkinter as tk
from tkinter import messagebox


binary_ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
unary_ops = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def evaluate(text):
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in binary_ops:
            right = visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError
            return binary_ops[type(node.op)](visit(node.left), right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_ops:
            return unary_ops[type(node.op)](visit(node.operand))
        raise ValueError

    return visit(ast.parse(text, mode="eval"))


def press(value):
    current = expression.get()
    if value == "C":
        expression.set("")
    elif value == "⌫":
        expression.set(current[:-1])
    else:
        expression.set(current + value)


def calculate():
    try:
        expression.set(str(evaluate(expression.get())))
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
        messagebox.showerror("Calculation error", "Enter a valid expression.")


def keyboard(event):
    if event.char in "0123456789.+-*/()%":
        press(event.char)
    elif event.keysym == "Return":
        calculate()
    elif event.keysym == "BackSpace":
        press("⌫")
    elif event.keysym == "Escape":
        press("C")


root = tk.Tk()
root.title("Calculator")
root.resizable(False, False)
expression = tk.StringVar()
tk.Entry(root, textvariable=expression, font=("Arial", 22),
         justify="right", state="readonly", width=18
         ).grid(row=0, column=0, columnspan=4, padx=10, pady=10)

keys = [
    ("C", 1, 0), ("⌫", 1, 1), ("%", 1, 2), ("/", 1, 3),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
    ("0", 5, 0), (".", 5, 1), ("(", 5, 2), (")", 5, 3),
]
for text, column , row  in keys:
    tk.Button(root, text=text, width=5, height=2, font=("Arial", 14),
              command=lambda value=text: press(value)
              ).grid(row=row, column=column, padx=3, pady=3)
tk.Button(root, text="=", width=24, height=2, font=("Arial", 14),
          command=calculate
          ).grid(row=6, column=0, columnspan=4, padx=5, pady=5)
root.bind("<Key>", keyboard)
root.mainloop()
