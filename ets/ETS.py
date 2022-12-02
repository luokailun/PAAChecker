




from ets import ispl_helper
import pddl



class ETS:

	def __init__(self, p_atoms, f_atoms, atoms, init, actions, sense_action, axioms):
		
		self.program_atoms = p_atoms
		self.formula_atoms = f_atoms
		self.atoms = atoms
		self.init = init
		self.actions = actions
		self.sense_action  = sense_action

		self.axiom_condition_dict = self.get_axiom_condition_dict(axioms)
		self.ispl_p_varas_dict = ispl_helper.get_ispl_varas_dict(self.program_atoms)
		self.ispl_f_varas_dict = ispl_helper.get_ispl_varas_dict(self.formula_atoms)
		self.ispl_varas_dict = ispl_helper.get_ispl_varas_dict(self.atoms)



	def __get_axiom_effect(self, name, axioms):
		for axiom in axioms:
			if name == axiom.name:
				return axiom.effect


	def __get_axiom_condition(self, name, axioms):

		mlist = list()
		for axiom in axioms:
			if name == axiom.name:
				mlist.append(pddl.Conjunction(axiom.condition))

		return pddl.Disjunction(mlist).simplified()


	def get_axiom_condition_dict(self, axioms):
		
		name_set = set(a.name for a in axioms)

		axiom_condition_dict = {}
		for name in name_set:
			condition = self.__get_axiom_condition(name, axioms)
			effect = self.__get_axiom_effect(name, axioms)
			axiom_condition_dict[str(effect)] = condition
			axiom_condition_dict[str(effect.negate())] = condition.negate()
		
		# print("hahahahahahah")
		# print(axioms)
		# print(axiom_condition_dict)
		return axiom_condition_dict


	def to_ispl(self, mode):

		# sense_varas = self.ispl_f_varas_dict.values()
		# env_varas =  set(self.ispl_p_varas_dict.values()) | set(self.ispl_varas_dict.values())
		# program_varas = self.ispl_p_varas_dict.values()

		#print("1111111111")

		ispl_formulation = ispl_helper.to_ispl(self.ispl_varas_dict, self.ispl_p_varas_dict, self.ispl_f_varas_dict, self.init, self.actions, self.sense_action, self.axiom_condition_dict,  mode)
		
		return ispl_formulation


	def dump(self):

		print("---variables:")
		for atom in self.atoms:
			print(atom)
		print("\n")
		print("---init:")
		for atom in self.init:
			print(atom)
		print("\n")
		print("---physical actions:")
		for action in self.actions:
			action.dump()

		print("---sensing action:")
		self.sense_action.dump()
		# print(env_varas)
		# print(sense_varas)





		
