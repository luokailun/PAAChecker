

import os
import re
import base64

import json
import itertools

from functools import reduce

import sys
sys.path.append("..")
#import util_constraint





'''
s = "exists(K11:Int)[numStone()=K11+3]"
universe = {'Int': ['1', '0', '3', '2'], '_S1': [], '_S2': ['p2', 'p1'], 'Bool': ['True', 'False']}
print grounding_formula(s)
exit(0)

'''




sub_lambda_exp = lambda x,y: re.sub(y[0],y[1],x)
replace_lambda_exp = lambda x,y: x.replace(y[0],y[1])
encode_pair_para = (['(',')',','],['[',']','#'])

# repeat to do function f with a list of arguments, initial argument is mbase
def repeat_do_function(f,args_list,mbase):
	return reduce(lambda x,y: f(x,y),args_list,mbase)


#def endecode_string_sub(my_str, old_symbols, new_symbols):
	#return repeat_do_function(sub_lambda_exp, zip(old_symbols, new_symbols), my_str)

def endecode_string(my_str, old_symbols, new_symbols):
	return repeat_do_function(replace_lambda_exp, zip(old_symbols, new_symbols), my_str)



def repeat_replace_inner_with_pattern(repeat_pattern, mrepl, my_str):
	while(True):
		encoded_str=repeat_pattern.sub(mrepl, my_str)
		my_str = encoded_str if my_str!=encoded_str else None
		if my_str is None:
			break	
	return encoded_str






