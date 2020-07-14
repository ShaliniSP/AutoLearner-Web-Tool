import pycparser
from pycparser import c_ast, c_generator
import sys
import pdb
import re
from zss import Node, simple_distance, Operation



class deleteLoopVisitor(c_ast.NodeVisitor):
	def __init__(self, loop):
		self.loop = loop

	def generic_visit(self, node):
		if node == None:
			return 
		if self.loop in [i for i in node]:
			if type(node) == c_ast.Compound:
				node.block_items.remove(self.loop)
			elif type(node) == c_ast.If:
				if self.loop == node.iftrue:
					node.iftrue = None
				else:
					node.iffalse = None

			else:
				print "BAD? trying to delete ", type(node)
				# pdb.set_trace()

		for c in node:
			self.visit(c)

class getLoopStructure(c_ast.NodeVisitor):

	def __init__(self, fname, ls_type = ''):
		self.loopStruct = []
		self.fname = fname
		self.loop_count = 0
		self.if_count = 0
		self.cost = 0
		self.temp_nodes = {}
		self.ls_type = ls_type
		self.matching = {}
		self.insert_nodes = {}
		self.all_ast_nodes = {}

	# def generic_visit(self, node):
	# 	flag = False
	# 	for c in node:
	# 		if self.visit(c) == True:
	# 			flag = True

	# 	return flag

	# def visit():
	def generic_visit(self, node):

		ls = []

		for c in node:
			rets = self.visit(c)
			if rets:
				# if ls == []:
				# 	ls = rets
				# else:
				# 	# ls.append(rets)
				# 	ls = [ls, rets]
				ls.append(rets)
		if ls == []:
			return
		if len(ls)==1:
			return ls[0]
		return ls

	def visit_If(self, node):


		self.if_count+=1
		ic = self.if_count

		tree_node = Node("IF"+str(ic)+self.ls_type)
		tree_node.ast_node = node
		self.all_ast_nodes["IF"+str(ic)+self.ls_type] = node

		if_node = Node("i"+str(ic)+self.ls_type)
		tree_node.addkid(if_node)
		if_node.ast_node = node.iftrue
		self.all_ast_nodes["i"+str(ic)+self.ls_type] = node.iftrue

		if_block = self.visit(node.iftrue)
		if type(if_block)==Node:
			if_node.addkid(if_block)
		elif type(if_block)==list:
			for i in if_block:
				if_node.addkid(i)

		if node.iffalse:
			else_block = self.visit(node.iffalse)
			else_node = Node("e"+str(ic)+self.ls_type)
			tree_node.addkid(else_node)
			else_node.ast_node = node.iffalse
			self.all_ast_nodes["e"+str(ic)+self.ls_type] = node.iffalse

			if type(else_block) == Node:
				else_node.addkid(else_block)
			elif type(else_block) == list:
				for i in else_block:
					else_node.addkid(i)

		return tree_node



	def loop_visit(self, node, loop_type = 'For'):
		# print "found loops"
		self.loop_count+=1
		lc = self.loop_count
		

		inner = self.generic_visit(node)
		tree_node = Node(loop_type+str(lc)+self.ls_type)
		tree_node.ast_node = node
		self.all_ast_nodes[loop_type+str(lc)+self.ls_type] = node

		if type(inner) == Node:
			tree_node.addkid(inner)
		elif type(inner) == list:
			for i in inner:
				tree_node.addkid(i)

		return tree_node
	
	def visit_For(self, node):
		return self.loop_visit(node, 'For')

	def visit_While(self, node):
		return self.loop_visit(node, 'While')

	def visit_DoWhile(self, node):
		return self.loop_visit(node, 'DoWhile')

	def visit_FuncDef(self, node):
		if node.decl.name == self.fname:
			# print fname, "found"


			# self.loopStruct = self.visit(node.body)
			# if type(self.loopStruct)==dict:
			# 	self.loopStruct = [self.loopStruct]


			fn_node = Node(self.fname)
			body_nodes = self.visit(node.body)
			if type(body_nodes) == Node:
				fn_node.addkid(body_nodes)
			elif type(body_nodes) ==list:
				for i in body_nodes:
					fn_node.addkid(i)

			fn_node.ast_node = node
			self.all_ast_nodes[self.fname] = node
			self.loopStruct = fn_node

		else:
			return 





	def getStructDiff(self, ls1, inside = None):
		cost, operations = simple_distance(self.loopStruct, ls1, return_operations = True, get_label = get_type)
		print "Cost of struct repairs =", cost
		self.sm_cost = cost


		# pdb.set_trace()

		for op in operations:
			if op.type == Operation.insert:
				# pdb.set_trace()
				# print "Inserting", op.arg2.label
				self.insert_nodes[op.arg2.label] = self.get_struct_nodes(op.arg2)

			elif op.type == Operation.update:
				# print "Updating", op.arg1.label, "to", op.arg2.label
				if op.arg1.label in self.matching.keys():
					self.matching[op.arg2.label] = self.matching[op.arg1.label]
					del self.matching[op.arg1.label] 
				self.update_ast(op.arg1, op.arg2)
				# op.arg1.label = op.arg2.label

				self.match_trees(op.arg1, op.arg2)




			elif op.type == Operation.remove:
				# print "Removing", op.arg1.label
				inside, after = self.get_position(self.loopStruct, op.arg1)
				hanging = self.remove_tree(self.loopStruct, op.arg1)
				self.repair_to_delete(op.arg1, inside, after)

				if hanging:
					for i in hanging:
						self.insert_nodes[i.label] = i

			elif op.type == Operation.match:
				# pdb.set_trace()

				# print "Matching",op.arg2.label, op.arg1.label
				self.matching[op.arg1.label] = op.arg2.label
				self.match_trees(op.arg1, op.arg2)


	def update_ast(self, node1, node2):
		# pdb.set_trace()
		if get_type(node1)==get_type(node2):
			return
			# node_type2 = c_ast.For if get_type(node2)=='For' else c_ast.While if get_type(node2)=='While' else c_ast.DoWhile
		orig_node = node1.ast_node
		
		if get_type(node1) in ['For', 'While', 'DoWhile']:
			if get_type(node2) == 'For':
				node1.ast_node = c_ast.For(None, orig_node.cond, None, orig_node.stmt)
			elif get_type(node2) in ['While', 'DoWhile']:
				node_type2 = c_ast.While if get_type(node2)=='While' else c_ast.DoWhile
				node1.ast_node = node_type2(orig_node.cond, orig_node.stmt)
			elif get_type(node2) == 'IF':
				node1.ast_node = c_ast.If(orig_node.cond, orig_node.stmt, None)
			elif get_type(node2) in ['i', 'e']:
				node1.ast_node = orig_node.stmt

		elif get_type(node1)=='IF':
			if get_type(node2) == 'For':
				node1.ast_node = c_ast.For(None, orig_node.cond, None, orig_node.iftrue)
			elif get_type(node2) in ['While', 'DoWhile']:
				node_type2 = c_ast.While if get_type(node2)=='While' else c_ast.DoWhile
				node1.ast_node = node_type2(orig_node.cond, orig_node.iftrue)
			elif get_type(node2) == 'i':
				node1.ast_node = orig_node.iftrue
			elif get_type(node2) == 'e':
				node1.ast_node = orig_node.iffalse


		elif get_type(node1)in ['i', 'e']:
			if get_type(node2) == 'For':
				node1.ast_node = c_ast.For(None, None, None, orig_node)
			elif get_type(node2) in ['While', 'DoWhile']:
				node_type2 = c_ast.While if get_type(node2)=='While' else c_ast.DoWhile
				node1.ast_node = node_type2(None, orig_node)

			# orig_node = node1.parent()
			elif get_type(node2) == 'IF':
				if get_type(node1) =='i':
					node1.ast_node = c_ast.If(None, orig_node, None)
				else:
					node1.ast_node = c_ast.If(None, None, orig_node)
		
	

		self.update_tree(self.loopStruct, node1, node1.ast_node, orig_node)
		node1.label = node2.label
		self.all_ast_nodes[node1.label] = node1.ast_node


	def get_position(self, root, t_node, inside = None, after = None):
		if t_node == root:
			return inside, after

		if t_node in root.children:
			index = root.children.index(t_node)
			if index!=0:
				return root, root.children[index-1]
			else:
				return root, None  
		else:

			for c in root.children:
				ret= self.get_position(c, t_node)
				if ret:
					return ret[0], ret[1]


	def update_tree(self,root, orig_node, new_node, orig_ast):
		# pdb.set_trace()
		# if orig_node.label[0] in ['i', 'e']:
		# 	orig_node = Node('IF'+orig_node.label[1:])
		# 	return self.update_tree(root, orig_node, new_node, orig_ast)
		if orig_node in root.children:
			# root.children.remove(t_node)
			node = root.ast_node
			if type(node) in [c_ast.For, c_ast.While, c_ast.DoWhile]:
				n = node.stmt
				if type(n)!=c_ast.Compound:
					n = c_ast.Compound([n])
					node.stmt = n
				node = n
			elif type(node) == c_ast.FuncDef:
				node = node.body
			if type(node) == c_ast.Compound:
				node.block_items = [i if i!=orig_ast else new_node for i in node.block_items]
			elif type(node) == c_ast.If:
				if orig_ast == node.iftrue:
					node.iftrue = new_node
				else:
					node.iffalse = new_node

			return True
		else:
			for c in root.children:
				r = self.update_tree(c, orig_node, new_node, orig_ast)
				if r==True:
					return True
	def remove_tree(self,root, t_node):
		# pdb.set_trace()
		# try:
		# 	if t_node in [n for n in root.children if n not in root.newnodes]:
		# 		root.children.remove(t_node)
		# 		return t_node.children
		# except:
		if t_node in root.children:
			root.children.remove(t_node)
			return t_node.children
		else:
			for c in root.children:
				r = self.remove_tree(c, t_node)
				if r:
					return r

	def match_trees(self, root1, root2):
		# pdb.set_trace()
		# self.matching[root1.label] = root2.label

		after = None
		for (c1,c2) in zip(root1.children,root2.children):
			if c1.label in self.matching.keys():
				if self.matching[c1.label] != c2.label:
					if c2.label in self.insert_nodes.keys():
						# root1.children.remove(c1)
						# self.temp_nodes[c1.label] = c1
						# root1.addkid()
						self.repair_to_add(c2,  root1, after)
						# pdb.set_trace()
						self.add_loop_structure(self.insert_nodes[c2.label], root1, after, inplace = c1)
						root1.children = [i if i!=c1 else c2 for i in root1.children]
					# else:
					# 	pdb.set_trace()
					# del self.matching[c1.label]

			# root1.addkid(c2)
			# self.match_trees(c1,c2)
			after = c1
				# self.matching[c1.label] == c2.label
		if len(root2.children) > len(root1.children):
			remaining = root2.children[len(root1.children):]
			
			if len(root1.children) >0:
				prev = root2.children[len(root1.children)-1]
			else:
				prev = None

			for c in remaining:
				root1.addkid(c)
				# pdb.set_trace()

				self.repair_to_add(c, root1, prev)
				# pdb.set_trace()
				if c.label in self.insert_nodes.keys():
					try:
						self.add_loop_structure(self.insert_nodes[c.label].ast_node, root1, prev)
					except:
						self.add_loop_structure(self.insert_nodes[c.label], root1, prev)

				else:
					self.insert_nodes[c.label] = self.get_struct_nodes(c)
					self.add_loop_structure(self.insert_nodes[c.label], root1, prev)
				prev = c


	def repair_to_add(self, t_node, inside = None, after = None):

		if inside:
			inside_text = inside.label
			m = re.search(r"\d", inside_text)
			if m:
				inside_text = inside_text[:m.start()] + " #"+ inside_text[m.start()]
		else:
			inside_text = 'None'

		if after:
			after_text = after.label

			m = re.search(r"\d", after_text)
			if m:
				after_text = after_text[:m.start()] + " #"+ after_text[m.start()]
		else:
			after_text = 'None'

		print "* Add", desc_struct(t_node), "\tInside -", inside_text, ";After -", after_text
		print "\n"

	def repair_to_delete(self, t_node, inside = None, after = None):
		# pdb.set_trace()
		if get_type(t_node)[0] not in ['i','e']:
			if inside:
				inside_text = inside.label
				m = re.search(r"\d", inside_text)
				if m:
					inside_text = inside_text[:m.start()] + " #"+ inside_text[m.start()]
			else:
				inside_text = 'None'

			if after:
				after_text = after.label
				m = re.search(r"\d", after_text)
				if m:
					after_text = after_text[:m.start()] + " #"+ after_text[m.start()]
			else:
				after_text = 'None'

			m = re.search(r"\d", t_node.label)
			if m:
				ttext = t_node.label[:m.start()] + " #"+ t_node.label[m.start()]
		
			
			print "* Delete", ttext, ";Inside -", inside_text, ";After -", after_text
			print "\n"

		self.delete_loop_structure(t_node, inside, after)



	def add_if_structure(self, ls, inside, if_block):



		ln = "IF"+re.search(r'\d+', if_block).group()
		ib = self.loop_nodes[ln]

		for key in ls.keys():
			if key[0] == 'i':
				block = self.get_struct_nodes(ls[key])
				if type(block) != c_ast.Compound:
					block = c_ast.Compound([block])

				ib.iftrue = block

			elif key[0] =='e':
				else_block = self.get_struct_nodes(ls[key])
				if type(else_block) != c_ast.Compound:
					else_block = c_ast.Compound([else_block])
				ib.iffalse = else_block

	def add_loop_structure(self, ls, inside, after = None, inplace = None):
		# pdb.set_trace()
		if inplace:
			inplace = self.all_ast_nodes[inplace.label]
		if after:
			if after.label in self.all_ast_nodes.keys():
				self.all_ast_nodes[after.label]

		inside_ast = self.all_ast_nodes[inside.label]

		if type(inside_ast) == c_ast.FuncDef:
			inside_ast = inside_ast.body
		elif type(inside_ast) in [c_ast.For, c_ast.While, c_ast.DoWhile]:
			i = inside_ast.stmt
			if type(i) != c_ast.Compound:
				i = c_ast.Compound([i])
				inside_ast.stmt = i

			inside_ast = inside_ast.stmt

		if type(inside_ast) == c_ast.Compound:
			if inplace:
				inside_ast.block_items = [i if i!=inplace else ls for i in inside_ast.block_items]		

			else:
				# if after ==None:
				if inside_ast.block_items:
					inside_ast.block_items.append(ls)
				else:
					inside_ast.block_items = [ls]
				# else:
				# 	index = inside_ast.block_items.index(after)
				# 	inside_ast.block_items = inside_ast.block_items[:index+1] + ls + inside_ast.block_items[index+1:]
		elif type(inside_ast) == c_ast.If:
			if type(after) == Node:
				if after.label[0] == 'i':
					inside_ast.iffalse = ls
				else:
					inside_ast.iftrue = ls
			else:
				inside_ast.iftrue = ls

		# else:
		# 	pdb.set_trace()




	def delete_loop_structure(self, t_node, inside, after):

		if type(inside.ast_node) == c_ast.FuncDef:
			inside.ast_node.body.block_items.remove(t_node.ast_node)

		if type(inside.ast_node) == c_ast.Compound:
			inside.ast_node.block_items.remove(t_node.ast_node)

		elif type(inside.ast_node) in [c_ast.For, c_ast.While, c_ast.DoWhile]:
			inside.ast_node.stmt.block_items.remove(t_node.ast_node)

		elif type(inside.ast_node) == c_ast.If:
			if t_node.label[0] == 'i':
				inside.ast_node.iftrue = None

			elif t_node.label[0] == 'e':
				inside.ast_node.iffalse = None



	def get_struct_nodes(self, root):
		if root.label in self.matching.values():
			rmap = {self.matching[key]:key for key in self.matching.keys()}
			return self.all_ast_nodes[rmap[root.label]]
		if root.label in self.insert_nodes.keys():
			return self.insert_nodes[root.label]

		node_type = get_type(root)
		tree_node = None
		if node_type in ['For', 'While', 'DoWhile']:
			inner = []
			for c in root.children:
				c_node = self.get_struct_nodes(c)
				if c_node:
					inner.append(c_node)
			inner = c_ast.Compound(inner)
			# n_t = c_ast.For if node_type=='For' else c_ast.While if node_type=='While' else c_ast.DoWhile
			if node_type =='For':
				tree_node = c_ast.For(None, None, None, inner)
			elif node_type == 'While':
				tree_node = c_ast.While(None, inner)
			else:
				tree_node = c_ast.DoWhile(None, inner)


		if node_type == 'IF':
			if_block = None
			else_block = None
			for c in root.children:
				if c.label[0] == 'i':
					if_block = self.get_struct_nodes(c)
					if if_block==None:
						if_block = c_ast.Compound([])
				elif c.label[0] == 'e':
					else_block = self.get_struct_nodes(c)
					if else_block == None:
						else_block = c_ast.Compound([])

			tree_node = c_ast.If(None, if_block, else_block)
		if node_type =='i' or node_type == 'e':
			# pdb.set_trace()
			inner = []
			for c in root.children:
				c_node = self.get_struct_nodes(c)
				if c_node:
					inner.append(c_node)

			tree_node = c_ast.Compound(inner)



		return tree_node

	def get_cost(self, ls):
		cost = 0
		t = get_type(ls)
		
		if t=='Loop':
			cost += (1+ self.get_cost(ls[ls.keys()[0]]))
		elif t=='If':
			if_block=ls[ls.keys()[0]]
			cost+=(1+self.get_cost(if_block))
			if len(ls.keys())==2:
				else_block = ls[ls.keys()[1]]
				cost += (1+self.get_cost(else_block))

		elif t=='List':
			for i in ls:
				cost+=self.get_cost(i)
		else:
			return 0

		return cost




def desc_struct(ls, depth = 0):
	s = ""
	if get_type(ls) in ['For', 'While', 'DoWhile']:
		# pdb.set_trace()
		s+=depth*'  '+get_type(ls)+"(...){\n"

		for c in ls.children:
			s+=desc_struct(c, depth+1)

		s+=depth*'  '+"}\n"
	elif get_type(ls) == 'IF':
		s+=depth*'  '+"if(...){\n"
		s+=desc_struct(ls.children[0], depth+1)
		s+=depth*'  '+"}\n"

		if len(ls.children) ==2:
			s+=depth*'  '+"else{\n"
			s+=desc_struct(ls.children[1], depth+1)
			s+=depth*'  '+"}\n"


	elif get_type(ls)[0] in ['i', 'e']:
		for c in ls.children:
			s+=desc_struct(c, depth+1)


	return s

def get_loop_numbers(ls):
	nums = []
	if type(ls) == dict:
		# pdb.set_trace()
		nums.append(ls.keys()[0])
		nums+=get_loop_numbers(ls[ls.keys()[0]])
	elif type(ls) == list:
		for i in ls:
			nums += get_loop_numbers(i)
	elif type(ls)==int:
		nums.append(ls)
	return nums

def get_struct_numbers(ls):
	nums = []
	if get_type(ls) == 'Loop':
		nums.append(ls.keys()[0])
		if len(ls.keys()) ==2:
			nums.append(ls.keys()[1])
		# nums+=get_loop_numbers(ls[ls.keys()[0]])

	if get_type(ls) == 'If':
		nums.append(ls.keys()[0])
		if len(ls.keys())==2:
			nums.append(ls.keys()[1])

	elif type(ls) == list:
		for i in ls:
			nums += get_loop_numbers(i)
	elif type(ls)==int:
		nums.append(ls)
	elif type(ls)==str:
		nums.append(ls)
	return nums



def get_type(node):
	m = re.search(r"\d", node.label)
	if m:
		return node.label[:m.start()]
	else:
		return node.label


def type_dist(l1, l2):
	pass


# count = 0



if __name__== "__main__":
	if len(sys.argv) < 3:
		print "enter filenames and/or function name"
		sys.exit(1) 

	ast1 = pycparser.parse_file(sys.argv[1])
	ast2 = pycparser.parse_file(sys.argv[2])
	fname = sys.argv[3]

	print "Original Program"
	generator = c_generator.CGenerator()
	print generator.visit(ast2)

	# ast.show()
	print "Loop structure"
	ls1 = getLoopStructure(fname, ls_type = 'c')
	ls2 = getLoopStructure(fname)

	
	ls1.visit(ast1)
	ls2.visit(ast2)
	print "Struct 1"
	print [i.label for i in ls1.loopStruct.iter()]

	print "Struct 2"
	print [i.label for i in ls2.loopStruct.iter()]





	# global count
	# count =0
	# visit_ls(ls.loopStruct)

	ls2.getStructDiff(ls1.loopStruct, ls2.loopStruct)
	# pdb.set_trace()

	print "Struct 2"
	print [i.label for i in ls2.loopStruct.iter()]


	print "NEW Program"
	generator = c_generator.CGenerator()
	print generator.visit(ast2)



