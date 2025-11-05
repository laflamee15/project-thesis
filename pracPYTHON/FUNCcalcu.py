def calc(a, b, operator):
    try:
        if operator == '+':
            result = a + b
        elif operator == '-':
            result = a - b
        elif operator == '/':
            result = a / b
        elif operator == '*':
            result = a * b
        else:
            raise ValueError("Invalid operator. Try Again.")
    except ZeroDivisionError:
        print(f"Cannot be divided by zero")
    else:
        print(f"Result: {result}")
    finally:
        print("Calculation Complete")
try:
    num1 = int(input("Enter numerator: "))
    num2 = int(input("Enter denominator: "))
    op = input("Enter your operator (+, -, /, *): ")
    calc(num1, num2, op)
except ValueError:
    print("Invalid input")