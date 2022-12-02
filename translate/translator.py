

import os

from . import util
from . import global_method
import re



most_inner_pattern = re.compile(r'\([^\(\)]+\)')


math_sym_first = re.compile(r'(?:(\w+)\s*(\*)\s*(\w+))|(?:(\w+)\s*(\/)\s*(\w+))|(?:(\w+)\s*(mod)\s*(\w+))')
#math_sym_second = re.compile(r'(?:(\w+)\s*(\+)\s*(\w+))|(?:(\w+)\s*(\-)\s*(\w+))')
math_sym_second = re.compile(r'(?:(\w+)\s*(\+)\s*(\w+))')
math_pred = re.compile(r'(?:(\w+)\s*(<=)\s*(\w+))|(?:(\w+)\s*(>=)\s*(\w+))|(?:(\w+)\s*(<)\s*(\w+))|(?:(\w+)\s*(>)\s*(\w+))|(?:(\w+)\s*(=)\s*(\w+))')
#logic_conn1 = re.compile(r'(not)\s*(\w+)(?!not\s*)')
logic_conn1 = re.compile(r'(not)\s*(?!not)(\w+)')
logic_conn2 = re.compile(r'(\w+)\s*(and)\s*(\w+)')
logic_conn3 = re.compile(r'(\w+)\s*(or)\s*(\w+)')
logic_conn4 = re.compile(r'(\w+)\s*(=>)\s*(\w+)')
logic_conn5 = re.compile(r'(\w+)\s*(<=>)\s*(\w+)')

quantifier_pattern = re.compile(r"(?:(forall|exists))\s*\(([\s\w:,_-]+)\)\[([^\(\)\[\]]+)\]")
##
##
# repeat most inner (exp):  
#	handle (exp)  
#		 exp:   basic expression    
#					math:   (1) * / mod  (2) + -         
#				    math predicate:    <= >=  <  >  =
# 		 		    logical connector ! &  |  => 
#
#	handle fluent(L1,L1,L1)   -> (fluent L1 L1 L1)
#	
#
#


#[2] construct math symbol
def __mrepl_math(matched):
	match_list = [ elem for elem in matched.groups() if elem]
	##print 'aaaa',match_list
	#s= "
	###print s
	return global_method.add_math_formula(match_list[0], match_list[1:])


#[3] construct not symbol
def __mrepl_logic(matched):
	match_list = [ elem for elem in matched.groups() if elem]
	symbol = match_list[1]
	match_list.remove(match_list[1])
	return global_method.add_logic_formula(symbol, match_list)

def __mrepl_logic_not(matched):
	match_list = [ elem for elem in matched.groups() if elem]
	return global_method.add_logic_formula(match_list[0], match_list[1:])


def __mrepl_no_inner_formula(matched):
	if matched.group().find(':')!=-1:
		return matched.group()
	formula = matched.group().lstrip('(').rstrip(')')
	#print "---before innerformula", formula
	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = math_sym_first.sub(__mrepl_math, formula, 1)
	#print '1111',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = math_sym_second.sub(__mrepl_math, formula, 1)
	#print '2222',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = math_pred.sub(__mrepl_math, formula, 1)
	#print '2222',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn1.sub(__mrepl_logic_not, formula)
	#print '3333',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn2.sub(__mrepl_logic, formula, 1)
	#print '4444',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn3.sub(__mrepl_logic, formula, 1)
	#print '5555',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn4.sub(__mrepl_logic, formula, 1)
	#print '6666',formula

	temp_formula =""
	while formula!=temp_formula:
		temp_formula = formula
		formula = logic_conn5.sub(__mrepl_logic, formula, 1)
	#print '7777',formula
	#print "----after,innerformula",formula
	return formula



#[1] construct fluent
def __mrepl_fluent(matched):
	match_list = [ elem for elem in matched.groups() if elem]
	# print("-----")
	# print(match_list)
	paras = match_list[1].split(',')
	return global_method.add_fluent(match_list[0], paras)



def __mrepl_quntifier(matched):
	paras = matched.group(2).split(',')
	formula = re.sub(r'.*', __mrepl_no_inner_formula, matched.group(3).strip())
	return global_method.add_quntifier_formula(matched.group(1), paras, formula)


def __logicSym_to_smtSym(formula):
	formula = formula.replace('!',' not ').replace('%',' mod ').replace('&',' and ').replace('|', ' or ')
	return util.repeat_do_function(util.sub_lambda_exp, [(r'\bFalse\b','false'), (r'\bTrue\b','true')] ,formula)


def translate(formula, fluents, constants):

	formula = __logicSym_to_smtSym(formula)
	def myFunc(e):
  		return len(e)
	fluents.sort(reverse=True, key=myFunc)
	fluent_sub = '|'.join([r"(?:(\b%s)\(?([\w,\?\s]*)\)?)"%fun for fun in fluents])
	#fluent_sub = fluent_sub.replace('_','\_')
	#print fluents
	fluent_sub_pattern = re.compile(fluent_sub)

	temp_formula = ""
	while temp_formula!= formula:
		temp_formula = formula
		#formula = fluent_sub_pattern.sub(__mrepl_fluent, formula)
		# print("fffffff")
		#print(formula)
		# print(fluents)
		# print(constants)
		# print(fluent_sub)
		# print(fluent_sub_pattern.findall(formula))
		formula = util.repeat_replace_inner_with_pattern(fluent_sub_pattern, __mrepl_fluent, formula)
		#print "repl_fluent---",formula
		#formula = Util.repeat_replace_inner_with_pattern(most_inner_pattern, __mrepl_no_inner_formula, formula)
		formula = most_inner_pattern.sub(__mrepl_no_inner_formula, formula)
		#print "inner_pattern---",formula
		formula = util.repeat_replace_inner_with_pattern(quantifier_pattern, __mrepl_quntifier, formula)
		#formula = quantifier_pattern.sub(__mrepl_quntifier, formula)
	formula = re.sub(r'.*', __mrepl_no_inner_formula, formula)
	formula = formula.strip()


	global_dict = global_method.get_global_dict()
	formula = global_dict[formula]
	global_method.clear_global_dict()

	from . import check

	condition = check.check_variables(formula, constants)

	return condition.simplified().uniquify_variables(dict())







