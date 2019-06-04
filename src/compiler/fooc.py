from lexical_analysis.lexer import Lexer
from syntax_analysis.parser import Parser
from compiler.ast_visualizer import ASTVisualizer

if __name__ == '__main__':
	with open('../../test-samples/zad10.foo', 'r') as file:
		text = file.read().replace('\n', ' ')

		lexer = Lexer(text)
		parser = Parser(lexer)
		viz = ASTVisualizer(parser)
		content = viz.genDot()

		print(content)
