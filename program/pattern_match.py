

import re
pattern_0 = r'\([^()]*\)'      #depth 0 pattern
pat_left_0 = r'\((?:[^()]|'    
pat_right_0 = r')*\)'

pattern_1 = r'\[[^\[\]]*\]'
pat_left_1 = r'\[(?:[^\[\]]|'    
pat_right_1 = r')*\]'




def __pattern_generate(pattern, pat_left, pat_right, depth=0):
    while(depth>0):
        pattern = pat_left + pattern + pat_right
        depth -= 1
    return pattern


def __parenthesis_depth(mstr):
	return mstr.count('(')-1


def __bracket_depth(mstr):
	return mstr.count('[')-1


def __parenthesis_pattern_genarate(depth=0):
	return __pattern_generate(pattern_0, pat_left_0, pat_right_0, depth)


def __bracket_pattern_genarate(depth=0):
	return __pattern_generate(pattern_1, pat_left_1, pat_right_1, depth)


'''
def pi_action_pattern_genarate(mstr):
	bracket_pattern = __bracket_pattern_genarate(__bracket_depth(mstr))
	pi_action_pattern = r"\s*pi\((?P<var>[A-Z\d,]+?)\)(?P<action>%s)"%bracket_pattern
	return pi_action_pattern
'''


def __mrepl_or(matched):
	return matched.group().replace('#','$')

def __mrepl_and(matched):
	return matched.group().replace(';','@')


def encode_or_in_parathesis(mstr):
	pattern = __parenthesis_pattern_genarate(__parenthesis_depth(mstr))
	pattern = re.compile(pattern)
	return pattern.sub(__mrepl_or, mstr)



def encode_or_in_bracket(mstr):
	pattern = __bracket_pattern_genarate(__bracket_depth(mstr))
	pattern = re.compile(pattern)
	return pattern.sub(__mrepl_or, mstr)



def encode_and_in_parathesis(mstr):
	pattern = __parenthesis_pattern_genarate(__parenthesis_depth(mstr))
	pattern = re.compile(pattern)
	return pattern.sub(__mrepl_and, mstr)



def encode_and_in_bracket(mstr):
	pattern = __bracket_pattern_genarate(__bracket_depth(mstr))
	pattern = re.compile(pattern)
	return pattern.sub(__mrepl_and, mstr)


def decode_and_or(mstr):
	return mstr.replace('$','#').replace('@',';')



def parse_pi_action(mstr):
	pi_action_pattern = r"\s*pi\((?P<var>[\w\d\s,-:_]+?)\)\[(?P<action>.+)\]"
	pi_action_pattern = re.compile(pi_action_pattern)
	match = pi_action_pattern.match(mstr)
	return match.group('var'), match.group('action')


def parse_parenthesis(mstr):
	strip_context = mstr.strip()
	strip_context = strip_context[1:len(strip_context)-1]
	return strip_context

def parse_sequential(mstr):
	return mstr.split(';')


def parse_non_deterministic(mstr):
	return mstr.split('#')







'''
def hell(mstr):
	print(mstr)


def mypring(mstr, f):
	f(mstr)


mypring("hello", hell)
'''



#mstr ="(|(|))| (|)"

#print(encode_or_in_parathesis(mstr))


'''
mstr = "pi(X)[[aaa][][](bbb)]"
k = pi_action_pattern_genarate(mstr)
print(k)
pattern = re.compile(k)
print(pattern.findall(mstr))
print()
'''
