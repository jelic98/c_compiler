# ACINONYX - BEGIN
 
DEBUG = True # OBAVEZNO: Postaviti na False pre slanja projekta
 
if DEBUG:
   test_id = '01' # Redni broj test primera [01-15]
   path_root = '/content/Datoteke/Druga faza/'
   args = {}
   args['src'] = f'{path_root}{test_id}/src.pas' # Izvorna PAS datoteka
   args['gen'] = f'{path_root}{test_id}/gen.c' # Generisana C datoteka
else:
   import argparse
   arg_parser = argparse.ArgumentParser()
   arg_parser.add_argument('src') # Izvorna PAS datoteka
   arg_parser.add_argument('gen') # Generisana C datoteka
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
 
# ACINONYX - END

# GRADER - BEGIN
 
# 1. Preuzeti notebook kao .py datoteku i imenovati je main.py
# 2. Postaviti main.py na putanju na koju pokazuje path_root
 
if DEBUG:
   path_grader = f'{path_root}grader.sh'
   !chmod +x '{path_grader}' # Dozvola za izvršavanje
   !bash '{path_grader}' '{path_root}' # Pokretanje gradera
 
# GRADER - END
