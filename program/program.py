


from literal import literal_operation
from literal import literal
from literal import action_literal
import pddl
import copy

class Program:

	def __init__(self, parts):
		self.parts = parts

	def dump(self, indent="  "):
		print("%s%s" % (indent, self._dump()))
		for part in self.parts:
			part.dump(indent + "  ")
	def _dump(self):
		return self.__class__.__name__


	def uniquify_variables(self, type_map, renamings={}):
		if not self.parts:
			return self
		else:
			return self.__class__([part.uniquify_variables(type_map, renamings)
                                   for part in self.parts])

	def get_quantified_variables(self):

		results = (part.get_quantified_variables() for part in self.parts)
		return sum(results, tuple())

	def free_variables(self):
		result = set()
		for part in self.parts:
			result |= part.free_variables()
		return result


	def simplified(self):
		return self




class TestAction(Program):
	parts = []
	def __init__(self, condition):
		self.condition = condition

	def dump(self, indent="  "):
		#print("%s%s" % (indent, self._dump()))
		print("%s%s?" % (indent, self.condition.output_formula()))

		
	def uniquify_variables(self, type_map, renamings={}):
		
		return self.__class__(self.condition.uniquify_variables(type_map, renamings))

	def get_quantified_variables(self):

		return self.condition.get_quantified_variables()

	def free_variables(self):
		return self.condition.free_variables()

	def simplified(self):
		return TestAction(self.condition.simplified())


	def regression(self, lp_list, actions):
		
		if isinstance(self.condition, pddl.Conjunction):
			cond_lp = literal.Literal_Partition(self.condition.parts)
		else:
			cond_lp = literal.Literal_Partition([self.condition])

		new_lp_list = list()
		for lp in lp_list:
			new_lp_list+= literal_operation.uplus(lp, cond_lp)

		# print("#### --- Regression Test Action result")
		# for lp in new_lp_list:
		# 	lp.dump()
		# print("\n\n")
		return new_lp_list


	def progression(self, lp_list, actions):
		return lp_list


	def to_program_condition(self):

		return self.condition



class SimpleAction(Program):
	parts = []
	def __init__(self, name, args):
		self.name = name
		self.args = args

	def dump(self, indent="  "):
		action_str = "%s(%s)"%(self.name, ",".join(self.args))
		#print("%s%s" % (indent, self._dump()))
		print("%s%s" % (indent, action_str))


	def uniquify_variables(self, type_map, renamings={}):
		return self.rename_variables(renamings)

	def rename_variables(self, renamings):
		new_args = tuple(renamings.get(arg, arg) for arg in self.args)
		return self.__class__(self.name, new_args)

	def get_quantified_variables(self):
		return tuple()

	def free_variables(self):
		return {arg for arg in self.args if arg[0] == "?"}


	def get_lp_pre_eff(self, actions):


		the_action = None
		for action in actions:
			if action.name == self.name:
				the_action = action
		assert the_action is not None
		
		renamings = {arg.name: self.args[i] for i, arg in enumerate(the_action.parameters)}
        #return self.condition.uniquify_variables(dict(), renaming)

		lp_pre = action_literal.get_precondition_lp(the_action, renamings)
		lp_eff = action_literal.get_effect_lp(the_action, renamings)

		return lp_pre, lp_eff


	def regression(self, lp_list, actions):

		# print("\n\n#### --- Regression Simple Action result")
		# self.dump()
		# print("####")

		lp_pre, lp_eff = self.get_lp_pre_eff(actions)


		new_lp_list = list()
		for lp in lp_list:
			# print("\n\ninput---cir_minus")
			# lp.dump()
			# print("\n\ninput---cir_minus")
			# lp_eff.dump()
			results = literal_operation.cir_minus(lp, lp_eff)
			#print("\n\n@@@@ cir_minus results")
			# for r in results:
			# 	r.dump()
			new_lp_list+= results

		# print("\nnewnewnewnew\n")
		# print(new_lp_list)
		

		new_new_lp_list = list()
		for new_lp in new_lp_list:
			# print("\n\ninput---uplus")
			# new_lp.dump()
			# print("\n\ninput---uplus")
			# lp_pre.dump()
			results = literal_operation.uplus(lp_pre, new_lp)
			# print("\n\n@@@@ uplus results---")
			# for r in results:
			# 	r.dump()
			new_new_lp_list += results

		return new_new_lp_list


	def progression(self, lp_list, actions):
		
		lp_pre, lp_eff = self.get_lp_pre_eff(actions)
		lp_eff_neg = lp_eff.negation()

		new_lp_list = list()
		for lp in lp_list:
			 results = literal_operation.minus(lp, lp_eff)
			 for result in results:
			 	new_results = literal_operation.minus(result, lp_eff_neg)
			 	new_lp_list+= new_results


		new_new_lp_list = list()
		for new_lp in new_lp_list:
			results = literal_operation.plus(new_lp, lp_eff)
			new_new_lp_list += results

		# print("\n\nRegression Action Results:----\n\n")
		# for a in new_new_lp_list:
		# 	a.dump()
		# 	print("######-------")

		return new_new_lp_list
	

	def to_program_condition(self):

		return pddl.Atom(self.name, self.args)






class SequentailProgram(Program):

	def __init__(self, parts):
		self.parts = parts

	def simplified(self):
		parts = [ part.simplified() for part in self.parts]
		result_parts = []
		for part in parts:
		    if isinstance(part, SequentailProgram):
		        result_parts += part.parts
		    else:
		    	result_parts += [part]

		if len(result_parts) == 1:
		    return result_parts[0]
		return SequentailProgram(result_parts)

	def regression(self, lp_list, actions):
		
		results = lp_list
		for part in reversed(self.parts):
			results = part.regression(results, actions)


		# print("#### --- Regression Sequential Action result")
		# for lp in results:
		# 	lp.dump()
		# print("\n\n")
		return results

	def progression(self, lp_list, actions):

		results = lp_list
		for part in self.parts:
			results = part.progression(results, actions)

		return results

	def to_program_condition(self):

		return pddl.Conjunction([part.to_program_condition() for part in self.parts])


class NondeterministicProgram(Program):

	def __init__(self, parts):
		self.parts = parts

	def simplified(self):
		parts = [ part.simplified() for part in self.parts]
		result_parts = []
		for part in parts:
		    if isinstance(part, NondeterministicProgram):
		        result_parts += part.parts
		    else:
		    	result_parts += [part]

		if len(result_parts) == 1:
		    return result_parts[0]
		return NondeterministicProgram(result_parts)



class PiProgram(Program):

	def __init__(self, parameters, parts):

		self.parameters = tuple(parameters)
		self.parts = parts

	def _dump(self):
		arglist = ", ".join(map(str, self.parameters))
		return "%s pi(%s)" % (self.__class__.__name__, arglist)


	def uniquify_variables(self, type_map, renamings={}):
		renamings = dict(renamings) # Create a copy.
		new_parameters = [par.uniquify_name(type_map, renamings)
						for par in self.parameters]
		new_parts = [part.uniquify_variables(type_map, renamings) for part in self.parts]
		return self.__class__(new_parameters, new_parts)

	def get_quantified_variables(self):
		return self.parameters

	def free_variables(self):
		result = Program.free_variables(self)
		for par in self.parameters:
			result.discard(par.name)
		return result

	def simplified(self):
		return PiProgram(self.parameters, (self.parts[0].simplified(),))