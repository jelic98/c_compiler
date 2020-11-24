# ACINONYX - BEGIN
 
DEBUG = True # OBAVEZNO: Postaviti na False pre slanja projekta
 
if DEBUG:
   import os
   path_root = '/content/Datoteke/Druga faza/'
   path_grader = f'{path_root}grader.sh'
   os.system(f'chmod +x {path_grader}')
   test_id = '01' # Redni broj test primera [01-15]
   args = {}
   args['src'] = f'{path_root}{test_id}/src.pas' # Izvorna C datoteka
   args['gen'] = f'{path_root}{test_id}/gen.c' # Generisana PY datoteka
else:
   import argparse
   arg_parser = argparse.ArgumentParser()
   arg_parser.add_argument('src') # Izvorna C datoteka
   arg_parser.add_argument('gen') # Generisana PY datoteka
   args = vars(arg_parser.parse_args())
 
with open(args['src'], 'r') as source:
   text = source.read()
   lexer = Lexer(text)
   tokens = lexer.lex()
   parser = Parser(tokens)
   ast = parser.parse()
   symbolizer = Symbolizer(ast)
   symbolizer.symbolize()
   generator = Generator(ast)
   generator.generate(args['gen'])
   runner = Runner(ast)
   runner.run()
 
if DEBUG:
   os.system(f'bash {path_grader}')
 
# ACINONYX - END
