from vyper_parser import cst

code = """def f():
    pass"""

ast = cst.parse_python(code)

print(ast)
