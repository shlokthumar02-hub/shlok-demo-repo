#!/usr/bin/env python3
"""Simple scientific calculator (TI-54-like) with an interactive REPL.

Features:
- basic arithmetic: + - * / %% ^ (power using ^ or **)
- scientific: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh
- log (base 10), ln, exp, sqrt, pow, factorial (fact)
- angle modes: degrees <-> radians (use `deg` / `rad` commands)
- memory: M+, M-, MR, MC and `ans` variable for last answer

Run `python calculator.py` to start the REPL or `python calculator.py --test` for a quick self-test.
"""

import ast
import math
import operator as op
import re
import sys


def make_namespace(angle_mode, memory, ans):
	def maybe_angle(fn, inv=False):
		if inv:
			if angle_mode == 'deg':
				return lambda x: math.degrees(fn(math.radians(x)))
			return lambda x: fn(x)
		else:
			if angle_mode == 'deg':
				return lambda x: fn(math.radians(x))
			return lambda x: fn(x)

	ns = {
		# basic math
		'pi': math.pi,
		'e': math.e,
		'abs': abs,
		'sqrt': math.sqrt,
		'pow': pow,
		'exp': math.exp,
		'ln': math.log,
		'log': lambda x: math.log10(x),
		'floor': math.floor,
		'ceil': math.ceil,
		'factorial': math.factorial,
		'fact': math.factorial,
		# trig (wrappers respect angle_mode)
		'sin': maybe_angle(math.sin),
		'cos': maybe_angle(math.cos),
		'tan': maybe_angle(math.tan),
		'asin': maybe_angle(math.asin, inv=True),
		'acos': maybe_angle(math.acos, inv=True),
		'atan': maybe_angle(math.atan, inv=True),
		'sinh': math.sinh,
		'cosh': math.cosh,
		'tanh': math.tanh,
	}
	# runtime values
	ns['ans'] = ans
	ns['mem'] = memory
	return ns


class SafeEval(ast.NodeVisitor):
	ALLOWED_NODES = (
		ast.Expression,
		ast.BinOp,
		ast.UnaryOp,
		ast.Num,
		ast.Constant,
		ast.Call,
		ast.Load,
		ast.Name,
		ast.Pow,
		ast.Add,
		ast.Sub,
		ast.Mult,
		ast.Div,
		ast.Mod,
		ast.USub,
		ast.UAdd,
		ast.FloorDiv,
		ast.LShift,
		ast.RShift,
		ast.BitOr,
		ast.BitXor,
		ast.BitAnd,
		ast.MatMult,
	)

	def __init__(self, names):
		self.names = names

	def visit(self, node):
		if not isinstance(node, self.ALLOWED_NODES):
			raise ValueError(f"Unsupported expression: {type(node).__name__}")
		return super().visit(node)

	def visit_Expression(self, node):
		return self.visit(node.body)

	def visit_Constant(self, node):
		return node.value

	def visit_Num(self, node):
		return node.n

	def visit_Name(self, node):
		if node.id in self.names:
			return self.names[node.id]
		raise NameError(f"Use of unknown identifier: {node.id}")

	def visit_BinOp(self, node):
		left = self.visit(node.left)
		right = self.visit(node.right)
		op_type = type(node.op)
		if op_type is ast.Add:
			return left + right
		if op_type is ast.Sub:
			return left - right
		if op_type is ast.Mult:
			return left * right
		if op_type is ast.Div:
			return left / right
		if op_type is ast.Mod:
			return left % right
		if op_type is ast.Pow:
			return left ** right
		if op_type is ast.FloorDiv:
			return left // right
		raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

	def visit_UnaryOp(self, node):
		operand = self.visit(node.operand)
		if isinstance(node.op, ast.UAdd):
			return +operand
		if isinstance(node.op, ast.USub):
			return -operand
		raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

	def visit_Call(self, node):
		if not isinstance(node.func, ast.Name):
			raise ValueError("Only direct function calls are allowed")
		func_name = node.func.id
		if func_name not in self.names:
			raise NameError(f"Function not allowed: {func_name}")
		func = self.names[func_name]
		args = [self.visit(a) for a in node.args]
		return func(*args)


def preprocess(expr: str) -> str:
	expr = expr.strip()
	expr = expr.replace('^', '**')
	# simple percentage: 50% -> (50/100)
	expr = re.sub(r'(?P<num>\d+(?:\.\d+)?)\%', r'(\g<num>/100)', expr)
	# simple factorial on numbers like 5! -> factorial(5)
	expr = re.sub(r'(?P<num>\d+(?:\.\d+)?)!', r'factorial(\g<num>)', expr)
	return expr


def evaluate(expr: str, namespace: dict):
	expr = preprocess(expr)
	tree = ast.parse(expr, mode='eval')
	se = SafeEval(namespace)
	return se.visit(tree)


REPL_BANNER = "TI-54-like Python calculator. Type `help` for commands."


def print_help():
	print("Commands and usage:")
	print("  help          Show this detailed help")
	print("  exit / quit   Leave the REPL")
	print("")
	print("Basic arithmetic:")
	print("  +, -, *, /    Standard precedence and parentheses")
	print("    Example: (2+3)*4  -> 20")
	print("")
	print("Power and roots:")
	print("  ^ or **       Power operator")
	print("    Example: 2^3  -> 8")
	print("  sqrt(x)       Square root")
	print("    Example: sqrt(16)  -> 4")
	print("")
	print("Percent and factorial:")
	print("  50%           Percent is interpreted as 0.5")
	print("    Example: 200 * 10%  -> 20")
	print("  fact(n) or factorial(n)  Factorial")
	print("    Example: factorial(5)  -> 120")
	print("")
	print("Exponentials and logs:")
	print("  exp(x)        e**x")
	print("    Example: exp(1)  -> e")
	print("  ln(x)         Natural logarithm (base e)")
	print("    Example: ln(exp(1))  -> 1")
	print("  log(x)        Base-10 logarithm")
	print("    Example: log(100)  -> 2")
	print("")
	print("Trigonometric functions (respect angle mode):")
	print("  sin(x), cos(x), tan(x)      Standard trig")
	print("  asin(x), acos(x), atan(x)   Inverse trig (returns angle)")
	print("  sinh(x), cosh(x), tanh(x)   Hyperbolic")
	print("  Use `deg` to switch to degrees mode, `rad` for radians")
	print("    Example (deg): deg then sin(30)  -> 0.5")
	print("")
	print("Other utilities:")
	print("  pow(a,b)      a to the power b")
	print("    Example: pow(2,3)  -> 8")
	print("  abs(x), floor(x), ceil(x)  Standard helpers")
	print("")
	print("Memory and last answer:")
	print("  ans           Last computed result")
	print("  mem           Stored memory value")
	print("  M+            Add `ans` to memory (mem += ans)")
	print("  M-            Subtract `ans` from memory (mem -= ans)")
	print("  MR            Recall memory (prints mem and sets ans=mem)")
	print("  MC            Clear memory (mem = 0)")
	print("    Example: compute 5, M+ (mem becomes 5), compute 3, M+ (mem becomes 8), MR -> prints 8")
	print("")
	print("Evaluation notes:")
	print("  - Use parentheses for grouping: ( ... )")
	print("  - You can combine functions: log( sqrt(100) )")
	print("  - Use `ans` in expressions: 2 * ans")
	print("")
	print("Examples summary:")
	print("  log(100)           -> 2")
	print("  ln(exp(1))         -> 1")
	print("  2^3 or pow(2,3)    -> 8")
	print("  50%                -> 0.5")
	print("  factorial(5)       -> 120")
	print("  deg; sin(30)       -> 0.5")
	print("  M+, M-, MR, MC     memory operations")


def repl():
	angle_mode = 'rad'
	memory = 0.0
	ans = 0.0
	print(REPL_BANNER)
	while True:
		try:
			line = input('> ').strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if not line:
			continue
		cmd = line.lower()
		if cmd in ('exit', 'quit'):
			break
		if cmd == 'help':
			print_help()
			continue
		if cmd == 'deg':
			angle_mode = 'deg'
			print('Angle mode: degrees')
			continue
		if cmd == 'rad':
			angle_mode = 'rad'
			print('Angle mode: radians')
			continue
		# Memory commands
		if cmd == 'm+':
			memory += ans
			print(f'mem = {memory}')
			continue
		if cmd == 'm-':
			memory -= ans
			print(f'mem = {memory}')
			continue
		if cmd == 'mr':
			print(memory)
			ans = memory
			continue
		if cmd == 'mc':
			memory = 0.0
			print('mem cleared')
			continue

		ns = make_namespace(angle_mode, memory, ans)
		try:
			result = evaluate(line, ns)
		except Exception as e:
			print('Error:', e)
			continue
		ans = result
		print(result)


def self_test():
	print('Running quick self-test...')
	tests = [
		('2+3*4', 14),
		('(2+3)*4', 20),
		('2^3', 8),
		('sqrt(16)', 4),
		('log(100)', 2),
		('ln(exp(1))', 1),
		('50%', 0.5),
		('factorial(5)', 120),
	]
	failures = 0
	for expr, expected in tests:
		try:
			got = evaluate(expr, make_namespace('rad', 0.0, 0.0))
		except Exception as e:
			print(expr, '-> Error:', e)
			failures += 1
			continue
		if abs(got - expected) > 1e-9:
			print(expr, 'Expected', expected, 'Got', got)
			failures += 1
		else:
			print(expr, 'OK')
	if failures:
		print(f'{failures} tests failed')
		sys.exit(2)
	print('All tests passed')


if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] in ('--test', 'test'):
		self_test()
	else:
		repl()
