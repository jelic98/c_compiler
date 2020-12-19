# ACINONYX - BEGIN
 
DEBUG = True # OBAVEZNO: Postaviti na False pre slanja projekta
 
if DEBUG:
   test_id = '01' # Redni broj test primera [01-16]
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
 
# 1. Preuzeti direktorijum Datoteke sa materijala
# 2. Postaviti arhivu u content direktorijum u okviru sesije
# 3. Napraviti i pokrenuti ćeliju sa komandom !unzip 'arhiva.zip'
# 4. Postaviti DEBUG promenljivu na False
# 5. Preuzeti notebook kao .py datoteku i imenovati je main.py
# 6. Postaviti main.py na putanju na koju pokazuje path_root
# 7. Postaviti DEBUG promenljivu na True
# 8. Pokrenuti grader.sh pokretanjem ove ćelije
 
if DEBUG:
   path_grader = f'{path_root}grader.sh'
   !chmod +x '{path_grader}' # Dozvola za izvršavanje
   !bash '{path_grader}' '{path_root}' # Pokretanje gradera
 
# GRADER - END
