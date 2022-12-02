



from literal import literal
import pddl



def get_precondition_lp(action, renamings):

	if isinstance(action.precondition, pddl.Conjunction):
		pre_lp = literal.Literal_Partition(action.precondition.uniquify_variables(dict(),renamings).parts)
	else:
		pre_lp = literal.Literal_Partition([action.precondition.uniquify_variables(dict(),renamings)])
	return pre_lp


def get_effect_lp(action, renamings):

	return literal.Literal_Partition([eff.literal.uniquify_variables(dict(),renamings) for eff in action.effects])


# def actions_to_literal_structure(actions):

# 	actions_structure = dict()
# 	for action in actions:

# 		eff_lp = literal.Literal_Partition([eff.literal for eff in action.effects])
# 		actions_structure[action.name] = (pre_lp, eff_lp)
	
# 	return actions_structure

	#action
