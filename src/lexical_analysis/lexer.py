from lexical_analysis.token import Token
from lexical_analysis.tokenType import *


class Lexer(object):
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

	def number(self):
		result = ''
		while self.current_char is not None and self.current_char.isdigit():
			result += self.current_char
			self.advance()

		if self.current_char == '.':
			result += '.'
			self.advance()
			while self.current_char is not None and self.current_char.isdigit():
				result += self.current_char
				self.advance()
			return Token(FLOAT, float(result))
		else:
			return Token(INTEGER, int(result))

	def id_type_keyword(self):
		result = ''
		while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
			result += self.current_char
			self.advance()

		if result in ['int', 'str', 'flt', 'bool', 'list']:
			return Token(TYPE, result)
		elif result == 'if':
			return Token(IF, result)
		elif result == 'loop':
			return Token(LOOP, result)
		elif result == 'func':
			return Token(FUNC, result)
		elif result == 'import':
			return Token(IMPORT, result)
		elif result == 'call':
			return Token(CALL, result)
		elif result == 'init':
			return Token(INIT, result)
		elif result == 'cond':
			return Token(COND, result)
		elif result == 'body':
			return Token(BODY, result)
		elif result == 'then':
			return Token(THEN, result)
		elif result == 'else':
			return Token(ELSE, result)
		else:
			return Token(ID, result)

	def string(self):
		result = ''
		while self.current_char is not None and self.current_char != "'":
			result += self.current_char
			self.advance()
		self.advance()
		return result

	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()

	def get_next_token(self):
		while self.current_char is not None:
			if self.current_char.isspace():
				self.skip_whitespace()

			if self.current_char is None:
				return Token(EOF, None)

			if self.current_char.isdigit():
				return self.number()

			if self.current_char.isalpha():
				return self.id_type_keyword()

			if self.current_char == ',':
				self.advance()
				return Token(COMMA, ',')

			if self.current_char == "'":
				self.advance()
				return Token(STRING, self.string())

			if self.current_char == ';':
				self.advance()
				return Token(SEMICOLON, ';')

			if self.current_char == '.':
				self.advance()
				return Token(DOT, '.')

			if self.current_char == '#':
				self.advance()
				return Token(HASH, '#')

			if self.current_char == '+':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(PLUS_ASSIGN, '+=')
				elif self.current_char == '+':
					self.advance()
					return Token(PLUS_PLUS, '++')
				return Token(PLUS, '+')

			if self.current_char == '-':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(MINUS_ASSIGN, '-=')
				elif self.current_char == '-':
					self.advance()
					return Token(MINUS_MINUS, '--')
				return Token(MINUS, '-')

			if self.current_char == '*':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(MUL_ASSIGN, '*=')
				return Token(MUL, '*')

			if self.current_char == '/':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(DIV_ASSIGN, '/=')
				return Token(DIV, '/')

			if self.current_char == '%':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(MOD_ASSIGN, '%=')
				return Token(MOD, '%')

			if self.current_char == '(':
				self.advance()
				return Token(LPAREN, '(')

			if self.current_char == ')':
				self.advance()
				return Token(RPAREN, ')')

			if self.current_char == '[':
				self.advance()
				return Token(LBRACKET, '[')

			if self.current_char == ']':
				self.advance()
				return Token(RBRACKET, ']')

			if self.current_char == '&':
				self.advance()
				return Token(AND, '&')

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
				return Token(ASSIGN, '=')

			if self.current_char == '!':
				self.advance()
				if self.current_char == '=':
					self.advance()
					return Token(NOT_EQUAL, '!=')
				self.error()

			self.error()

		return Token(EOF, None)
