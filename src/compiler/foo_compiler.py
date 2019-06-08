from syntax_analysis.interpreter import NodeVisitor
from lexical_analysis.tokenType import *
from syntax_analysis.interpreter import *


def indent(code):
	result = '\t'
	i = 0
	for ch in code:
		result += ch
		if ch == '\n' and i < len(code) - 1:
			result += '\t'
		i += 1
	return result


class Compiler(NodeVisitor):
	def __init__(self, parser):
		self.parser = parser
		self.output = ''
		self.vars = {}
		self.libs = []

	def visit_Program(self, node):
		code = ''
		for child in node.children:
			stmt = self.visit(child)
			if len(stmt) == len(stmt.strip()):
				stmt += '\n'
			code += stmt
		return code

	def visit_Library(self, node):
		code = 'import {}\n'.format(node.library)
		self.libs.append(node.library)
		return code

	def visit_VarDecl(self, node):
		var = node.var_node.var
		default_value = None
		if node.type_node.type == 'int' or node.type_node.type == 'flt':
			default_value = '0'
		elif node.type_node.type == 'str':
			default_value = "''"
		else:
			default_value = '[]'
		code = '{} = {}\n'.format(var, default_value)
		self.vars[var] = {}
		self.vars[var]['type'] = node.type_node.type
		return code

	def visit_Assign(self, node):
		var = node.var_node.var
		value = self.visit(node.expr)
		if value == 'input()' and self.vars[var]['type'] == 'int':
			value = 'int(' + value + ')'
		if value == 'input()' and self.vars[var]['type'] == 'float':
			value = 'float(' + value + ')'
		if value.startswith('math.') and self.vars[var]['type'] == 'int':
			value = 'int(' + value + ')'

		code = '{} = {}\n'.format(node.var_node.var, value)
		return code

	def visit_FunDecl(self, node):
		args = self.visit(node.args_node)
		code = 'def {}({}):\n'.format(node.fun_name, args)
		stmts = self.visit(node.stmts_node)
		for stmt in stmts:
			code += indent(stmt)
			if len(stmt) == len(stmt.strip()):
				code += '\n'
		return code

	def visit_ReturnStmt(self, node):
		expr = self.visit(node.expr)
		code = 'return {}'.format(expr)
		return code

	def visit_Loop(self, node):
		code = ''
		init_stmts = self.visit(node.init_node)
		for stmt in init_stmts:
			code += stmt
		cond = self.visit(node.cond_node)
		code += 'while {}:\n'.format(cond)
		body_stmts = self.visit(node.body_node)
		for stmt in body_stmts:
			code += indent(stmt)
		return code

	def visit_IfStmt(self, node):
		cond = self.visit(node.cond_node).strip()
		code = 'if {}:\n'.format(cond)
		then_stmts = self.visit(node.then_node)
		for stmt in then_stmts:
			code += indent(stmt)

		if node.else_node:
			code += 'else:\n'
			else_stmts = self.visit(node.else_node)
			for stmt in else_stmts:
				code += indent(stmt)

		return code

	def visit_Args(self, node):
		code = ''
		counter = 0
		for child in node.args:
			if counter > 0:
				code += ', '
			code += self.visit(child).strip()
			counter += 1
		return code

	def visit_Stmts(self, node):
		stmts = []
		for child in node.stmts:
			stmt = self.visit(child)
			if len(stmt) == len(stmt.strip()):
				stmt += '\n'
			stmts.append(stmt)
		return stmts

	def visit_Type(self, node):
		s = 'node{} [label="Type: {}"]\n'.format(self.nodecount, node.type)
		node.num = self.nodecount
		self.nodecount += 1
		self.dot_body.append(s)

	def visit_Var(self, node):
		code = node.var
		return code

	def visit_VarInc(self, node):
		code = '{} += 1'.format(node.var.var)
		return code

	def visit_VarDec(self, node):
		code = '{} -= 1'.format(node.var.var)
		return code

	def visit_BinOp(self, node):
		op = node.op.value
		if node.op.value == '&':
			op = 'and'

		if node.op.value == '/':
			op = '//'
			if type(node.left) is Num and node.left.token.type == FLOAT:
				op = '/'
			if type(node.right) is Num and node.right.token.type == FLOAT:
				op = '/'
			if type(node.left) is Var and self.vars[node.left.var]['type'] == 'flt':
				op = '/'
			if type(node.right) is Var and self.vars[node.right.var]['type'] == 'flt':
				op = '/'

		left = self.visit(node.left)
		right = self.visit(node.right)
		code = '({} {} {})'.format(left, op, right)
		return code

	def visit_Num(self, node):
		code = '{}'.format(node.value)
		return code

	def visit_String(self, node):
		code = "'{}'".format(node.value)
		return code

	def visit_Boolean(self, node):
		value = node.value[0].upper() + node.value[1:]
		code = "{}".format(value)
		return code

	def visit_FunCall(self, node):
		splitted = node.name.split('.')
		if len(splitted) > 1:
			lib = splitted[0]
			if lib not in self.libs and lib in ['io', 'string', 'random']:
				raise Exception("Library '{}' not imported".format(lib))

		fun_name = node.name
		if node.name == 'io.in':
			fun_name = 'input'
		elif node.name == 'io.out':
			fun_name = 'print'
		elif node.name == 'io.fin':
			args = self.visit(node.args_node)
			code = "open({}, 'r').read()".format(args)
			return code
		elif node.name.endswith('len'):
			fun_name = 'len(' + fun_name.split('.')[0] + ')'
			return fun_name
		elif node.name.endswith('max'):
			fun_name = 'max'
		elif node.name.startswith('string.'):
			method = node.name.split('.')[1]
			args = self.visit(node.args_node)
			if method == 'toString':
				code = 'str({})'.format(args)
			else:
				code = '{}.{}()'.format(args, method)
			return code
		args = self.visit(node.args_node)
		code = '{}({})'.format(fun_name, args)
		return code

	def visit_Cond(self, node):
		expr = self.visit(node.expr)
		code = '{}'.format(expr)
		return code

	def visit_ListAccess(self, node):
		index = self.visit(node.index)
		code = '{}[{}]'.format(node.var.var, index)
		return code

	def compile(self):
		tree = self.parser.parse()
		code = self.visit(tree)
		return code
