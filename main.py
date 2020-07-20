from src.token import Class, Token
from src.lexer import Lexer
from src.parser import Parser
from src.grapher import Grapher
from src.symbolizer import Symbolizer
from src.optimizer import Optimizer
from src.generator import Generator
from src.runner import Runner
import argparse


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('path')
    args = arg_parser.parse_args()
    path = args.path

    with open(path, 'r') as source:
        text = source.read()

        lexer = Lexer(text)
        tokens = lexer.lex()

        parser = Parser(tokens)
        ast = parser.parse()

        grapher = Grapher(ast)
        grapher.graph()

        symbolizer = Symbolizer(ast)
        symbolizer.symbolize()

        optimizer = Optimizer(ast)
        optimizer.optimize()

        generator = Generator(ast)
        generator.generate()

        runner = Runner(ast)
        runner.run()


if __name__ == '__main__':
    main()
