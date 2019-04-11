from lexer import Lexer
from infix import Infix
from prefix import Prefix
from postfix import Postfix

interpreters = {
	'infix': Infix,
	'prefix': Prefix,
	'postfix': Postfix,
}


def main():
	mode = 'postfix'
	selected_interpreter = interpreters[mode]
	variables = {}

	while True:
		try:
			text = input(f'{mode.upper()} -> ')
		except EOFError:
			break

		if not text:
			continue

		if text == 'exit':
			break

		if text.lower() in interpreters.keys():
			mode = text.lower()
			selected_interpreter = interpreters[mode]
			continue

		lexer = Lexer(text)
		interpreter = selected_interpreter(lexer, variables)
		result, variables = interpreter.parse()
		print(result)


if __name__ == "__main__":
	main()

