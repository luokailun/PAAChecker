



import pddl
from program.normalize import build_DNF, split_disjunctions, split_conjunctions
from ets import lset_op


def __get_axiom_effect(name, axioms):
	for axiom in axioms:
		if name == axiom.name:
			return axiom.effect


def __get_axiom_condition(name, axioms):

	mlist = list()
	for axiom in axioms:
		if name == axiom.name:
			mlist.append(pddl.Conjunction(axiom.condition))

	return pddl.Disjunction(mlist)


def get_axiom_condition_dict(axioms):

	#
	#   axiom name: DNF atom list
	#
	
	name_set = set(a.name for a in axioms)

	axiom_condition_dict = {}
	for name in name_set:
		condition = __get_axiom_condition(name, axioms)
		effect = __get_axiom_effect(name, axioms)
		axiom_condition_dict[str(effect)] = [ set(split_conjunctions(c)) for c in split_disjunctions(build_DNF(condition))]
		axiom_condition_dict[str(effect.negate())] = [ set(split_conjunctions(c)) for c in split_disjunctions(build_DNF(condition.negate()))]
	
	return axiom_condition_dict


#####################################################################################################################


def __regression(element, results, action_precondition_dict, action_effect_dict, atomic_action_dict, grounded_actions):
	
	ground_action_name = "(%s %s)"%(element.predicate, " ".join(element.args))
	action_name = element.predicate

	if action_name in atomic_action_dict:

		if ground_action_name not in action_precondition_dict:

			inst_action = atomic_action_dict[action_name].instantiate_with_paras(element.args)
			grounded_actions.append(inst_action)
			#action_precondition_dict = { a.name: set(a.precondition) for a in grounded_actions }
			#action_effect_dict = { a.name: { l for c, l in a.add_effects} |  { l.negate() for c, l in a.del_effects}  for a in grounded_actions }
			action_precondition_dict[inst_action.name] = set(inst_action.precondition)
			action_effect_dict[inst_action.name] = { l for c, l in inst_action.add_effects} |  { l.negate() for c, l in inst_action.del_effects}

		pre = action_precondition_dict[ground_action_name] 
		eff = action_effect_dict[ground_action_name]

		results = [lset_op.cir_minus(r, eff) for r in results]
		# print("---rrrrrr---")
		# print(results)
		results = [lset_op.uplus(pre, r) for r in results if r is not None]
		# print("---rrrrrr222---")
		# print(results)
		return [ r for r in results if r is not None]

	else:
		tests = [{element}]
		results = [ lset_op.uplus(t,r)  for t in tests for r in results] 
		return [r for r in results if r is not None]




def get_program_action_precondition(program_action, action_precondition_dict, action_effect_dict, atomic_action_dict, grounded_actions):

	results = [set()]
	for elem in reversed(program_action.precondition):
		results = __regression(elem, results, action_precondition_dict, action_effect_dict, atomic_action_dict, grounded_actions)

	return results




#####################################################################################################################

def __prog(lset, eff):

	result = (lset - eff - lset_op.negate(eff)) | eff
	return result


def __progression(results, element, action_effect_dict):

	name = "(%s %s)"%(element.predicate, " ".join(element.args))

	if name in action_effect_dict:
		eff = action_effect_dict[name]
		results = [ __prog(r, eff) for r in results]
		return results
	else:
		return results


def get_program_action_effect(program_action, action_effect_dict):

	results = [set()]
	for elem in program_action.precondition:
		results = __progression(results, elem, action_effect_dict)

	return results


#####################################################################################################################


def __unify_name(name, name_set):
    if name not in name_set:
        name_set.add(name)
        return name
    for counter in itertools.count(1):
        new_name = name + "_v"+str(counter)
        if new_name not in name_set:
            name_set.add(new_name)
            return new_name


def __check_pre(precondition, fluent_facts, init_facts):

	# print("-----")
	# print(precondition)
	# print(fluent_facts)
	# print("-----")

	new_pre = set()
	for p in precondition:
		if isinstance(p, pddl.Atom):
			if p in fluent_facts:
				new_pre.add(p)
			elif p not in init_facts:
				return None	
		elif isinstance(p, pddl.NegatedAtom):
			if p.negate() in fluent_facts:
				new_pre.add(p)
			elif p.negate() in init_facts:
				return None
		else:
			print("ERROR in __check_pre")
			exit(0)

	#print("results-----")
	#print(new_pre)
	return new_pre


def __simplify_effs(effects, fluent_facts):

	new_effs = set()
	for l in effects:
		if isinstance(l, pddl.Atom) and l in fluent_facts:
			new_effs.add(l)
		elif isinstance(l, pddl.NegatedAtom) and l.negate() in fluent_facts:
			new_effs.add(l)

	#print("############EFEFE")
	#print(new_effs)
	return new_effs


import itertools



def from_program_actions_to_actions(program_actions, atomic_actions, fluent_facts, init_facts):


	program_atoms = { a.add_effects[0][1] for a in program_actions }

	#action_precondition_dict = { a.name: set(a.precondition) for a in grounded_actions }
	#action_effect_dict = { a.name: { l for c, l in a.add_effects} |  { l.negate() for c, l in a.del_effects}  for a in grounded_actions }
	atomic_action_dict = {action.name: action for action in atomic_actions}
	action_precondition_dict = dict()
	action_effect_dict = dict()
	

	name_set = set()
	grounded_program_actions = list()
	num = len(program_actions)
	turn = pddl.Atom("turn", [])
	neg_turn = turn.negate()

	grounded_actions = []
	for e, p_action in enumerate(program_actions):

		# print("hello-------")
		# p_action.dump()

		pos_p = {l for c, l in p_action.add_effects if l.predicate.find("p_") == 0}
		neg_p = { l.negate() for l in program_atoms - pos_p }

		if e%100==0:
			print("finish %s/%s"%(e,num))

		pre_cond_list = get_program_action_precondition(p_action, action_precondition_dict, action_effect_dict, atomic_action_dict, grounded_actions)
		effs_list = get_program_action_effect(p_action, action_effect_dict)

		for pre_cond, effs in itertools.product(pre_cond_list, effs_list):
			# print("#####ppppppp")
			# print(pre_cond)

			pre_cond = __check_pre(pre_cond, fluent_facts, init_facts)
			if pre_cond is None:
				continue
			effs = __simplify_effs(effs, fluent_facts)
			if len(effs) == 0:
				continue

			new_name = __unify_name(p_action.to_ispl_action(), name_set)
			new_pre_cond = pre_cond | {neg_turn}
			new_effs = effs | {turn} | pos_p | neg_p

			grounded_program_actions.append(pddl.PropositionalSimpleAction(new_name, new_pre_cond, new_effs, 0))
			
	print("finish all! %s/%s"%(num,num))
	#print("delete useless atoms from actions...")


	return grounded_program_actions, program_atoms


#####################################################################################################################


def from_formula_actions_to_actions(grounded_f_actions):

	turn = pddl.Atom("turn", [])
	neg_turn = turn.negate()

	pre_cond = {turn}
	effs = list()
	effs.append(([],neg_turn))

	for action in grounded_f_actions:
		if len(action.add_effects) > 0:
			for cond, literal in action.add_effects:
				effs.append( (action.precondition, literal))
		else: 
			for cond, literal in action.del_effects:
				effs.append( (action.precondition, literal.negate()))

	return pddl.PropositionalAction("sense", pre_cond, effs, 0)


#####################################################################################################################
# import itertools


# def get_action_precondition_dict(actions, axiom_condition_dict):

# 	action_precondition_dict = dict()
# 	for action in actions:
# 		pre_list = list()
# 		for atom in action.precondition:
# 			if atom in axiom_condition_dict:
# 				pre_list.append([ conjunct.parts for conjunct in axiom_condition_dict[atom].parts] )
# 			else:
# 				pre_list.append([atom])

# 		action_precondition_dict[action.name] = [set(elem) for elem in itertools.product(*pre_list)]

# 	return action_precondition_dict

