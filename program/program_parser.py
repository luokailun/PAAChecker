
import re
from . import pattern_match
from translate import check



def __find_non_determin_not_in_priority(program):
	new_program = pattern_match.encode_or_in_parathesis(program)
	new_program = pattern_match.encode_or_in_bracket(new_program)
	if new_program.find('#')==-1:
		return False
	else:
		return True

def __find_seq_not_in_priority(program):
	new_program = pattern_match.encode_and_in_parathesis(program)
	new_program = pattern_match.encode_and_in_bracket(new_program)
	if new_program.find(';')==-1:
		return False
	else:
		return True


def match_nondertm_action(program):
	if program.find('#')==-1:
		return False
	elif __find_non_determin_not_in_priority(program) is True:
		return True
	else:
		return False



def match_seq_action(program):
	if program.find(';') ==-1:
		return False
	elif __find_seq_not_in_priority(program) is True:
		return True
	else:
		return False



def match_parenthesis(program):
	mstr = program.strip()
	if mstr[0]=='(':
		return True
	else:
		return False


def match_pi_action(program):
	mstr = program.strip()
	if mstr[0]=='p' and mstr[1]=='i' and mstr[2]=='(':
		return True
	else:
		return False

#     a ; b ; (c | d) |  d; e
# test whether | exits
# find | not in ()




def parse_nondertm_action(program):
	new_program = pattern_match.encode_or_in_parathesis(program)
	new_program = pattern_match.encode_or_in_bracket(new_program)
	sub_programs = pattern_match.parse_non_deterministic(new_program)
	#first_part, remain_part = first_part.replace('@','|'), remain_part.replace('@', '|')
	return sub_programs



def parse_seq_action(program):
	new_program = pattern_match.encode_and_in_parathesis(program)
	new_program = pattern_match.encode_and_in_bracket(new_program)
	sub_programs = pattern_match.parse_sequential(new_program)
	#first_part, remain_part = first_part.replace('@','|'), remain_part.replace('@', '|')
	return sub_programs



def parse_parenthesis(program):
	 strip_context = pattern_match.parse_parenthesis(program)
	 strip_context = pattern_match.decode_and_or(strip_context)
	 return strip_context







def parse_pi_action(program):
	
	variables, body  = pattern_match.parse_pi_action(program)
	variable_list = variables.split(',')
	body = pattern_match.decode_and_or(body)
	return (variable_list, body)




def parse(program):

	if match_nondertm_action(program) is True:
		#print('1\n')
		return 'non_deterministric', parse_nondertm_action(program)

	elif match_seq_action(program) is True:
		#print('2\n')
		return 'sequential', parse_seq_action(program)

	elif match_parenthesis(program) is True: 
		#print('3\n')
		return 'parenthesis', parse_parenthesis(program)

	elif match_pi_action(program) is True:
		#print('4\n')
		return 'pi_action', parse_pi_action(program)
	else:
		return 'single', program





#p = "pi(T1,T2)[R=rtA and cnroad(rtA,O,D)?;takeroad(X,T1,O,loc1); takeroad(X,T2,loc1,D)] | pi(T1,T2)[R=rtB and cnroad(rtB,O,D)?;takeroad(X,T1,O,loc3); takeroad(X,T2,loc3,D)] | pi(T1,T2)[R=rtA and cnroad(rtA,O,D)?;takeroad(X,T1,O,loc4); takeroad(X,T2,loc4,D)] "
#parse(p, "", fun)



