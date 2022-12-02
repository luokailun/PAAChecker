



from . import global_variable
from pddl import conditions


# ##########################################################################################
# # from transformation to SMT format

# def get_replace_list():
# 	return global_variable.RPLIST

# def clear_replace_list():
# 	global_variable.RPLIST = list()
# 	global_variable.RP_INDEX =0


# def add_replace_list(elem):
# 	repl = "RP%s"%str(global_variable.RP_INDEX)
# 	global_variable.RP_INDEX+=1
# 	global_variable.RPLIST.append((r"\b%s\b"%repl, elem))
# 	return repl


def get_global_index():
	repl = "RP%s"%str(global_variable.RP_INDEX)
	global_variable.RP_INDEX+=1
	return repl

def get_global_dict():
	return global_variable.RP_DICT


def clear_global_dict():
	global_variable.RP_DICT = dict()
	global_variable.RP_INDEX =0




##########################################################################################



def add_fluent(fluent_name, paras):

	index = get_global_index()
	fluent = conditions.Atom(fluent_name, paras)
	global_variable.RP_DICT[index] = fluent
	return index


def add_math_formula(math_symbol, paras):

	index = get_global_index()
	fluent = conditions.Atom(math_symbol, paras)
	global_variable.RP_DICT[index] = fluent
	return index


def add_logic_formula(symbol, formula_indexs):


	index = get_global_index()
	formulas = [ global_variable.RP_DICT[formula_index] for formula_index in formula_indexs]

	if symbol == "not":

		assert len(formulas) == 1
		new_formula = formulas[0].negate()

	elif symbol == "and":

		new_formula = conditions.Conjunction(formulas)

	elif symbol == "or":

		new_formula = conditions.Disjunction(formulas)

	elif symbol == '=>':

		assert len(formulas) == 2

		new_formula = conditions.Disjunction([formulas[0].negate(), formulas[1]])

	elif symbol == '<=>':

		assert len(formulas) == 2

		left_formula = conditions.Disjunction([formulas[0].negate(), formulas[1]])
		right_formula = conditions.Disjunction([formulas[1].negate(), formulas[0]])
		new_formula = conditions.Conjunction([left_formula, right_formula])
	else:

		print("something is wrong!!!")
		print(symbol, formula_indexs)
		exit(0)

	
	global_variable.RP_DICT[index] = new_formula

	return index



def add_quntifier_formula(symbol, parameters, formula_index):

	index = get_global_index()
	formula = global_variable.RP_DICT[formula_index]

	if symbol == "forall":

		new_formula = conditions.UniversalCondition(parameters, [formula])

	elif symbol == "exists":

		new_formula = conditions.ExistentialCondition(parameters, [formula])


	global_variable.RP_DICT[index] = new_formula

	return index









