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
		library = self.current_token.value
		self.eat(STRING)
		self.eat(SEMICOLON)

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
		args_node = Args(self.parameter_list())
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
		stmts_node = Stmts(FUNC, self.statement_list())
		self.eat(RPAREN)

		return FunDecl(type_node=type_node, fun_name=fun_name, args_node=args_node, stmts_node=stmts_node)

	def argument_list(self):
		args = []

		while self.current_token.type != RPAREN:
			args.append(self.expr())

			if self.current_token.type == COMMA:
				self.eat(COMMA)

		return args

	def parameter_list(self):
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

		while self.current_token.type != EOF and self.current_token.type != RPAREN:
			# print(self.current_token)
			if self.current_token.type == TYPE:
				statements.extend(self.var_declaration())
			elif self.current_token.type == IF:
				statements.append(self.if_statement())
			elif self.current_token.type == LOOP:
				statements.append(self.loop())
			elif self.check_assignment():
				statements.append(self.assignment_stmt())
			elif self.check_aug_assignment():
				statements.append(self.aug_assignment_stmt())
			else:
				statements.append(self.expr())
				print(self.current_token)
				self.eat(SEMICOLON)

		return statements

	@restorable
	def check_assignment(self):
		if self.current_token.type != ID:
			return False
		self.eat(ID)
		return self.current_token.type == ASSIGN

	def assignment_stmt(self):
		var_node = Var(self.current_token.value)
		self.eat(ID)
		self.eat(ASSIGN)
		expr = self.expr()
		self.eat(SEMICOLON)
		return Assign(var_node, expr)

	@restorable
	def check_aug_assignment(self):
		if self.current_token.type != ID:
			return False
		self.eat(ID)
		return self.current_token.type in [PLUS_ASSIGN, MINUS_ASSIGN, MUL_ASSIGN, DIV_ASSIGN, MOD_ASSIGN]

	def aug_assignment_stmt(self):
		var_node = Var(self.current_token.value)
		self.eat(ID)
		op = self.current_token
		op.value = op.value[0]
		if self.current_token.type == PLUS_ASSIGN:
			op.type = PLUS
		elif self.current_token.type == MINUS_ASSIGN:
			op.type = MINUS
		elif self.current_token.type == MUL_ASSIGN:
			op.type = MUL
		elif self.current_token.type == MOD_ASSIGN:
			op.type = MOD
		self.eat(self.current_token.type)

		expr = BinOp(left=var_node, op=op, right=self.expr())
		self.eat(SEMICOLON)
		return Assign(var_node, expr)

	def if_statement(self):
		self.eat(IF)
		self.eat(DOT)
		self.eat(COND)
		self.eat(LPAREN)
		cond_node = Cond(self.expr())
		self.eat(RPAREN)
		self.eat(DOT)
		self.eat(THEN)
		self.eat(LPAREN)
		then_node = Stmts(THEN, self.statement_list())
		self.eat(RPAREN)

		else_node = None
		if self.current_token.type == DOT:
			self.eat(DOT)
			self.eat(ELSE)
			self.eat(LPAREN)
			else_node = Stmts(ELSE, self.statement_list())
			self.eat(RPAREN)
			self.eat(SEMICOLON)
		else:
			self.eat(SEMICOLON)

		return IfStmt(cond_node, then_node, else_node)

	def loop(self):
		print('evo me')
		self.eat(LOOP)
		self.eat(DOT)
		self.eat(INIT)
		self.eat(LPAREN)
		init_node = Stmts(INIT, self.statement_list())
		self.eat(RPAREN)
		self.eat(DOT)
		self.eat(COND)
		self.eat(LPAREN)
		cond_node = Cond(self.expr())
		print(cond_node)
		self.eat(RPAREN)
		self.eat(DOT)
		print(self.current_token)
		self.eat(BODY)
		self.eat(LPAREN)
		body_node = Stmts(BODY, self.statement_list())
		self.eat(RPAREN)
		self.eat(SEMICOLON)
		print('zavrsio')
		return Loop(init_node, cond_node, body_node)

	def var_declaration(self):
		type_node = Type(self.current_token.value)
		self.eat(TYPE)
		var_node = Var(self.current_token.value)
		self.eat(ID)

		declarations = [VarDecl(type_node, var_node)]

		if self.current_token.type == ASSIGN:
			self.eat(ASSIGN)
			declarations.append(Assign(var_node, self.expr()))

		self.eat(SEMICOLON)
		return declarations

	def factor(self):
		token = self.current_token

		if token.type == INTEGER:
			self.eat(INTEGER)
			return Num(token)
		elif token.type == FLOAT:
			self.eat(FLOAT)
			return Num(token)
		elif token.type == PLUS_PLUS:
			self.eat(PLUS_PLUS)
			var = Var(self.current_token.value)
			self.eat(ID)
			return VarInc(var)
		elif token.type == STRING:
			self.eat(STRING)
			return String(token.value)
		elif token.type == ID:
			name = self.current_token.value
			self.eat(ID)
			if self.current_token.type == DOT:
				name += self.current_token.value
				self.eat(DOT)
				name += self.current_token.value
				self.eat(ID)
				self.eat(DOT)
				self.eat(CALL)
				self.eat(LPAREN)
				args_node = Args(self.argument_list())
				self.eat(RPAREN)
				return FunCall(name, args_node)
			else:
				return Var(name)
		elif token.type == LPAREN:
			self.eat(LPAREN)
			node = self.expr()
			self.eat(RPAREN)
			return node

	def term(self):
		node = self.factor()

		while self.current_token.type in (MUL, DIV, MOD):
			token = self.current_token
			if token.type == MUL:
				self.eat(MUL)
			elif token.type == DIV:
				self.eat(DIV)
			elif token.type == MOD:
				self.eat(MOD)
			else:
				self.error()

			node = BinOp(left=node, op=token, right=self.factor())

		return node

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

			return result
		else:
			return left

	def expr(self):
		node = self.term()

		if self.current_token.type in [LESS, GREATER, EQUAL, NOT_EQUAL, LESS_EQ, GREATER_EQ]:
			token = self.current_token
			self.eat(token.type)
			return BinOp(left=node, op=token, right=self.expr())

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
