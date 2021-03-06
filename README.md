[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# C Compiler

Lightweight modular C compiler with code optimization build to support [this](https://github.com/jelic98/c_compiler/blob/master/grammar.txt) context free grammar. Extracted notebooks with detailed code explanation are available [here](https://github.com/jelic98/raf_pp_materials).

## Usage

1. Compile and run example C code
```bash
python3 main.py res/testX.c gen/testX.py
```
where X is chosen from [1-10]

2. Generated code and AST are stored in _out_ directory

## Future work

* Error handling
* Multidimensional arrays
* Unary increment/decrement operators
* Switch statement
* Additional stdlib functions
