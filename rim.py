from constants import (
	RIM, LPAREN, RPAREN, VARIABLE
)


def parse_rim(interpreter, lexer):
	interpreter.eat(RIM)
	interpreter.eat(LPAREN)
	token = interpreter.current_token
	result = convert(token.value)
	interpreter.eat(VARIABLE)
	interpreter.eat(RPAREN)
	return result


def convert(x):
	y = thousand(x)
	result = y[0]
	z = hundred(y[1])
	result += z[0]
	t = ten(z[1])
	result += t[0]
	u = one(t[1])
	result += u[0]
	return result


def thousand(x):
	if x.startswith('MMM'):
		return (3000, x[3:])
	elif x.startswith('MM'):
		return (2000, x[2:])
	elif x.startswith('M'):
		return (1000, x[1:])
	return (0, x)


def hundred(x):
	if x.startswith('CM'):
		return (900, x[2:])
	elif x.startswith('CD'):
		return (400, x[2:])
	elif x.startswith('D'):
		hundreds, remainder = s_hundred(x[1:])
		return (500 + hundreds, remainder)
	return s_hundred(x)


def s_hundred(x):
	if x.startswith('CCC'):
		return (300, x[3:])
	elif x.startswith('CC'):
		return (200, x[2:])
	elif x.startswith('C'):
		return (100, x[1:])
	return (0, x)


def ten(x):
	if x.startswith('XC'):
		return (90, x[2:])
	elif x.startswith('XL'):
		return (40, x[2:])
	elif x.startswith('L'):
		tens, remainder = s_ten(x[1:])
		return (50 + tens, remainder)
	return s_ten(x)


def s_ten(x):
	if x.startswith('XXX'):
		return (30, x[3:])
	elif x.startswith('XX'):
		return (20, x[2:])
	elif x.startswith('X'):
		return (10, x[1:])
	return (0, x)


def one(x):
	if x.startswith('X'):
		return (9, x[1:])
	elif x.startswith('IV'):
		return (4, x[2:])
	elif x.startswith('V'):
		ones, remainder = s_one(x[1:])
		return (5 + ones, remainder)
	return s_one(x)


def s_one(x):
	if x.startswith('III'):
		return (3, x[3:])
	elif x.startswith('II'):
		return (2, x[2:])
	elif x.startswith('I'):
		return (1, x[1:])
	return (0, x)


