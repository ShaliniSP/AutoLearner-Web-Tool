import pycparser
from pycparser import c_ast, c_generator
import copy


class deleteV(c_ast.NodeVisitor):
	def visit_FuncDef(self, node):
		node.body = c_ast.Compound([])



def remove_fnbody(ast, new_pgm_name):
	ast_copy = copy.deepcopy(ast)

	deleteV().visit(ast_copy)

	generator = c_generator.CGenerator()

	new_code = generator.visit(ast_copy)

	with open(new_pgm_name, 'w') as f:
		f.write(new_code)




if __name__== "__main__":
	if len(sys.argv) < 2:
		print "enter filenames and/or function name"
		sys.exit(1) 
	ast1 = pycparser.parse_file(sys.argv[1])
	remove_fnbody(ast1, "../../new_code.c")


