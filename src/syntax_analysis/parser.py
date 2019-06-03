from lexical_analysis.tokenType import *
from syntax_analysis.interpreter import *
from syntax_analysis.util import restorable


class Parser(object):
	def __init__(self, lexer):
		self.lexer = lexer
		self.current_token = self.lexer.get_next_token()

	def error(self):
		raise Exception('Greska u parsiranju')

	def eat(self, type):
		if self.current_token.type == type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error()

	def program(self):
		children = []

		while self.current_token.type != EOF:
			if self.current_token.type == IMPORT:
				children.append(self.library_import())
			elif self.current_token.type == FUNC:
				children.append(self.function_declaration())
			else:
				children.extend(self.statement_list())

		return Program(children)

	# @restorable
	# def check_function(self):
	# 	self.eat(TYPE)
	# 	self.eat(ID)
	# 	return self.current_token.type == LPAREN

	def library_import(self):
		self.eat(IMPORT)
		self.eat(APOSTROPHE)
		library = self.current_token.value
		self.eat(ID)
		self.eat(APOSTROPHE)

		return Library(library)

	def function_declaration(self):
		self.eat(FUNC)

		self.eat(DOT)
		self.eat(NAME)
		self.eat(LPAREN)
		fun_name = self.current_token.value
		self.eat(ID)
		self.eat(RPAREN)

		self.eat(DOT)
		self.eat(PARAMS)
		self.eat(LPAREN)
		args_node = Args(self.argument_list())
		self.eat(RPAREN)

		self.eat(DOT)
		self.eat(RETURNS)
		self.eat(LPAREN)
		type_node = Type(self.current_token.value)
		self.eat(TYPE)
		self.eat(RPAREN)

		self.eat(DOT)
		self.eat(BODY)
		self.eat(LPAREN)
		stmts_node = Stmts(self.statement_list())
		self.eat(RPAREN)

		return FunDecl(type_node=type_node, fun_name=fun_name, args_node=args_node, stmts_node=stmts_node)

	def argument_list(self):
		params = []

		while self.current_token.type != RPAREN:
			type_node = Type(self.current_token.value)
			self.eat(TYPE)

			var_node = Var(self.current_token.value)
			self.eat(ID)

			params.append(VarDecl(type_node, var_node))

			if self.current_token.type == COMMA:
				self.eat(COMMA)

		return params

	def statement_list(self):
		statements = []

		while self.current_token.type != EOF:
			# VAR_DECL
			if self.current_token.type == TYPE:
				statements.append(self.var_declaration())
			elif self.current_token.type == IF:
				statements.append(self.if_statement())
			elif self.current_token.type == LOOP:
				statements.append(self.loop())
			elif self.check_assignment():
				pass
			elif self.check_aug_assignment():
				pass
			else:
				self.error()

			# if self.current_token.type == IMPORT:
			# 	children.append(self.library_import())
			# elif self.current_token.type == FUNC:
			# 	children.append(self.function_declaration())
			# else:
			# 	children.extend(self.statement_list())

		return statements

	def var_declaration(self, type_node, var_node):
		declarations = []

		declarations.append(VarDecl(type_node, var_node))

		if self.current_token.type == ASSIGN:
			self.eat(ASSIGN)
			declarations.append(Assign(var_node, self.expr()))

		return declarations

	def factor(self):
		token = self.current_token

		if token.type == INTEGER:
			self.eat(INTEGER)
			return Num(token)
		elif token.type == LPAREN:
			self.eat(LPAREN)
			node = self.expr()
			self.eat(RPAREN)
			return node

	def term(self):
		node = self.factor()

		while self.current_token.type in (MUL, DIV):
			token = self.current_token
			if token.type == MUL:
				self.eat(MUL)
			elif token.type == DIV:
				self.eat(DIV)
			else:
				self.error()

			node = BinOp(left=node, op=token, right=self.factor())

		return node

	def expr(self):

		node = self.term()

		while self.current_token.type in (PLUS, MINUS):
			token = self.current_token
			if token.type == PLUS:
				self.eat(PLUS)
			elif token.type == MINUS:
				self.eat(MINUS)
			else:
				self.error()

			node = BinOp(left=node, op=token, right=self.term())

		return node

	def parse(self):
		return self.program()
