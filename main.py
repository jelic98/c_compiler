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
    arg_parser.add_argument('read_path')
    arg_parser.add_argument('write_path')
    args = arg_parser.parse_args()

    with open(args.read_path, 'r') as source:
        text = source.read()

        lexer = Lexer(text)
        tokens = lexer.lex()

        parser = Parser(tokens)
        ast = parser.parse()

        symbolizer = Symbolizer(ast)
        symbolizer.symbolize()

        optimizer = Optimizer(ast)
        optimizer.optimize()

        grapher = Grapher(ast)
        grapher.graph()

        generator = Generator(ast)
        generator.generate(args.write_path)

        runner = Runner(ast)
        runner.run()


if __name__ == '__main__':
    main()
