'''
Simulation relation
'''

# clara imports
from common import debug, equals
from interpreter import Interpreter, RuntimeErr, UndefValue, isundef
from model import SPECIAL_VARS, VAR_RET, VAR_IN, VAR_OUT, isprimed, prime, Var, Op
from matching import Matching
from itertools import permutations
from copy import deepcopy
from forcematching import force_matching

import pdb


def get_signature(fname):
    if fname.params ==[]:
        return fname.rettype
    else:
        return (fname.rettype, tuple([p[1] for p in fname.params]))
        # print "signature", x
        # return x


class Fn_Matching(Matching):


    def __init__(self, ignoreio=False, ignoreret=False, verbose=False,
                 debugvar=None, bijective=True, fnmapping = False, structrepair = False):
        super(Fn_Matching, self).__init__(ignoreio, ignoreret, verbose, debugvar, bijective)
        
        self.fnmapping = fnmapping
        self.structrepair = structrepair
        self.fmap = {}

    def replace_fnCalls(self, expr, fmap):
        if hasattr(expr, 'name'):
            if expr.name == 'FuncCall':
                # print "found fn call"
                expr.args[0] = Var(fmap[expr.args[0].name])
        if hasattr(expr, 'args'):
            for arg in expr.args:
                self.replace_fnCalls(arg, fmap)


    def rename_fncs(self, P, fmap):

        for fp in fmap.keys():
            if fp==fmap[fp]:
                continue
            f = P.getfnc(fp)
            f.name = fmap[fp]
            P.addfnc(f)
            P.rmfnc(fp)

    def rename_fnCalls(self, P, fmap):
        for fname in P.getfncs():
            for loc in fname.locs():
                new_exprs = []
                for (var,expr) in fname.exprs(loc):
                    # try:
                        # print type(var), type(expr)
                        # print expr

                        self.replace_fnCalls(var, fmap)
                        self.replace_fnCalls(expr, fmap)
                        
                        # pdb.set_trace()
                        # if type(expr) == Op and expr.name == 'FuncCall':
                        # #     # print expr.name, expr.args
                        # #     # print type(expr.args[0])
                        #     # pdb.set_trace()
                        #     if expr.args[0].name in fmap.keys():
                        #         expr.args[0] = Var(fmap[expr.args[0].name])
                        #     # new_exprs.append((var,expr.replace_vars(fmap)))
                    # except:
                    #     continue
                # fname.replaceexprs(loc,new_exprs)

    def function_mapping(self, P,Q, entryfnc = None):
        # print "mapping functions"
        fncsP = P.getfncs()
        fncsQ = Q.getfncs()

        mapping = {}

        for fp in fncsP:
            # print fp.name, fp.rettype, fp.params
            if fp==entryfnc:
                continue
            sign = get_signature(fp)
            try:
                mapping[sign]['P'].append(fp.name)
            except KeyError:
                mapping[sign] = {'P':[fp.name], 'Q':[]}

        for fq in fncsQ:
            if fq==entryfnc:
                continue

            sign = get_signature(fq)
            try:
                mapping[sign]['Q'].append(fq.name)
            except KeyError:
                mapping[sign] = {'P':[],'Q':[fq.name]}

        # print mapping
        for key in mapping.keys():
            # if len(mapping[key]['P'])!=len(mapping[key]['Q']):
            #     # print "mapping failed"
            #     return 
            mapping[key]['iter'] = permutations(mapping[key]['P'])


        # return self.match_struct(P,Q)
        return mapping

    # @conditional_decorator(function_mapping, True)

    def MS(self, P,Q, astP = None, astQ = None):
        # print "in MS"
        fncs1 = P.getfncnames()
        fncs2 = Q.getfncnames()
        # Go through all functions
        sm = {}
        # if fmap==None:
        for fnc2 in fncs2:
            if fnc2 not in fncs1:
                self.debug("Function '%s' not found in P", fnc2)
                return
            
        for fnc1 in fncs1:

            if fnc1 not in fncs2:
                self.debug("Function '%s' not found in Q", fnc1)
                return

            f1 = P.getfnc(fnc1)
            f2 = Q.getfnc(fnc1)

            # Compare structure of two functions
            def build_sm(loc1, loc2):

                # Check if already mapped
                if loc1 in sm[fnc1]:
                    return sm[fnc1][loc1] == loc2

                # Check if loc2 already mapped
                if loc2 in sm[fnc1].values():
                    return False

                # Remember this pair
                sm[fnc1][loc1] = loc2

                # Check number of transitions
                n1 = f1.numtrans(loc1)
                n2 = f2.numtrans(loc2)
                if n1 != n2:
                    return False

                # Done
                if n1 == 0:
                    return True

                # Check True
                nloc1 = f1.trans(loc1, True)
                nloc2 = f2.trans(loc2, True)
                if not build_sm(nloc1, nloc2):
                    return False
                if n1 == 1:
                    return True

                # Check False
                nloc1 = f1.trans(loc1, False)
                nloc2 = f2.trans(loc2, False)
                return build_sm(nloc1, nloc2)

            # Start from initial locations
            sm[fnc1] = {}


            if not build_sm(f1.initloc, f2.initloc):
                if self.structrepair:
                    # print "HERES"
                    # pdb.set_trace()
                    if self.fnmapping:
                        fm = force_matching(f1,f2, astP, astQ, P, Q, fmap = self.fmap).force_sm()
                    else:
                        fm = force_matching(f1,f2, astP, astQ, P, Q).force_sm()
                    if fm!=False:
                        sm[fnc1] = fm
                    else:
                        return
                else:
                    return

        return sm

    def match_struct(self, P, Q, entryfnc = None, astP = None, astQ = None):

        fmapping = self.function_mapping(P,Q)
        # print fmapping
        # print len(fmapping.values())

        sm = self.MS(P,Q, astP, astQ)

        if self.fnmapping and fmapping:
            print "mapping functions"

            permLeft = True
            count = 0
            total = len(fmapping.keys())
            rmap = {}
            fmap = {entryfnc:entryfnc}
            self.fmap = fmap
            while sm==None and permLeft:
                print "mismatch"
                if len(rmap) > 0:
                    self.rename_fncs(P,rmap)
                    self.rename_fnCalls(P,rmap)

                # fmap = {}
                rmap = {}

                for sign in fmapping.keys():

                    try:
                        mapP = fmapping[sign]['iter'].next()
                        for fp,fq in zip(mapP, fmapping[sign]['Q']):
                            
                            fmap[fp] = fq
                            rmap[fq] = fp
                    except:
                        count+=1
                        if count == total:
                            permLeft = False
                
                if permLeft:
                    print "Mapping", fmap
                    self.rename_fncs(P,fmap)
                    self.rename_fnCalls(P,fmap)
                    # print P.getfncnames(), Q.getfncnames()
                    self.fmap = fmap
                    sm = self.MS(P,Q, astP, astQ)




        # else:
        # print "good", sm
        return sm
        
        
    def match_programs(self, P, Q, inter, ins=None, args=None,
                       entryfnc=None, timeout=5):

        # Check inputs and arguments
        assert ins or args, "Inputs or argument required"
        if ins:
            assert isinstance(ins, list), "List of inputs expected"
        if args:
            assert isinstance(args, list), "List of arguments expected"

        if ins and args:
            assert len(ins) == len(args), \
                "Equal number of inputs and arguments expected"

        # Check struct
        sm,fmap = self.match_struct(P, Q, entryfnc = entryfnc)
        if sm is None:
            self.debug("No struct match!")
            return

        # Populate ins or args (whichever may be missing)
        if not ins:
            ins = [None for _ in xrange(len(args))]
        if not args:
            args = [None for _ in xrange(len(ins))]

        # Create interpreter
        I = inter(timeout=timeout, entryfnc=entryfnc)

        # Init traces
        T1 = []
        T2 = []

        # Go through inputs and arguments
        for i, a in zip(ins, args):

            # Run both programs on each input and arg
            t1 = I.run(P, ins=i, args=a)
            t2 = I.run(Q, ins=i, args=a)

            T1.append(t1)
            # self.debug("P1: %s", t1)
            T2.append(t2)
            # self.debug("P1: %s", t2)

        self.debug("Programs executed, matching traces")

        # Match traces
        V1 = {f: P.getfnc(f).getvars() for f in P.getfncnames()}
        V2 = {f: Q.getfnc(f).getvars() for f in Q.getfncnames()}
        return self.match_traces(T1, T2, sm, V1, V2)
