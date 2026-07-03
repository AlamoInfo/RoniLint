from ronilint import linter
import ast, sys

def lintFile(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    
    tree = ast.parse(source, filename)
    visitor = linter.RoniLint()
    visitor.visit(tree)

def main():
    for filename in sys.argv[1:]:
        lintFile(filename)

