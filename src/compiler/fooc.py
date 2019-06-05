from lexical_analysis.lexer import Lexer
from syntax_analysis.parser import Parser
from compiler.ast_visualizer import ASTVisualizer
from compiler.foo_compiler import Compiler

if __name__ == '__main__':
	test_case = 10
	with open('../../test-samples/dummy.foo', 'r') as inFile:
		text = inFile.read().replace('\n', ' ')

		lexer = Lexer(text)
		parser = Parser(lexer)

		# viz = ASTVisualizer(parser)
		# content = viz.genDot()
		# print(content)

		compiler = Compiler(parser)
		content = compiler.compile()
		print(content)

		with open('../../test-samples/dummy.py'.format(test_case), 'w') as outFile:
			outFile.write(content)

