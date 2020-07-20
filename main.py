import os
import argparse
from graphviz import Source
from src.token import Class, Token
from src.lexer import Lexer
from src.parser import Parser
from src.grapher import Grapher
from src.runner import Runner

RUN = False


def handle_input(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    grapher = Grapher(parser)
    runner = Runner(parser)

    if RUN:
        return runner.run()
    else:
        return grapher.graph()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('path')

    args = arg_parser.parse_args()
    path = args.path

    with open(path, 'r') as input:
        result = handle_input(input.read())

    if not RUN:
        dirs = os.path.splitext(path)[0].split(os.sep)
        dirs.insert(-2, 'out')
        graph = os.sep.join(dirs)

        s = Source(result, filename=graph, format='png')
        s.view()


if __name__ == '__main__':
    main()
