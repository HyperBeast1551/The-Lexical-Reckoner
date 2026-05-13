import re
import math
import sys
import difflib

from colorama import init

try:
    from word2number import w2n
    from num2words import num2words
    from colorama import Fore, Style, init
    # Initialize colorama to automatically reset colors after each print
    init(autoreset=True)
except ImportError:
    print("Missing dependencies! Please run: pip install word2number num2words colorama")
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
    'divide by': '/',
    'over': '/',
    'to the power of': '**',
    'power': '**',
    'modulo': '%',
    'mod': '%'
    }

# Build a vocabulary list for fuzzy matching (includes operators and number-words)
VOCABULARY = set([
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
    'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
    'hundred', 'thousand', 'million', 'billion', 'previous', 'square', 'root'
])
# Add operator words to the vocabulary
for phrase in OPERATOR_MAP.keys():
    for word in phrase.split():
        VOCABULARY.add(word)

def display_help():
    print(Fore.YELLOW + "\n--- HELP MENU ---")
    print("How to use:")
    print("  Type your math equation using words or standard symbols.")
    print("  Press Enter to calculate.\n")

    print("Special Features:")
    print("  Memory:      Use the word 'previous' to insert your last answer.")
    print("  Auto-Fix:    Slight typos will be auto-corrected (e.g., 'plsu' instead of 'plus').\n")

    print("Supported Operators (Words):")
    print("  Addition:       plus, add")
    print("  Subtraction:    minus, subtract")
    print("  Multiplication: times, multiplied by, multiply by")
    print("  Division:       divided by, divide by, over")
    print("  Exponents:      power, to the power of")
    print("  Square Root:    sqrt, square root of")
    print("  Modulo:         mod, modulo\n")

    print("Supported Operators (Symbols):")
    print("  +, -, *, /, **, %, ( )\n")

    print("Tips:")
    print("  - You can mix words and symbols in the same equation (e.g., 'five * six').")
    print("  - Use parentheses to control the order of operations (e.g., '(two plus two) times three').")
    print("  - Type 'exit' or 'quit' to close the calculator.")
    print("----------------------------------------------------------------------------------------------\n")

def correct_typos(text):
    """Checks alphabetical words against known vocabulary and fixes minor typos."""
    words = text.split()
    corrected_words = []
    for w in words:
        # Only attempt to fuzzy match purely alphabetical words
        if re.match(r'^[a-z]+$', w):
            matches = difflib.get_close_matches(w, VOCABULARY, n=1, cutoff=0.7)
            if matches:
                corrected_words.append(matches[0])
            else:
                corrected_words.append(w)
        else:
            corrected_words.append(w)
    return " ".join(corrected_words)
                    
def translate_and_calculate(user_input, previous_value):
    # Normalize input
    text = user_input.lower().strip()

    # Remove filler words that don't affect calculation (e.g., "and")
    text = re.sub(r'\band\b', ' ', text)

    # Step 1: Correct typos using fuzzy matching
    text = correct_typos(text)

    # Replace hyphens with spaces to handle cases like "twenty-one"
    text = text.replace('-', ' ')

    # Normalize whitespace to a single space
    text = re.sub(r'\s+', ' ', text)  

    # Step 2: Handle memory variable ("previous")
    if 'previous' in text:
        if previous_value is None:
            return "error: no previous calculation in memory", None, True
        # Substitute 'previous' with the raw numeric value of the last calculation
        text = text.replace('previous', str(previous_value))

    # Step 3: Handle "square root" phrases before mapping operators
    text = text.replace('square root of', 'sqrt')
    text = text.replace('square root', 'sqrt')

    # Step 4: Replace word operators with symbols
    for word, symbol in OPERATOR_MAP.items():
        text = re.sub(rf'\b{word}\b', symbol, text)

    # Step 5: Split the expression
    parts = re.split(r'(sqrt|\*\*|\+|\-|\*|\/|%|\(|\))', text)

    math_expression = ""

    # Step 6: Translate words back to digits
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

    # Step 7: Evaluate the mathematical expression safely 
    try:
        safe_math = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}

        result = eval(math_expression, {"__builtins__": None}, safe_math)

        # Format cleanup: 2.0 to 2 so output isn't "two pont zero"
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        # Step 8: Convert the final digit result back to words
        return num2words(result), result, False

    except ZeroDivisionError:
        return "infinity (division by zero)", None, True
    except Exception as e:
        return "error: invalid mathematical expression", None, True

def main():
    print(Fore.CYAN + Style.BRIGHT + "===========================================")
    print(Fore.CYAN + Style.BRIGHT + "      Welcome to The Lexical Reckoner       ")
    print(Fore.CYAN + Style.BRIGHT + "===========================================")
    print(Fore.LIGHTBLACK_EX + "Example: 'one hundred plus twenty two'")
    print(Fore.LIGHTBLACK_EX + "Example: 'square root of sixteen'")
    print(Fore.LIGHTBLACK_EX + "Type 'help' for operators and tips.\n")
    print(Fore.LIGHTBLACK_EX + "Type 'exit' or 'quit' to close the calculator.\n")

    previous_value = None

    while True:
        try:
            user_input = input(Fore.CYAN + "Calc > " + Style.RESET_ALL)

            # Check for help command
            if user_input.lower() == 'help':
                display_help()
                continue

            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                print(Fore.YELLOW + "Goodbye!")
                break

            if not user_input.strip():
                continue

            # Run the calculation engine
            str_result, raw_number, is_error = translate_and_calculate(user_input, previous_value)

            # Colourize the output based on success or error
            if is_error:
                print(Fore.RED + f"Result: {str_result}")
            else:
                print(Fore.GREEN + f"Result: {str_result}")
                # Save successful result to memory
                previous_value = raw_number

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nGoodbye!")
            break

if __name__ == "__main__":
    main()