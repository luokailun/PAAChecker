

import re
import copy
import pddl




# def get_high_level_state_varas(varas):

# 	return [ p for p in varas if re.match(r"f_.+", p)]

# def get_program_varas(varas):

# 	return [p for p in varas if re.match(r"p_.+", p)]


def get_ispl_varas_dict(atoms):

	ispl_var_dict = dict()	
	for atom in atoms:
		ispl_var_dict[atom] = ('%s_%s'%(atom.predicate, '_'.join(atom.args))).replace("-", "__")
	#return '\n    '.join(ispl_var_list)
	return ispl_var_dict



########################################################################################################################

ispl = 'Semantics=SA;\n\
Agent Environment\n\
  Vars:\n\
  	 %s\n\
  end Vars\n\
  Actions = {none};\n\
  Protocol: Other: {none}; end Protocol \n\
  Evolution: \n\
	  %s \n\
  end Evolution \n\
end Agent\n \
\n\
Agent Player1\n\
  Lobsvars = {%s};\n\
  Vars:\n\
  	state: {none};\n\
  end Vars\n\
  Actions = {%s, none};\n\
  Protocol:\n\
	  %s \n\
	  Other: {none};\n\
  end Protocol \n\
  Evolution: \n\
	  state = none if state = none; \n\
  end Evolution \n\
end Agent\n \
\n\
Agent Player2\n\
  Lobsvars = {%s};\n\
  Vars:\n\
  	state: {none};\n\
  end Vars\n\
  Actions = {%s, none};\n\
  Protocol:\n\
	  %s \n\
	  Other: {none};\n\
  end Protocol \n\
  Evolution: \n\
	  state = none if state = none; \n\
  end Evolution \n\
end Agent\n \
\n\
Evaluation \n\
	%s \n\
end Evaluation \n\
\n\
InitStates \n \
	%s;\n\
end InitStates \n\
\n\
Formulae \n \
	%s \n\
end Formulae \n\
'



# Groups \n\
# 	%s; \n\
# end Groups \n\
# \n\

#   %p_varas, %f_varas, %varas
#   
#   Env has no actions but all updates
#   Env has all variables (i.e., %p_varas, %f_varas, %varas)
#   P1  has physical actions that change %varas and %p_varas (all updates are happened in Env)
#   P1  can observe %varas to see whether his action is possible    
#   P2  has the sensing action that change %f_varas (all updates are happened in Env)
#   P2  can observe %turn to see whether the sensing action is possible
#   P2  can observe $f_varas to check the K relation
#
#

#%(ispl_vars, ispl_updates, p1_actions, p1_poss, p2_actions, p2_poss, win_property, init)


def __get_ispl_vars_def(varas):

	ispl_var_list = list()	

	for vara in varas:
		ispl_type = 'boolean'
		ispl_var_list.append('%s:%s;'%(vara, ispl_type))

	return ispl_var_list



def __get_action_names(actions):

	return [ action.to_ispl_action() for action in actions]



def __get_ispl_poss(ispl_actions, actions, axiom_condition_dict, ispl_varas_dict):

	varas_dict =  { key: 'Environment.%s'%(value) for key, value in ispl_varas_dict.items()}

	ispl_poss = list()
	for e, action in enumerate(actions):
		# print("aaaaaa")
		# action.dump()
		ispl_poss.append("%s:{%s};"%(" and ".join([ atom.literal_replaced(axiom_condition_dict).to_ispl(varas_dict) \
			for atom in action.precondition ]), ispl_actions[e] ))
		#print("hello\n\n")
		# for atom in action.precondition:
		# 	atom.dump()
		# 	atom.literal_replaced(axiom_condition_dict).dump()

	# for a, k in axiom_condition_dict.items():
	# 	print(a)
	# 	k.dump()
	# 	print("---")

	# exit(0)
	return ispl_poss



def ____get_pos_cond(atom, grounded_actions):

	pos_conds = [conditions.Falsity()]
	for action in grounded_actions:
		for cond, fact in action.add_effects:
			if atom == fact:
				pos_conds.append(conditions.Conjunction(set(action.precondition)))
	return conditions.Disjunction(pos_conds)


def ____get_neg_cond(atom, grounded_actions):

	neg_conds = [conditions.Falsity()]
	for action in grounded_actions:
		for cond, fact in action.del_effects:
			if atom == fact:
				neg_conds.append(conditions.Conjunction(set(action.precondition)))
	return conditions.Disjunction(neg_conds)



# def __get_ispl_phy_update(update_varas_dict, ispl_actions, actions, flag_add, action_pre=""):


# 	update_list = list()
# 	ispl_actions = [ "%s%s"%(action_pre, action) for action in ispl_actions]

# 	for atom, ispl_vara in update_varas_dict.items():
# 		cond_str = ""
# 		for e, action in  enumerate(actions):
# 			if flag_add is True:
# 				#action.dump()
# 				cond_list = [ fact for fact in  action.add_effects if fact == atom ] 
# 				#print(cond_list)
# 			else:
# 				cond_list = [ fact for fact in  action.del_effects if fact == atom ]

# 			#cond.dump()
# 			if len(cond_list) == 0:
# 				continue
# 			else:
# 				cond_str += " %s or"%(ispl_actions[e])

# 		if cond_str == "":
# 			continue
# 		else:
# 			if flag_add is True:
# 				update_str = ("%s = true if %s"%(ispl_vara, cond_str)).rstrip(" or") + ";"
# 			else:
# 				update_str = ("%s = false if %s"%(ispl_vara, cond_str)).rstrip(" or")+ ";"

# 			update_list.append(update_str)
	
# 	return update_list


def __get_ispl_phy_update(update_varas_dict, ispl_actions, actions, action_pre=""):


	update_list = list()
	ispl_actions = [ "%s%s"%(action_pre, action) for action in ispl_actions]

	action_pos_update_dict = {atom: [] for atom in update_varas_dict.keys()}
	action_neg_update_dict = {atom: [] for atom in update_varas_dict.keys()}


	for e, action in  enumerate(actions):
		for fact in  action.add_effects:
			if fact in action_pos_update_dict:
				action_pos_update_dict[fact].append(ispl_actions[e])

		for fact in action.del_effects:
			if fact in action_neg_update_dict:
				action_neg_update_dict[fact].append(ispl_actions[e])

	update_list = []
	for atom, action_list in action_pos_update_dict.items():
		if len(action_list)!=0:
			ispl_vara = update_varas_dict[atom]
			cond_str = " or ".join(action_list)
			update_str = "%s = true if %s"%(ispl_vara, cond_str) + ";"
			update_list.append(update_str)
	
	for atom, action_list in action_neg_update_dict.items():
		if len(action_list)!=0:
			ispl_vara = update_varas_dict[atom]
			cond_str = " or ".join(action_list)
			update_str = "%s = false if %s"%(ispl_vara, cond_str) + ";"
			update_list.append(update_str)

	return update_list



def __get_ispl_sense_update(update_varas_dict, ispl_actions, actions, axiom_condition_dict, ispl_varas_dict, flag_add, action_pre=""):

	# print("-----")
	# print(axiom_condition_dict)
	# exit(0)
	update_list = list()
	ispl_actions = [ "%s%s"%(action_pre, action) for action in ispl_actions]

	for atom, ispl_vara in update_varas_dict.items():
		cond_str = ""
		for e, action in  enumerate(actions):
			if flag_add is True:
				#action.dump()
				cond_list = [ pddl.Conjunction(cond) for cond, fact in  action.add_effects if fact == atom ] + [pddl.Falsity()]
				#print(cond_list)
			else:
				cond_list = [ pddl.Conjunction(cond) for cond, fact in  action.del_effects if fact == atom ] + [pddl.Falsity()]

			#print("--fafdsf")
			cond = pddl.Disjunction(cond_list)
			#cond.dump()
			cond = cond.literal_replaced(axiom_condition_dict).simplified()
			#print(axiom_condition_dict)
			#cond.dump()
			if cond == pddl.Falsity():
				continue
			elif cond == pddl.Truth():
				cond_str += " %s or"%(ispl_actions[e])
			else:
				ispl_cond = cond.to_ispl(ispl_varas_dict)
				cond_str += " %s and %s or"%(ispl_cond, ispl_actions[e])

		if cond_str == "":
			continue
		else:
			if flag_add is True:
				update_str = ("%s = true if %s"%(ispl_vara, cond_str)).rstrip(" or") + ";"
			else:
				update_str = ("%s = false if %s"%(ispl_vara, cond_str)).rstrip(" or")+ ";"

			update_list.append(update_str)
	
	return update_list


def __get_turn_update(ispl_vara, phy_actions, sense_actions):

	ispl_phy_actions = [ "Player1.Action = %s"%action for action in  phy_actions]
	ispl_sense_actions = [ "Player2.Action = %s"%action for action in  sense_actions]

	update1 = "%s = true if %s;"%(ispl_vara, " or ".join(ispl_phy_actions))
	update2 = "%s = false if %s;"%(ispl_vara, " or ".join(ispl_sense_actions))
	update3 = "%s = true if Player1.Action = none and Player2.Action = none;"%(ispl_vara)

	return [update1, update2, update3]




def __get_ispl_init(atoms_init, ispl_varas_dict):

	ispl_inits = list()
	for atom, ispl_vara in ispl_varas_dict.items():
		if atom in atoms_init:
			ispl_inits.append( "Environment.%s = true"%ispl_varas_dict[atom])
		else:
			ispl_inits.append( "Environment.%s = false"%ispl_varas_dict[atom])
	return " and ".join(ispl_inits)


def __get_evaluation_sc(program_varas, sense_varas):

	import itertools
	eval_facts = list()
	eval_formulas = list()
	for e, (pvar, svar) in enumerate(itertools.product(program_varas, sense_varas)):
		e_fact = "p%s"%(str(e))
		e_formula = "%s if  Environment.%s = true and Environment.%s = true;"%(e_fact, pvar, svar)
		#e_formula = "%s if Environment.turn_ = false and  Environment.%s = true and Environment.%s = true;"%(e_fact, pvar, svar)

		eval_facts.append(e_fact)
		eval_formulas.append(e_formula)

	return eval_facts, eval_formulas


def __get_evaluation_dtm(program_varas, sense_varas):

	import itertools
	eval_facts = list()
	eval_formulas = list()
	for e, (pvar, svar) in enumerate(itertools.product(program_varas, sense_varas)):
		e_fact = "q%s"%(str(e))
		e_formula = "%s if  Environment.%s = false or Environment.%s = true;"%(e_fact, pvar, svar)
		#e_formula = "%s if Environment.turn_ = false and  Environment.%s = true and Environment.%s = true;"%(e_fact, pvar, svar)

		eval_facts.append(e_fact)
		eval_formulas.append(e_formula)

	return eval_facts, eval_formulas



def __get_check_formulas(eval_facts, eval_facts2, mode):
	
	template_sc = "AG ((turn_p1 and EX EX %s) -> K(Player2, EX EX %s));" 
	template_dtm = "AG ((turn_p1 and EX EX %s) ->  AX AX %s);" 

	if mode == "sc":

		return [ template_sc%(ef, ef) for ef in eval_facts ]

	elif mode == "dtm":

		return [ template_dtm%(ef1, ef2) for ef1, ef2 in zip(eval_facts, eval_facts2) ]

	elif mode == "sc_dtm":
		check_formulas = [ template_sc%(ef, ef) for ef in eval_facts ]
		check_formulas +=[ template_dtm%(ef1, ef2) for ef1, ef2 in zip(eval_facts, eval_facts2) ]
		return check_formulas

	else:
		print("ERROR")
		exit(0)







def to_ispl(ispl_varas_dict, ispl_p_varas_dict, ispl_f_varas_dict, init, actions, sense_action, axiom_condition_dict, mode):
	"""
	players: a list containing p1, p2
	modal_operator: G or F
	"""
	# print("hhhhh")
	# print(axiom_condition_dict)
	# exit(0)

	phy_varas =  ispl_varas_dict.values()
	sense_varas = ispl_f_varas_dict.values()
	prog_varas = ispl_p_varas_dict.values()

	ispl_actions = __get_action_names(actions)
	##
	## Note that actions' s axioms have been replaced
	ispl_p1_actions_poss = __get_ispl_poss(ispl_actions, actions, axiom_condition_dict, ispl_varas_dict)

	#print("11111111")
	ispl_sense_actions = __get_action_names([sense_action])
	ispl_p2_actions_poss = __get_ispl_poss(ispl_sense_actions, [sense_action], {}, ispl_varas_dict)
	# print(ispl_p2_actions_poss)
	# exit(0)
	#print("22222222")
	#sense_action.dump()
	phy_update_vara_dict = {}
	phy_update_vara_dict.update(ispl_varas_dict)
	phy_update_vara_dict.update(ispl_p_varas_dict)
	del phy_update_vara_dict[pddl.Atom('turn', [])]



	ispl_env_updates = __get_ispl_phy_update(phy_update_vara_dict, ispl_actions, actions,  "Player1.Action = ")

	# print(ispl_env_updates)
	# exit(0)
	ispl_env_updates += __get_ispl_sense_update(ispl_f_varas_dict, ispl_sense_actions, [sense_action], axiom_condition_dict, ispl_varas_dict, True, "Player2.Action = ")
	#print("5555555")
	ispl_env_updates += __get_ispl_sense_update(ispl_f_varas_dict, ispl_sense_actions, [sense_action], axiom_condition_dict, ispl_varas_dict, False, "Player2.Action = ")
	#print("6666666")
	ispl_env_updates += __get_turn_update('turn_', ispl_actions, ispl_sense_actions)
	ispl_env_updates += [" %s = false if Player1.Action = none and Player2.Action = none;"%pv for pv in  prog_varas]
	


	ispl_phy_vars_def = __get_ispl_vars_def(phy_varas)
	ispl_sense_vars_def = __get_ispl_vars_def(sense_varas)
	ispl_prog_vars_def = __get_ispl_vars_def(prog_varas)

	local_env_varas = '\n    '.join(ispl_phy_vars_def + ispl_sense_vars_def+ ispl_prog_vars_def)
	lobs_p1_varas = ','.join(phy_varas)
	lobs_p2_varas = ','.join(sense_varas) + ', turn_' 

	#print("777777777777")

	p1_actions = ','.join(ispl_actions)
	p2_actions = ','.join(ispl_sense_actions)

	#print("888888888888")
	p1_actions_poss = '\n    '.join(ispl_p1_actions_poss)
	p2_actions_poss = '\n    '.join(ispl_p2_actions_poss)

	#print("888888")
	env_updates = '\n    '.join(ispl_env_updates)
	#print("999999")

	all_varas_dict = {}
	all_varas_dict.update(ispl_varas_dict)
	all_varas_dict.update(ispl_p_varas_dict)
	all_varas_dict.update(ispl_f_varas_dict)

	init_formula = __get_ispl_init(init, all_varas_dict)

	evaluate_facts, evaluate_formulas = __get_evaluation_sc(prog_varas, sense_varas)
	evaluate_formulas = '\n    '.join(evaluate_formulas)
	evaluate_facts2 = evaluate_facts
	#print("bbbbbb")

	if mode == "dtm" or mode == "sc_dtm":
		evaluate_facts2, evaluate_formulas2 = __get_evaluation_dtm(prog_varas, sense_varas)
		evaluate_formulas = evaluate_formulas + '\n  ' + '\n    '.join(evaluate_formulas2)

	#print("ccccccc")
	evaluate_formulas = evaluate_formulas + '\n  ' + "turn_p1 if Environment.turn_ = false;"


	check_formulas = '\n    '.join(__get_check_formulas(evaluate_facts, evaluate_facts2, mode))

	ispl_text =  ispl%(local_env_varas, env_updates, lobs_p1_varas, p1_actions, p1_actions_poss, lobs_p2_varas,\
		p2_actions, p2_actions_poss, evaluate_formulas, init_formula, check_formulas)

	return ispl_text
