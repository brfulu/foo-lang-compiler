class AST(object):
	pass


class Program(AST):
	def __init__(self, declarations):
		self.children = declarations


class Library(AST):
	def __init__(self, library):
		self.library = library


class FunDecl(AST):
	def __init__(self, type_node, fun_name, args_node, stmts_node):
		self.type_node = type_node
		self.fun_name = fun_name
		self.args_node = args_node
		self.stmts_node = stmts_node


class FunCall(AST):
	def __init__(self, name, args_node):
		self.name = name
		self.args_node = args_node


class IfStmt(AST):
	def __init__(self, cond_node, then_node, else_node):
		self.cond_node = cond_node
		self.then_node = then_node
		self.else_node = else_node


class Loop(AST):
	def __init__(self, init_node, cond_node, body_node):
		self.init_node = init_node
		self.cond_node = cond_node
		self.body_node = body_node

class Cond(AST):
	def __init__(self, expr):
		self.expr = expr

class Type(AST):
	def __init__(self, type):
		self.type = type


class Var(AST):
	def __init__(self, var):
		self.var = var

class VarInc(AST):
	def __init__(self, var):
		self.var = var

class VarDecl(AST):
	def __init__(self, type_node, var_node):
		self.type_node = type_node
		self.var_node = var_node


class Assign(AST):
	def __init__(self, var_node, expr):
		self.var_node = var_node
		self.expr = expr


class Args(AST):
	def __init__(self, args):
		self.args = args


class Stmts(AST):
	def __init__(self, type, stmts):
		self.type = type
		self.stmts = stmts


class BinOp(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right


class Num(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value


class String(AST):
	def __init__(self, value):
		self.value = value


class NodeVisitor(object):
	def visit(self, node):
		method_name = 'visit_{}'.format(type(node).__name__)
		visitor = getattr(self, method_name, self.error)
		return visitor(node)

	def error(self, node):
		raise Exception('Not found {}'.format(type(node).__name__))
