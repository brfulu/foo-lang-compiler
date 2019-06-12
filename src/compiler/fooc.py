from lexical_analysis.lexer import Lexer
from syntax_analysis.parser import Parser
from compiler.ast_visualizer import ASTVisualizer
from compiler.foo_compiler import Compiler
import sys

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('Please pass source file name!')
		exit()

	src_file = sys.argv[1]
	# test_case = 2
	with open('./test-samples/{}'.format(src_file), 'r') as inFile:
		text = inFile.read().replace('\n', ' ')

		lexer = Lexer(text)
		parser = Parser(lexer)

		# viz = ASTVisualizer(parser)
		# content = viz.genDot()
		# print(content)

		compiler = Compiler(parser)
		content = compiler.compile()
		# print(content)

		with open('./test-samples/{}.py'.format(src_file.split('.')[0]), 'w') as outFile:
			outFile.write(content)

		exec(content)
		# exec(open('./test-samples/zad{}.py'.format(test_case)).read())
