from lexical_analysis.lexer import Lexer
from lexical_analysis.tokenType import EOF

if __name__ == '__main__':
	with open('../../test-samples/zad2.foo', 'r') as file:
		text = file.read().replace('\n', ' ')
		lexer = Lexer(text)

		token = lexer.get_next_token()
		while token.type != EOF:
			print(token)
			token = lexer.get_next_token()
