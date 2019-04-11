from constants import (
	INTEGER, VARIABLE, RIM,
	PLUS, MINUS, MUL, DIV,
	RPAREN, LPAREN, ASSIGN,
	LESS, GREATER, EQUAL, NOT_EQUAL, LESS_EQ, GREATER_EQ,
)
from rim import parse_rim


class Infix():
	def __init__(self, lexer, variables):
		self.lexer = lexer
		self.current_token = self.lexer.get_next_token()
		self.variables = variables

	def error(self):
		raise Exception('Greska u parsiranju')

	def eat(self, type):
		if self.current_token.type == type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error()

	def factor(self):
		token = self.current_token

		if token.type == INTEGER:
			self.eat(INTEGER)
			return token.value
		elif token.type == LPAREN:
			self.eat(LPAREN)
			result = self.expr()
			self.eat(RPAREN)
			return result
		elif token.type == RIM:
			# Parse roman numeral
			return parse_rim(self, self.lexer)
		elif token.type == VARIABLE:
			# Parse variables
			self.eat(VARIABLE)
			if self.current_token.type == ASSIGN:
				self.eat(ASSIGN)
				result = self.expr()
				self.variables[token.value] = result
				return result
			else:
				return self.variables[token.value]

	def term(self):
		result = self.factor()

		while self.current_token.type in (MUL, DIV):
			token = self.current_token
			if token.type == MUL:
				self.eat(MUL)
				result = result * self.factor()
			elif token.type == DIV:
				self.eat(DIV)
				result = round(result / self.factor())
			else:
				self.error()

		return result

	def expr(self):
		result = self.term()

		while self.current_token.type in (PLUS, MINUS):
			token = self.current_token
			if token.type == PLUS:
				self.eat(PLUS)
				result = result + self.term()
			elif token.type == MINUS:
				self.eat(MINUS)
				result = result - self.term()
			else:
				self.error()

		return result

	def bool(self):
		result = True
		left = self.expr()

		if self.current_token.type in (LESS, GREATER, EQUAL, NOT_EQUAL, LESS_EQ, GREATER_EQ):
			right = None
			while self.current_token.type in (LESS, GREATER, EQUAL, NOT_EQUAL, LESS_EQ, GREATER_EQ):
				if self.current_token.type == LESS:
					self.eat(LESS)
					right = self.expr()
					if not (left < right):
						result = False
					left = right
				elif self.current_token.type == GREATER:
					self.eat(GREATER)
					right = self.expr()
					if not (left > right):
						result = False
					left = right
				elif self.current_token.type == EQUAL:
					self.eat(EQUAL)
					right = self.expr()
					if not (left == right):
						result = False
					left = right
				elif self.current_token.type == NOT_EQUAL:
					self.eat(NOT_EQUAL)
					right = self.expr()
					if not (left != right):
						result = False
					left = right
				elif self.current_token.type == LESS_EQ:
					self.eat(LESS_EQ)
					right = self.expr()
					if not (left <= right):
						result = False
					left = right
				elif self.current_token.type == GREATER_EQ:
					self.eat(GREATER_EQ)
					right = self.expr()
					if not (left >= right):
						result = False
					left = right

			return result, self.variables
		else:
			return left, self.variables

	def parse(self):
		return self.bool()

