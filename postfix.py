from constants import (
	INTEGER, VARIABLE, RIM, EOF,
	PLUS, MINUS, MUL, DIV,
	ASSIGN,
	LESS, GREATER, EQUAL, NOT_EQUAL, LESS_EQ, GREATER_EQ,
)
from rim import parse_rim


class Postfix:
	def __init__(self, lexer, variables):
		self.lexer = lexer
		self.current_token = self.lexer.get_next_token()
		self.variables = variables
		self.stack = []

	def error(self):
		raise Exception('Greska u parsiranju')

	def eat(self, type):
		if self.current_token.type == type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error()

	def get_from_stack(self, pop=True):
		if pop:
			value = self.stack.pop()
		else:
			value = self.stack[-1]

		if type(value) is str:
			return self.variables[value]

		return value

	def parse(self):
		token = self.current_token
		result = None

		while token.type is not EOF:
			if token.type in (PLUS, MINUS, MUL, DIV):
				right = self.get_from_stack()
				left = self.get_from_stack()
				if token.type == PLUS:
					self.stack.append(left + right)
					self.eat(PLUS)
				elif token.type == MINUS:
					self.stack.append(left - right)
					self.eat(MINUS)
				elif token.type == MUL:
					self.stack.append(left * right)
					self.eat(MUL)
				elif token.type == DIV:
					self.stack.append(round(left / right))
					self.eat(DIV)
			elif token.type == ASSIGN:
				value = self.get_from_stack()
				variable = self.stack.pop()
				self.variables[variable] = value
				self.stack.append(value)
				self.eat(ASSIGN)
			elif token.type == RIM:
				number = parse_rim(self, self.lexer)
				self.stack.append(number)
			elif token.type == INTEGER:
				self.stack.append(token.value)
				self.eat(INTEGER)
			elif token.type == VARIABLE:
				self.stack.append(token.value)
				self.eat(VARIABLE)
			elif token.type == LESS:
				right = self.get_from_stack()
				left = self.get_from_stack(False)
				if result in (None, True):
					result = left < right
				self.eat(LESS)
			elif token.type == GREATER:
				right = self.get_from_stack()
				left = self.get_from_stack(False)
				if result in (None, True):
					result = left > right
				self.eat(GREATER)
			elif token.type == LESS_EQ:
				right = self.get_from_stack()
				left = self.get_from_stack(False)
				if result in (None, True):
					result = left <= right
				self.eat(LESS_EQ)
			elif token.type == GREATER_EQ:
				right = self.get_from_stack()
				left = self.get_from_stack(False)
				if result in (None, True):
					result = left >= right
				self.eat(GREATER_EQ)
			elif token.type == EQUAL:
				right = self.get_from_stack()
				left = self.get_from_stack(False)
				if result in (None, True):
					result = left == right
				self.eat(EQUAL)
			elif token.type == NOT_EQUAL:
				right = self.get_from_stack()
				left = self.get_from_stack(False)
				if result in (None, True):
					result = left != right
				self.eat(NOT_EQUAL)

			token = self.current_token

		if result is None:
			return self.get_from_stack(), self.variables
		else:
			return result, self.variables

