from src.token import Class, Token
from src.lexer import Lexer
from src.parser import Parser
from src.grapher import Grapher
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
        parser = Parser(lexer)
        grapher = Grapher(parser)
        runner = Runner(parser)
        grapher.graph()


if __name__ == '__main__':
    main()
