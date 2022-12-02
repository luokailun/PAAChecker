
import pddl
from program import normalize
from literal import literal



# def __get_program_fluents(action_maps):
	
# 	p_fluents = list()
# 	for action_map in action_maps:
# 		p_fluents.append(pddl.Predicate("p_"+action_map.action_name, action_map.parameters))

# 	return p_fluents



def get_pysical_actions(action_maps, task):

	#p_fluents = __get_program_fluents(action_maps)
	actions = task.actions

	new_actions = list()
	for e, action_map in enumerate(action_maps):
		DNF_program = normalize.build_DNF_program(action_map.program)
		for k, seq_program in enumerate(normalize.split_nondeterministic(DNF_program)):
			# seq_program.dump()
			seq_program = normalize.move_pi_quantifiers(seq_program).simplified()
			paras, seq_program = normalize.eliminate_pi_quantifiers(seq_program)
			# print("#####")
			# seq_program.dump()
			# print("#####")
			for n, simple_seq_program in enumerate(normalize.get_restricted_sequential_programs(seq_program, action_map.type_map, task)):

				test_action_paras, simple_seq_program = normalize.eliminate_test_action_quantifiers(simple_seq_program)

				new_action_name = action_map.action_name +"_"+ str(k)+ str(n)
				new_action_paras = action_map.parameters + list(paras)+ test_action_paras
				
				# print(new_action_name)
				# print(new_action_paras)
				# print("----")
				pre_lps = simple_seq_program.regression([literal.Literal_Partition(list())], actions)
				# print("\n\n#################################\n")
				# for pre_lp in pre_lps:
				# 	#pre_lp.dump()
				# 	pre_cond = pre_lp.to_condition()
				# 	pre_cond.dump()
				# 	print("######\n")
				# print("\n\n#################################\n")

				pre_cond = pddl.Disjunction([ pre_lp.to_condition() for pre_lp in pre_lps]).simplified()
				pre_cond = pddl.Conjunction([pre_cond]).simplified()

				# pre_cond.dump()

				eff_lps = seq_program.progression([literal.Literal_Partition(list())], actions)

				eff_list = list()
				for eff_lp in  eff_lps:
					eff_list += eff_lp.to_effects()




				# print("---------------RRRResults\n\n\n")
				# for eff_lp in eff_lps:
				# 	eff_lp.dump()
				# 	print("\n\n")

				# exit(0)

				#eff_list.append(pddl.Effect([], pddl.Truth(), turn))

				# if p(\vec{x}) 
				# p_vars = [item.name for item in p_fluents[e].arguments]
				# p_literal = pddl.Atom(p_fluents[e].name,  p_vars)
				# eff_list.append(pddl.Effect([], pddl.Truth(), p_literal))
				# #print(p_fluents[e])

				# prime_args = [pddl.TypedObject(item.name+"_prime", item.type_name) for item in p_fluents[e].arguments]
				# prime_vars = [item.name for item in prime_args]
				# prime_cond = pddl.Disjunction([pddl.NegatedAtom("=", elem) for elem in zip(p_vars, prime_vars)])
				# prime_literal = p_literal.negate().uniquify_variables(list(),{var:p_var for  var, p_var in zip(p_vars, prime_vars)})
				
				# prime_effect = pddl.Effect(prime_args, prime_cond, prime_literal)
				# eff_list.append(prime_effect)
				# #prime_effect.dump()

				# for fluent in set(p_fluents)- set([p_fluents[e]]):
				# 	n_literal = pddl.NegatedAtom(fluent.name,  [item.name for item in fluent.arguments])
				# 	eff_list.append(pddl.Effect(fluent.arguments, pddl.Truth(), n_literal))


				new_action = pddl.Action(new_action_name, new_action_paras, 0, pre_cond, eff_list, 0)
				new_actions.append(new_action)

	# print("Physical actions -------------:\n")
	# for action in new_actions:
	# 	action.dump()
	return new_actions




