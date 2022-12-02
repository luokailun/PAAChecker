
import pddl
from program import normalize
import itertools
import copy

def __get_formula_atoms(fluent_maps):
	
	f_fluents = list()
	for fluent_map in fluent_maps:
		f_fluents.append(pddl.Atom("f_"+fluent_map.fluent_name, [ p.name for p in fluent_map.parameters]))

	return f_fluents



def __get_program_atoms(action_maps):
	
	p_fluents = list()
	for action_map in action_maps:
		p_fluents.append(pddl.Atom("p_"+action_map.action_name, [ p.name for p in action_map.parameters]))

	return p_fluents


def __get_action_atoms(actions):

	a_fluents = list()
	for action in actions:
		a_fluents.append(pddl.Atom(action.name, [ p.name for p in action.parameters]))
	return a_fluents


def __extend_action_effect(actions, atoms):
	
	new_actions = list()

	for e, action in enumerate(actions):
		new_action = copy.deepcopy(action)
		new_action.effects.append(pddl.Effect(list(), pddl.Truth(), atoms[e]))
		new_actions.append(new_action)

	return new_actions



def __get_program_actions(action_maps, p_atoms, task):

	#p_atoms = __get_program_atoms(action_maps)

	new_actions = list()
	for e, action_map in enumerate(action_maps):
		effects = [pddl.Effect(list(), pddl.Truth(), p_atoms[e])]
		DNF_program = normalize.build_DNF_program(action_map.program)


		for k, seq_program in enumerate(normalize.split_nondeterministic(DNF_program)):
			# print("###program.......")
			# seq_program.dump()
			# print("###program.......")
			seq_program = normalize.move_pi_quantifiers(seq_program).simplified()
			paras, seq_program = normalize.eliminate_pi_quantifiers(seq_program)

			for n, simple_seq_program in enumerate(normalize.get_restricted_sequential_programs(seq_program, action_map.type_map, task)):


				test_action_paras, simple_seq_program = normalize.eliminate_test_action_quantifiers(simple_seq_program)

				new_action_name = action_map.action_name + "_" + str(k)+ str(n)
				new_action_paras = action_map.parameters + list(paras)+ test_action_paras
				
				precondition = simple_seq_program.to_program_condition().simplified()

				new_action = pddl.Action(new_action_name, new_action_paras, 0, precondition, effects, 0)
				#new_action = pddl.Action(new_action_name, new_action_paras, len(new_action_paras), precondition, effects, 0)
				new_actions.append(new_action)


	return new_actions


def __get_formula_actions(fluent_maps, f_atoms):

	f_actions = list()
	for e, fluent_map in enumerate(fluent_maps):
		pos_precondition = fluent_map.condition
		pos_effects = [ pddl.Effect(list(), pddl.Truth(), f_atoms[e]) ]
		#f_actions.append(pddl.Action(fluent_map.fluent_name, fluent_map.parameters, len(fluent_map.parameters), precondition, effects, 0))
		f_actions.append(pddl.Action(fluent_map.fluent_name, fluent_map.parameters, 0, pos_precondition, pos_effects, 0))

		neg_precondition = fluent_map.condition.negate()
		neg_effects = [ pddl.Effect(list(), pddl.Truth(), f_atoms[e].negate()) ]
		#f_actions.append(pddl.Action(fluent_map.fluent_name, fluent_map.parameters, len(fluent_map.parameters), precondition, effects, 0))
		f_actions.append(pddl.Action(fluent_map.fluent_name, fluent_map.parameters, 0, neg_precondition, neg_effects, 0))

	return f_actions




def build_extended_element(mapping, task):

	###########################################################################################
	## 2 kinds of fluents: program_fluents, formula_fluents 
	## 2 kinds of actions: 
	##					   1. actions affecting program_fluents
	##					   2. actions affecting formula_fluents
	###########################################################################################
	#
	# 
	# Here program actions will only mark which actions should be grounded, by taking actions as atoms in the precondition. 
	#
	#

	p_atoms = __get_program_atoms(mapping.action_maps)
	p_actions = __get_program_actions(mapping.action_maps, p_atoms, task)


	f_atoms = __get_formula_atoms(mapping.fluent_maps)
	f_actions = __get_formula_actions(mapping.fluent_maps, f_atoms)

	return p_actions, f_actions






