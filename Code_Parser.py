import pycparser
from pycparser import c_ast

class CCodeParser:
    def extract_structs_from_code(self, code: str):
        parser = pycparser.CParser()
        parsed_code = parser.parse(code)
        structs = []
        
        class StructVisitor(c_ast.NodeVisitor):
            def visit_Struct(self, node):
                struct_info = {
                    "struct_name": node.name,
                    "fields": [decl.name for decl in node.decls] if node.decls else [],
                }
                structs.append(struct_info)
        
        struct_visitor = StructVisitor()
        struct_visitor.visit(parsed_code)
        
        output = []
        for struct_info in structs:
            fields = "\n".join(struct_info["fields"])
            struct_information = f"Struct {struct_info['struct_name']} \nFields:\n{fields}\n"
            output.append(struct_information)
        
        return output
    
    def extract_functions_from_code(self, code: str):
        parser = pycparser.CParser()
        parsed_code = parser.parse(code)
        functions = []
        
        class FuncDefVisitor(c_ast.NodeVisitor):
            def visit_FuncDef(self, node):
                func_name = node.decl.name
                start_line = node.decl.coord.line
                end_line = node.body.coord.line
                func_code = "\n".join(code.splitlines(True)[start_line - 1:end_line])
                functions.append(func_code)
        
        func_visitor = FuncDefVisitor()
        func_visitor.visit(parsed_code)
        
        return functions
    
    def extract_elements(self, source: str):
        structs = self.extract_structs_from_code(source)
        functions = self.extract_functions_from_code(source)
        
        return structs + functions


def remove_preprocessor_directives(code: str) -> str:
    # Remove lines starting with preprocessor directives
    processed_code = "\n".join(line for line in code.splitlines() if not line.strip().startswith("#"))
    return processed_code


if __name__ == "_main_":
    # Provide the code directly as a string or read from a file
    with open("sample.c","r") as f:
        source = f.read()
    print(source)
    # Remove preprocessor directives before parsing
    processed_source = remove_preprocessor_directives(source)
    print(processed_source)
    # Use the CCodeParser to extract elements from the processed code
    extracted_elements = CCodeParser().extract_elements(processed_source)
    
    for element in extracted_elements:
        print(element)