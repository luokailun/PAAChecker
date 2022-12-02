


from grounding import normalize
from grounding import pddl_to_prolog
from grounding import build_model
from grounding import instantiate
import itertools

# from ets.build_extended_task import build_extended_task
from ets.build_extended_element import build_extended_element
from ets.ETS import ETS
from ets import action_handler
from ets import sym_action
import re
import copy
import pddl






def __get_grounded_light(planning_task, action_ground_set):

	normalize.normalize(planning_task)

	prog = pddl_to_prolog.translate(planning_task)
	model = build_model.compute_model(prog)

	# print("-sasasa-----")
	# prog.dump()
	# print(model)
	# exit(0)

	fluents, actions, axioms, action_paras_dict = instantiate.instantiate_light(planning_task, model, action_ground_set)

	return fluents, actions, axioms, action_paras_dict



def __ground_actions(p_actions, action_paras_dict):

	# We assert that all the parameters tuple of an action are of the same length
	check_dict = {a: {len(p) for p in pset } for a, pset in action_paras_dict.items()}
	for a, len_set in check_dict.items():
		assert len(len_set) == 1

	grounded_actions = []
	for action in p_actions:
		for inst_paras in action_paras_dict[action.name]:
			variable_mapping = {par.name: arg for par, arg in zip(action.parameters, inst_paras) }
			inst_action = action.instantiate_full(variable_mapping)
			if inst_action:
				grounded_actions.append(inst_action)

	return grounded_actions



def __divide_atoms(grounded_atoms, pred_names):

	set1 = { a for a in grounded_atoms if a.predicate.find("p_") == 0}
	set2 = { a for a in grounded_atoms if a.predicate.find("f_") == 0}
	set3 = { a for a in grounded_atoms if a.predicate in pred_names}

	return set1, set2, set3


# def __del_self_pred(grounded_actions):

# 	for a in grounded_actions:
# 		effs = [ (cond, l) for cond, l in a.add_effects if "(%s %s)"%(l.predicate, " ".join(l.args)) != a.name]
# 		a.add_effects = effs
# 	return grounded_actions



def get_ETS(mytask, mapping):


	# we assume actions are having simple form:
	# 1. precondition is conjunction of literals
	# 2. effects have no conditions
	#
	for action in mytask.actions:
		assert not isinstance(action.precondition, pddl.Disjunction)
		for effect in action.effects:
			assert not isinstance(effect, pddl.UniversalEffect)
			assert not isinstance(effect, pddl.ConditionalEffect)



	p_actions, f_actions  = build_extended_element(mapping, mytask)



	##################
	# macro_actions are symbolic actions whole preconditions and effects built from programs
	# macro_actions are different from p_actions, in that p_actions doest not indeed build preconditions and effects
	#

	macro_actions = sym_action.get_pysical_actions(mapping.action_maps, mytask)

	###
	### IDEA: We do not directly ground macro_actions as they are very time-consuming. We just get 
	### all the possible parameters of macro_actions, and facts reachable from macro_actions. With
	### the facts, we can also ground f_actions ( which are used to construct sensing actions), 
	### whose grounding is not so time-consuming.
	###

	atomic_actions = mytask.actions
	mytask.actions = macro_actions +  f_actions
	action_ground_set = {a.name for a in f_actions}
	fluent_facts, grounded_f_actions, grounded_axioms, action_paras_dict = __get_grounded_light(mytask, action_ground_set)


	### 
	### IDEA: We then grounded p_actions using the possible parameters of macro_actions.
	### Note that as a p_action contains precondition which denotes a program, we indeed ground this program.
	###

	_, grounded_f_atoms, grounded_atoms = __divide_atoms(fluent_facts, { p.name for p in mytask.predicates})
	grounded_p_actions = __ground_actions(p_actions, action_paras_dict)


	###
	### IDEA: Using the grounded program (precondition), we get the actual precondition and effects.
	### ### It doest not need to ground atomic actions many times (like DP).
	###
	grounded_p_actions, grounded_p_atoms  = action_handler.from_program_actions_to_actions(grounded_p_actions, atomic_actions, grounded_atoms, mytask.init)
	###
	### Note that this action does not del axioms.
	### 
	sense_action = action_handler.from_formula_actions_to_actions(grounded_f_actions)

	# sense_action.dump()
	# exit(0)

	turn = pddl.Atom('turn',[])
	neg_turn = turn.negate()

	grounded_atoms = { atom for atom in grounded_atoms if atom.predicate!="=" and atom.predicate.find("new-axiom@")==-1 } \
				| {turn}
	init = {p for p in mytask.init if p in grounded_p_atoms or p in grounded_f_atoms or p in grounded_atoms  } \
				| {turn}

	# print("---numnumunum---")
	# print(len(new_actions))
	# print(len(grounded_atoms))
	# print(len(grounded_f_atoms))
	# print(len(grounded_p_atoms))

	# for a in new_actions:
	# 	a.dump()

	# print("\n\n\n")
	# for p in grounded_atoms: #| grounded_p_atoms | grounded_f_atoms:
	# 	print(p)
	# exit(0)
	return ETS(grounded_p_atoms, grounded_f_atoms, grounded_atoms, init, grounded_p_actions, sense_action,  grounded_axioms)
	




# def get_ETS(task, mapping):

# 	extended_task = build_extended_task(task, mapping)

# 	# for action in extended_task.actions:
# 	# 	action.dump()
# 	# exit(0)

# 	fluent_facts, grounded_actions, grounded_axioms = __get_grounded(extended_task)

# 	# for action in grounded_actions:
# 	# 	action.dump()
# 	# exit(0)

# 	varables = [ atom for atom in fluent_facts if atom.predicate!="=" and atom.predicate.find("new-axiom@")==-1]
# 	init = [p for p in extended_task.init if p in varables]


# 	# print("111111111")
# 	# print(len(grounded_actions))
# 	# # exit(0)


# 	name_set = set()
# 	sense_action = None
# 	new_grounded_actions = list()
# 	for e, action in enumerate(grounded_actions):
# 		new_name = __unify_name(action.to_ispl_action(), name_set)
# 		action.name =  "(%s )"%new_name
# 		#print(action.name)
# 		if re.match(r"\(sense \)", action.name) is not None:
# 			sense_action = action
# 		else:
# 			new_grounded_actions.append(action)

# 	assert sense_action is not None

# 	# print("44444444")
# 	# exit(0)

# 	







