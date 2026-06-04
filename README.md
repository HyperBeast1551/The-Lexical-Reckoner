# The Lexical Reckoner
> **"Its your usual calculator but with a twist."**

**The Lexical Reckoner** is an advanced linguistic computation engine. Version 2.0 update introduces a smarter interface that can forgive your typos, remember your history, and display everything in a beautiful, colorized terminal environment.

---

## Demo..!



https://github.com/user-attachments/assets/3e35429c-17e9-4c2e-b86f-913efe1ed486



---

## What’s New in the v2.0 update?

- **Auto-Fix (Fuzzy Matching):** Made a typo? The Reckoner uses `difflib` to understand what you meant. If you type *"fvie plsu ten"*, it intelligently corrects it to *"five plus ten"*.
- **Memory Recall:** Use the keyword **"previous"** to carry your last result into a new calculation.  
  - *Example: "five plus five" -> "ten". Then: "previous times two" -> "twenty".*
- **Colorized Interface:** Powered by `colorama`. Successes are in **Green**, errors in **Red**, and the interface stays crisp and readable in **Cyan**.
- **Improved Parsing:** Better handling of square roots and complex expressions.

---

## Installation
> **"Latest version of Python and Git must be installed before hand."**

The Reckoner now requires three libraries to reach its full potential.

### 1. Clone the repository

```bash
git clone https://github.com/HyperBeast1551/The-Lexical-Reckoner.git
cd The-Lexical-Reckoner
```

### 2. Install the dependencies

```bash
pip install word2number num2words colorama
```

### 3. Run the program

```bash
python main.py
```

---

## Usage Examples

| Scenario | Input | Result |
|---|---|---|
| Basic Math | `twelve times twelve` | `one hundred and forty-four` |
| Typo Correction | `ten plsu fvie` | `fifteen` |
| Memory Usage | `previous divided by three` | `(Uses last answer)` |
| Advanced | `square root of sixty four` | `nine` |

---

## Supported Operations

| Operation | Verbal Commands | Symbols |
|---|---|---|
| Addition | plus, add | `+` |
| Subtraction | minus, subtract | `-` |
| Multiplication | times, multiplied by | `*` |
| Division | divided by, over | `/` |
| Exponents | power, to the power of | `**` |
| Square Root | square root, square root of | `sqrt` |
| Modulo | mod, modulo | `%` |

---

## How it Works

- **Fuzzy Correction:** The script compares every word against a known vocabulary of numbers and operators.
- **Linguistic Translation:** Words are converted to integers using `word2number`.
- **Safe Evaluation:** The expression is sanitized and evaluated using Python's `math` library.
- **Verbalization:** The numeric result is converted back into English prose via `num2words`.

---

## License

This project is licensed under the MIT License.
