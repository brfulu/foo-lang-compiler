from lexical_analysis.lexer import Lexer
from syntax_analysis.parser import Parser
from compiler.ast_visualizer import ASTVisualizer
from compiler.foo_compiler import Compiler

if __name__ == '__main__':
	test_case = 5
	with open('../../test-samples/zad{}.foo'.format(test_case), 'r') as inFile:
		text = inFile.read().replace('\n', ' ')

		lexer = Lexer(text)
		parser = Parser(lexer)

		# viz = ASTVisualizer(parser)
		# content = viz.genDot()
		# print(content)

		compiler = Compiler(parser)
		content = compiler.compile()
		# print(content)

		with open('../../test-samples/zad{}.py'.format(test_case), 'w') as outFile:
			outFile.write(content)

		exec(content)
		# exec(open('../../test-samples/zad{}.py'.format(test_case)).read())
