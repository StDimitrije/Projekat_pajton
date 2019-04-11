from token import Token
from constants import (
	INTEGER, VARIABLE, RIM, EOF,
	PLUS, MINUS, MUL, DIV,
	RPAREN, LPAREN, ASSIGN,
	LESS, GREATER, EQUAL, NOT_EQUAL, LESS_EQ, GREATER_EQ,
)


class Lexer():
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.current_char = self.text[self.pos]

	def error(self):
		raise Exception('Neocekivani karakter {} '.format(self.current_char))

	def advance(self):
		self.pos += 1

		if self.pos > len(self.text) - 1:
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]

	def integer(self):
		number = ""
		while(self.current_char is not None and self.current_char.isdigit()):
			number += self.current_char
			self.advance()
		return int(number)

	def skip_whitespace(self):
		while(self.current_char is not None and self.current_char.isspace()):
			self.advance()

	def get_next_token(self):
		while self.current_char is not None:
			if self.current_char.isspace():
				self.skip_whitespace()
				continue

			if self.current_char.isdigit():
				return Token(INTEGER, self.integer())

			if self.current_char == '+':
				self.advance()
				return Token(PLUS, '+')

			if self.current_char == '-':
				self.advance()
				return Token(MINUS, '-')

			if self.current_char == '*':
				self.advance()
				return Token(MUL, '*')

			if self.current_char == '/':
				self.advance()
				return Token(DIV, '/')

			if self.current_char == '(':
				self.advance()
				return Token(LPAREN, '(')

			if self.current_char == ')':
				self.advance()
				return Token(RPAREN, ')')

			if self.current_char == '<':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(LESS_EQ, '<=')
				return Token(LESS, '<')

			if self.current_char == '>':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(GREATER_EQ, '>=')
				return Token(GREATER, '>')

			if self.current_char == '=':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(EQUAL, '==')
				else:
					return Token(ASSIGN, '=')
				self.error()

			if self.current_char == '!':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(NOT_EQUAL, '!=')
				self.error()

			var = ''
			if self.current_char and self.current_char.isalpha():
				while self.current_char and (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_'):
					var += self.current_char
					self.advance()

			if var:
				if var == 'RIM' and self.current_char == '(':
					return Token(RIM, 'RIM')

				return Token(VARIABLE, var)

			self.error()

		return Token(EOF, None)

