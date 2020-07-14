
import pdb
from loop_structure import getLoopStructure
from pycparser import c_ast, c_generator
from c_parser import CParser


class force_matching:

    def __init__(self, f1, f2, astP, astQ, P, Q, fmap = None):

        self.f1 = f1
        self.f2 = f2
        self.force_m = {}
        self.astP = astP
        self.astQ = astQ

        if fmap:
            self.rmap = {v: k for k, v in fmap.items()} 
        else:
            self.rmap = None

        self.P = P
        self.Q = Q


        self.orig_locs = list(f2.loctrans.keys())
        self.new_locations = set()
        self.del_locations = set()
        self.struct_repair = {}

        self.sm_cost = 0

    def build_sm(self, loc1, loc2):
        # pdb.set_trace()
        # Check if already mapped
        if loc1 in self.force_m:
            return  self.force_m[loc1] == loc2
            # return sm[fnc1][loc1] == loc2

        # Check if loc2 already mapped
        if loc2 in self.force_m.values():
            # print "Failed here"
            return False
            #What to do here

        # Remember this pair
        self.force_m[loc1] = loc2

        # Check number of transitions
        n1 = self.f1.numtrans(loc1)
        n2 = self.f2.numtrans(loc2)
        
        if n1!=n2:
            return False

        # Done
        if n1 == 0:
            return True

        # Check True
        nloc1 = self.f1.trans(loc1, True)
        nloc2 = self.f2.trans(loc2, True)


        if not self.build_sm(nloc1, nloc2):
            return False
        if n1 == 1:
            return True

        # Check False
        nloc1 = self.f1.trans(loc1, False)
        nloc2 = self.f2.trans(loc2, False)
        

        return self.build_sm(nloc1, nloc2)


    def force_sm(self):
        # pdb.set_trace()
        self.force_m = {}
        # print self.f1.getstruct(), self.f2.getstruct()
        if self.rmap:
            ls1 = getLoopStructure(self.rmap[self.f1.name], ls_type = 'c')
        else:
            ls1 = getLoopStructure(self.f1.name, ls_type = 'c')
        ls2 = getLoopStructure(self.f1.name)

        ls1.visit(self.astP)
        ls2.visit(self.astQ)

        print "Number the loops in", self.f1.name, "in a serial fashion."
        print "Make the following structural edits to", self.f1.name, ":"
        ls2.getStructDiff(ls1.loopStruct, ls2.loopStruct)
        # pdb.set_trace()
        self.sm_cost = ls2.sm_cost

        
        print "Function", ls2.fname, "is changed to:"
        generator = c_generator.CGenerator()
        print generator.visit(ls2.all_ast_nodes[ls2.fname])

        parser = CParser()


        parser.visit(ls2.all_ast_nodes[ls2.fname])
        parser.postprocess()
        new_model = parser.prog

        # pdb.set_trace()

        self.Q.addfnc(new_model.getfnc(self.f1.name))
        self.f2 = new_model.getfnc(self.f1.name)

        # Start from initial locations
        # pdb.set_trace()
        if not self.build_sm(self.f1.initloc, self.f2.initloc):
            # pdb.set_trace()
            return False
        else:
            # print "New locations", self.new_locations
            # self.change_loc_descs()

            return self.force_m

    def get_loop_info(self):

        newloops = {}
        count = 0
        for addloc in self.f2.locs():
            # print self.new_locations[addloc]
            # self.new_locations[addloc]+=self.get_positions(addloc)
            # desc = self.new_locations[addloc][0]
            desc = self.f2.locdescs[addloc]
            # print addloc, "Desc", desc
            # pdb.set_trace()
            loop_info = ""
            try:
                line_no = int(desc[desc.find('line')+len('line')+1:])
            except:
                continue
            if "inside the body" in desc:
                loop_info = "body"
                line_no-=1
            if "the condition of" in desc:
                loop_info = "cond"
            if "update of the" in desc:
                loop_info = "update"
            # print loop_info, line_no, addloc 
            if loop_info!="":
                try:
                    newloops[line_no][loop_info] = addloc
                except:
                    newloops[line_no]={loop_info:addloc}
            # line_no = desc[]


        # print newloops

        # print "new_locations", self.new_locations
        # print "deleted locations", self.del_locations
        count = 1
        for line_no in sorted(newloops.keys()):
            newloops[line_no]["loop_count"] = count
            count +=1

        return newloops

    def change_loc_descs(self):
        loopinfo = self.get_loop_info()

        # print "loopinfo", loopinfo

        for newloc in self.f2.locs():
            desc = self.f2.locdescs[newloc]
            try:
                line_no = int(desc[desc.find('line')+len('line')+1:])
                if 'inside the body' in desc:
                    line_no-=1

                loop_count = loopinfo[line_no]["loop_count"]
            except:
                # pdb.set_trace()
                continue
            if len(loopinfo[line_no].keys())<4:
                continue
            desc = desc[:desc.find('loop')+4] +"#"+str(loop_count)
            # index = desc[:desc.find('loop')-1].rfind(' ')
            # desc = desc[:index]  desc [index:]

            self.f2.locdescs[newloc] = desc
            # pdb.set_trace()


   