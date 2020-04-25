import sys
import subprocess
import re
import argparse

from itertools import permutations
import functools

def get_inner(nested, count = 0):
    if all(type(x) == list for x in nested):
        return sum(map(get_inner, nested), [])
    return nested

def add_paren(ip, depth):

	for i in range(depth):
		ip = [ip]
	return ip

def permute_ip(ip):
	new_ip = []
	depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
	d = depth(ip)
	for i in ip:
		i = get_inner(i)
		if type(i) == list:
			new_ip+=list(permutations(i))
			print new_ip
	return [add_paren(list(i), d-2) for i in new_ip]
