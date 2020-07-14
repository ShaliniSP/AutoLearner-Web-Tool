# import clara
import subprocess
import os
import pdb
import glob
import itertools
import copy
import pdb
import re
import pycparser
import sys
import math
from pycparser import c_ast, c_generator
from clara.repair import Repair
from clara.feedback_repair import RepairFeedback


class deleteV(c_ast.NodeVisitor):
		def visit_FuncDef(self, node):
			node.body = c_ast.Compound([])

class Grader():

	def __init__(self, models, numc, numi, inter, ins, args, ignoreio, ignoreret, entryfnc, clara):
		print len(models), numc, numi
		self.models = copy.deepcopy(models)
		self.asts = copy.deepcopy(clara.asts)
		# print len(models), numc, numi

		self.numc = numc
		self.numi = numi
		self.clara = clara
		self.inter = inter
		self.ins = ins
		self.args = args
		self.ignoreio = ignoreio
		self.ignoreret = ignoreret
		self.entryfnc = entryfnc
		self.correct_pg = self.models[:numc]
		self.incorrect_pg = self.models[numc:numc+numi]
		self.correct_asts = []
		self.incorrect_asts = self.asts[numc:numc+numi]

		# self.ipgen = clara.ipgen
		# self.dce = clara.dce
		# self.fnmapping = clara.fnmapping
		# self.structrepair = clara.structrepair


	''' Make skeleton code of correct codes '''


	def remove_fnbody(self, ast, new_pgm_name):
		ast_copy = copy.deepcopy(ast)

		deleteV().visit(ast_copy)

		generator = c_generator.CGenerator()

		new_code = generator.visit(ast_copy)

		with open(new_pgm_name, 'w') as f:
			f.write(new_code)

	def grade(self):
		# cluster the correct specs
		# create dir
		# call feedback in a loop for each incorrect spec
		# pdb.set_trace()
		try:
			dirname = "Correct_clusters"
			os.mkdir(dirname)
		except:
			#run rm * 
			for f in set(glob.glob(dirname+'/*')):
				subprocess.call(["rm", f])
			print "Dir exists. Overwriting"

		# pdb.set_trace()
		self.clara.clusterdir = dirname
		self.clara.models = self.correct_pg
		print len(self.clara.models)
		self.clara.cluster()
		#pdb.set_trace()
		print "New", len(self.incorrect_pg)
		self.correct_clusters = []
		''' dict for skeleton codes '''
		self.empty_codes = []

		files = list(set(glob.glob(dirname+'/*')) - set(glob.glob(dirname+'/*.json')))
		max_cost = 0

		for cor in files:
			# ast1 = pycparser.parse_file(cor)
			cor_model, cor_ast = self.clara.process_source(cor)
			self.correct_asts.append(cor_ast)
			# remove_fnbody(ast1, "new_code.c")
			self.remove_fnbody(cor_ast, "new_code.c")
			e_model, e_ast = self.clara.process_source("new_code.c")

			self.empty_codes.append(e_model) #models of empty codes
			self.correct_clusters.append(cor_model)
			# pdb.set_trace()

			R = Repair(timeout=60, verbose=0,
                   allowsuboptimal=0,
                   cleanstrings=1, fnmapping = True, structrepair = True)
        	r = R.repair(cor_model, e_model, self.inter,
                     ins=self.ins, args=self.args, ignoreio=self.ignoreio,
                     ignoreret=self.ignoreret, entryfnc=self.entryfnc, astP = cor_ast, astQ = e_ast)
        	if r:
				txt = RepairFeedback(e_model, cor_model, r)
				txt.genfeedback()
				total_cost = 0
				for t in txt.feedback:
					c = re.search(r'\(cost(.*?)\)', t)
					cost_val = c.group(1).split("=")
					total_cost += eval(cost_val[1])
				total_cost += R.sm_cost
				if total_cost > max_cost:
					max_cost = total_cost

				# cost = re.findall(r'\(cost(.*?)\)', txt.feedback)
				# for c in costs:
				# 		cost_val = c.split("=")
				# 		total_cost += eval(cost_val[1])
				# if total_cost > max_cost:
				# 	max_cost = total_cost
		print "Max Cost:", max_cost
		# print math.pow(10, (1 - 51 / max_cost))


		# pdb.set_trace()
		cost_dict = {}
		for inc, inc_ast in zip(self.incorrect_pg, self.incorrect_asts):
			print "Repairing ", inc.name
			self.clara.models = self.correct_clusters+[inc]
			self.clara.asts = self.correct_asts + [inc_ast]
			total_cost = 0
			# pdb.set_trace()

			try:
				fb = self.clara.feedback()
				# sm_cost = clara.sm_cost
				total_cost = None
				for f in fb:
					print f

					if total_cost == None:
						total_cost = f
					# costs = re.findall(r'\(cost(.*?)\)', f)
					# for c in costs:
					# 	cost_val = c.split("=")
					# 	total_cost += eval(cost_val[1])
				# total_cost+=sm_cost
				if(total_cost != 0):
					cost_dict[inc.name] = total_cost
				else:
					cost_dict[inc.name] = -1
			except:
				cost_dict[inc.name] = -1
				continue

		a1_sorted_keys = sorted(cost_dict, key=cost_dict.get)

		print "Ranking:"
		i = 0
		costs = list(cost_dict.values())
		#m = max(costs)
		for r in a1_sorted_keys:
			marks = math.pow(10, (1 - cost_dict[r] / max_cost))
			if cost_dict[r] !=-1:
				print i + 1, ".", r, " Cost: ", cost_dict[r], " Marks: ", round(marks, 1)
				i += 1
			# else:
			# 	print "No repairs were generated for", r

