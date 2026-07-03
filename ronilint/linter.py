import ast
import re
from typing import Any

CAMEL_CASE = re.compile(r"^[a-z]+(?:[A-Z][a-z0-9]*)*$")

def classifyName(name:str):
    if name.startswith("__") and name.endswith("__"):
        return "dunder"
    elif name.startswith("__"):
        return "mangled"
    elif name.startswith("_"):
        return "private definition"
    elif name.isupper():
        return "constant"
    
    return "normal"

class RoniLint(ast.NodeVisitor):
    def visit_FunctionDef(self, node) -> Any:
        if not CAMEL_CASE.match(node.name) and not classifyName(node.name) == 'dunder':
            print(
                f"Linha {node.lineno}: "
                f"Função '{node.name}' deveria usar camelCase."
            )
        
        elif classifyName(node.name) == "dunder":
            return
        
        elif classifyName(node.name) == "mangled":
            print(
                f"Linha {node.lineno}: "
                f"Função '{node.name} sofrerá name mangling. Considere tirar uma underscore."
            )

        elif classifyName(node.name) == "private definition":
            return
        
        elif classifyName(node.name) == "normal":
            return

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            varName = node.id
            if not CAMEL_CASE.match(varName) and not classifyName(node.id) == 'dunder':
                print(
                    f"Linha {node.lineno}: "
                    f"Variável '{varName}' deveria usar camelCase."
                )
            
            elif classifyName(varName) == "dunder":
                return
            
            elif classifyName(varName) == "mangled":
                print(
                    f"Linha {node.lineno}: "
                    f"Variável {varName} sofrerá name mangling. Considere tirar uma underscore."
                )

            elif classifyName(varName) == "private definition":
                return
            
            elif classifyName(varName) == "constant":
                return
            
            elif classifyName(varName) == "normal":
                return