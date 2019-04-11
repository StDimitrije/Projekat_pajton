from constants import (
	INTEGER, VARIABLE, RIM,
	PLUS, MINUS, MUL, DIV,
	ASSIGN,
	LESS, GREATER, EQUAL, NOT_EQUAL, LESS_EQ, GREATER_EQ,
)
from rim import parse_rim


class Prefix():
	def __init__(self, lexer, variables):
		self.lexer = lexer
		self.current_token = self.lexer.get_next_token()
		self.variables = variables

	def error(self):
		raise Exception('Greska pri parsiranju.')

	def eat(self, type):
		if self.current_token.type == type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error()

	def expr(self):
		token = self.current_token
		if token.type == PLUS:
			self.eat(PLUS)
			left, _ = self.expr()
			right, _ = self.expr()
			return left + right, None
		elif token.type == MINUS:
			self.eat(MINUS)
			left, _ = self.expr()
			right, _ = self.expr()
			return left - right, None
		elif token.type == MUL:
			self.eat(MUL)
			left, _ = self.expr()
			right, _ = self.expr()
			return left * right, None
		elif token.type == DIV:
			self.eat(DIV)
			left, _ = self.expr()
			right, _ = self.expr()
			return round(left / right), None
		elif token.type == ASSIGN:
			self.eat(ASSIGN)
			variable = self.current_token.value
			self.eat(VARIABLE)
			result, _ = self.expr()
			self.variables[variable] = result
			return result, None
		elif token.type == RIM:
			return parse_rim(self, self.lexer), None
		elif token.type == INTEGER:
			self.eat(INTEGER)
			return token.value, None
		elif token.type == VARIABLE:
			self.eat(VARIABLE)
			return self.variables[token.value], None
		elif token.type == LESS:
			self.eat(LESS)
			left, left_result = self.expr()
			right, right_result = self.expr()
			return left, left < right and left_result in (None, True) and right_result in (None, True)
		elif token.type == GREATER:
			self.eat(GREATER)
			left, left_result = self.expr()
			right, right_result = self.expr()
			return left, left > right and left_result in (None, True) and right_result in (None, True)
		elif token.type == LESS_EQ:
			self.eat(LESS_EQ)
			left, left_result = self.expr()
			right, right_result = self.expr()
			return left, left <= right and left_result in (None, True) and right_result in (None, True)
		elif token.type == GREATER_EQ:
			self.eat(GREATER_EQ)
			left, left_result = self.expr()
			right, right_result = self.expr()
			return left, left >= right and left_result in (None, True) and right_result in (None, True)
		elif token.type == EQUAL:
			self.eat(EQUAL)
			left, left_result = self.expr()
			right, right_result = self.expr()
			return left, left == right and left_result in (None, True) and right_result in (None, True)
		elif token.type == NOT_EQUAL:
			self.eat(NOT_EQUAL)
			left, left_result = self.expr()
			right, right_result = self.expr()
			return left, left != right and left_result in (None, True) and right_result in (None, True)

	def parse(self):
		exp, result = self.expr()

		if result is not None:
			return result, self.variables

		return exp, self.variables

