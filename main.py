import re
import math
import sys

try:
    from word2number import w2n
    from num2words import num2words
except ImportError:
    print("Missing dependencies! Please run: pip install word2number num2words")
    sys.exit(1)

# Map conversational operators to mathematical symbols
OPERATOR_MAP = {
    'plus': '+',
    'add': '+',
    'minus': '-',
    'subtract': '-',
    'times': '*',
    'multiplied by': '*',
    'multiply by': '*',
    'divided by': '/',
    'over': '/',
    'to the power of': '**',
    'power': '**',
    'modulo': '%',
    'mod': '%'
    }

def display_help():
    print("\n--- HELP MENU ---")
    print("How to use:")
    print("  Type your math equation using words or standard symbols.")
    print("  Press Enter to calculate.\n")

    print("Supported Operators (Words):")
    print("  Addition:      plus, add")
    print("  Subtraction:   minus, subtract")
    print("  Multiplication: times, multiplied by, multiply by")
    print("  Division:      divided by, over")
    print("  Exponents:     power, to the power of")
    print("Square Root:     sqrt, square root of")
    print("  Modulo:        mod, modulo\n")

    print("Supported Operators (Symbols):")
    print("  +, -, *, /, **, %, ( )\n")

    print("Tips:")
    print("  - You can mix words and symbols in the same equation (e.g., 'five * six').")
    print("  - Use parentheses to control the order of operations (e.g., '(two plus two) times three').")
    print("  - Type 'exit' or 'quit' to close the calculator.")
    print("-----------------\n")

def translate_and_calculate(user_input):
    text = user_input.lower().strip()

    # Handle "square root" phrases before mapping operators
    text = text.replace('square root of', 'sqrt')
    text = text.replace('square root', 'sqrt')

    # Step 1: Replace word operators with symbols
    for word, symbol in OPERATOR_MAP.items():
        text = re.sub(rf'\b{word}\b', symbol, text)

    # Step 2: Split the exprssion
    parts = re. split(r'(sqrt|\*\*|\+|\-|\*|\/|%|\(|\))', text)

    math_expression = ""

    # Step 3: trancilate words back int digits
    for part in parts: 
        part = part.strip()
        if not part:
            continue

        if part in ['+', '-', '*', '/', '**', '%', '(', ')', 'sqrt']:
            math_expression += part
        else:
            try:
                num = w2n.word_to_num(part)
                math_expression += str(num)
            except ValueError:
                math_expression += part

    # Fix function syntax before evaluating (e.g., turning "sqrt 4" into "sqrt(4)")
    math_expression = re.sub(r'sqrt\s*(\d+(?:\.\d+)?)', r'sqrt(\1)', math_expression)

    # Step 4: evaluate the mathematical expression safely 
    try:
        safe_math = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}

        result = eval(math_expression, {"__builtins__": None}, safe_math)

        # Format cleanup: 2.0 to 2 so output isn't "two pont zero"
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        # Step 5: Convert the final digit result back to words
        result num2words(result)

    except ZeroDivisionError:
        return "infinity (division by zero)"
    except Exception as e:
        return "error: invalid mathematical expression"
    
def main():
    print("============================================")
    print("      Welcome to The Lexical Reckoner!      ")
    print("============================================")
    print("Example: 'one hundred plus twenty two'")
    print("Example: 'square root of sixteen'")
    print("Type 'help' for operators and tips.\n")
    print("Type 'exit' or 'quit' to close the calculator.\n")

    while True:
        try:
            user_input = input("Calc > ")

            # Check for help command
            if user_input.lower() == 'help':
                display_help()
                continue

            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            if not user_input.strip():
                continue

            result = translate_and_calculate(user_input)
            print(f"Result: {result}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()

        