# TI-54-like Python Calculator — Documentation

This document explains the functionality of the `calculator.py` script, how to run it, usage examples for each operation, and a short explanation of the code that implements the behavior.

## Running

Start the interactive REPL:

```bash
python calculator.py
```

Run the built-in quick tests:

```bash
python calculator.py --test
```

You can also call the evaluator programmatically:

```bash
python -c "from calculator import evaluate, make_namespace; print(evaluate('log(100)', make_namespace('rad',0.0,0.0)))"
```

## Commands and Operations (with examples)

- Basic arithmetic
  - `+`, `-`, `*`, `/` with normal precedence and parentheses.
  - Example: `(2+3)*4` -> `20`

- Power and roots
  - `^` or `**` for power. Example: `2^3` or `2**3` -> `8`.
  - `sqrt(x)` for square root. Example: `sqrt(16)` -> `4`.

- Percent and factorial
  - `%` after a number turns it into a fraction: `50%` -> `0.5` (so `200 * 10%` -> `20`).
  - `factorial(n)` or `fact(n)` for `n!`. Example: `factorial(5)` -> `120`.

- Exponentials and logs
  - `exp(x)` = e**x. Example: `exp(1)` -> `e`.
  - `ln(x)` = natural log (base e). Example: `ln(exp(1))` -> `1`.
  - `log(x)` = base-10 log. Example: `log(100)` -> `2`.

- Trigonometry (respect angle mode)
  - `sin(x)`, `cos(x)`, `tan(x)` and inverses `asin`, `acos`, `atan`.
  - `sinh`, `cosh`, `tanh` available.
  - Use `deg` command to switch to degrees, `rad` to use radians.
  - Example: `deg` then `sin(30)` -> `0.5`.

- Other utilities
  - `pow(a,b)` is available as well. Example: `pow(2,3)` -> `8`.
  - `abs(x)`, `floor(x)`, `ceil(x)`.

- Memory & last answer
  - `ans` contains last computed result.
  - `mem` holds memory value.
  - `M+` adds `ans` to memory, `M-` subtracts `ans` from memory.
  - `MR` recalls memory (prints it and sets `ans`), `MC` clears memory.
  - Example flow: compute `5`, type `M+` (mem=5); compute `3`, `M+` (mem=8); `MR` -> prints `8` and sets `ans` to `8`.

## Evaluation notes and examples

- Parentheses group expressions: `2 * (1 + 3)`.
- Combine functions: `log(sqrt(100))` -> `1`.
- Use `ans` in expressions: after computing `5`, `2 * ans` -> `10`.

## Code overview — how it works

Key symbols in the code (see `calculator.py`):

- `make_namespace(angle_mode, memory, ans)`
  - Builds the function/variable namespace provided to the evaluator.
  - Provides constants `pi`, `e`, helper functions `sqrt`, `exp`, `log`, `ln`, etc.
  - Wraps trig functions so they respect `angle_mode` (`deg` or `rad`). When in degree mode, trig inputs are converted to radians and inverse results are converted back to degrees.

- `preprocess(expr: str) -> str`
  - Lightweight text rewrites before parsing:
    - replaces `^` with `**` so users can use `^` for power.
    - converts `50%` -> `(50/100)` so `%` works on numbers.
    - converts `5!` to `factorial(5)`.

- `SafeEval` (AST-based evaluator)
  - The evaluator uses Python's `ast` module to parse expressions in `eval` mode and walks the AST.
  - Only a restricted set of AST node types is allowed (literals, names, calls, binary/unary ops). Any other node raises an error.
  - `visit_Call` only allows direct function calls by name (no attribute access), and only functions present in the provided namespace may be called — this prevents arbitrary code execution.
  - Binary and unary operators are implemented explicitly (add, sub, mul, div, mod, pow, floor div, unary plus/minus). This keeps evaluation behavior predictable and safe.

- `evaluate(expr, namespace)`
  - Runs `preprocess`, parses the expression into an AST, then evaluates it with `SafeEval` using the provided `namespace` (from `make_namespace`).

- REPL (`repl()`)
  - Maintains `angle_mode`, `memory`, and `ans` across user commands.
  - Recognizes commands like `help`, `deg`, `rad`, `M+`, `M-`, `MR`, `MC`, `exit`.
  - On ordinary input, it builds a fresh namespace via `make_namespace(angle_mode, memory, ans)` and calls `evaluate`.

- `self_test()`
  - A small set of expressions used to validate core behaviors (`^`, `sqrt`, `log`, `%`, `factorial`).

## Security notes

- The evaluator deliberately avoids `eval()` on raw strings. Using the AST and a whitelist of nodes and names prevents executing arbitrary code and limits available operations to mathematical computations only.

## Extending the calculator

- To add new functions, export the function in `make_namespace` (e.g., add a safe wrapper for `math.gamma` as `gamma`).
- To add more operators, extend the `SafeEval` visitor methods and whitelist the corresponding AST node in `ALLOWED_NODES`.

## Files

- `calculator.py` — main script and REPL.
- `CALCULATOR.md` — this documentation.

---

If you'd like, I can also:
- Add a short README with usage shortcuts.
- Add unit tests for more functions.
- Provide a small GUI wrapper.
