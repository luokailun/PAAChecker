


import pddl
import copy

class Literal_EQC:

	def __init__(self, literal):
		self.predicate = literal.predicate
		self.paras_set =set()
		self.paras_set.add(literal.args)
		self.negated = literal.negated

	def is_eq(self, elem):

		return elem.predicate == self.predicate and self.negated == elem.negated


	def is_conflictive(self, elem):

		return elem.predicate == self.predicate and self.negated != elem.negated

	def is_relevant(self, elem):

		return elem.predicate == self.predicate


	def is_unique(self):
		if len(self.paras_set)==1:
			return True
		else:
			return False

	def add(self, literal):
		self.paras_set.add(literal.args)


	def add_EQC(self, eqc):

		new = copy.deepcopy(self)
		new.paras_set |= eqc.paras_set
		return new


	def remove_paras(self, paras):
		if len(self.paras_set) == 1:
			return None
		new = copy.deepcopy(self)
		new.paras_set.remove(paras)
		return new

	def to_condition(self):

		if self.negated is False:
			return pddl.Conjunction([pddl.Atom(self.predicate, paras) for paras in self.paras_set])
		else:
			return pddl.Conjunction([pddl.NegatedAtom(self.predicate, paras) for paras in self.paras_set])

	def to_literals(self):
		if self.negated is False:
			return [pddl.Atom(self.predicate, paras) for paras in self.paras_set]
		else:
			return [pddl.NegatedAtom(self.predicate, paras) for paras in self.paras_set]


	def negation(self):
		neg_self = copy.deepcopy(self)
		neg_self.negated = not self.negated
		return neg_self


	def dump(self):
		print("Name: ", self.predicate)
		print("Parameters:")
		for e in self.paras_set:
			print(e)
		print("Negated?: ", self.negated)





class Literal_Partition:



	def __init__(self, literals):

		self.eqc_list = list()
		self.e_parts = set()
		self.ne_parts = set()

		for literal in literals:
			self.add(literal)

	def add(self, literal):

		if literal.predicate == "=" and literal.negated == False:
			self.e_parts.add(tuple(literal.args))
			return
		elif literal.predicate == "=" and literal.negated == True:
			self.ne_parts.add(tuple(literal.args))
			return

		for eqc in self.eqc_list:
			if eqc.is_eq(literal):
				eqc.add(literal)
				return 

		eqc = Literal_EQC(literal)
		self.eqc_list.append(eqc)
		return

	def add_eqc(self, eqc):
		self.eqc_list.append(eqc)

	def add_es(self, es):
		self.e_parts |= set(es)

	def add_nes(self, nes):
		self.ne_parts |= set(nes)

	def add_one_nes(self, nes):
		self.ne_parts.add(nes)

	def is_relevant(self, eqc):

		for m_eqc in self.eqc_list:
			if m_eqc.is_relevant(eqc):
				return True
		return False


	def is_eq(self, eqc):

		for m_eqc in self.eqc_list:
			if m_eqc.is_eq(eqc):
				return True
		return False

	def simplified(self):

		for p1, p2 in self.ne_parts:
			if p1 == p2 or (p1, p2) in self.e_parts or (p2, p1) in self.e_parts:
				return None

		for p1, p2 in copy.copy(self.e_parts):
			if p1 == p2 or (p2, p1) in self.e_parts:
				self.e_parts.remove((p1,p2))
		return self


	def to_condition(self):

		parts = [eqc.to_condition() for eqc in self.eqc_list]
		parts += [pddl.Atom("=", args) for args in self.e_parts]
		parts += [pddl.NegatedAtom("=", args) for args in self.ne_parts]

		return pddl.Conjunction(parts).simplified()


	def to_effects(self):

		literals = sum([eqc.to_literals() for eqc in self.eqc_list], [])

		parts = [pddl.Atom("=", args) for args in self.e_parts]
		parts += [pddl.NegatedAtom("=", args) for args in self.ne_parts]
		condition = pddl.Conjunction(parts).simplified()

		return [pddl.Effect([], condition, literal) for literal in literals ]



	def negation(self):

		neg_self = self.__class__([])
		neg_self.eqc_list = [ eqc.negation() for eqc in self.eqc_list]
		neg_self.e_parts = copy.copy(self.ne_parts)
		neg_self.ne_parts = copy.copy(self.e_parts)

		return neg_self


	def dump(self):
		print("EQCs:")
		for eqc in self.eqc_list:
			eqc.dump()
			print("------")
		print("Es")
		print(self.e_parts)
		print("NEs")
		print(self.ne_parts)

			#elif eqc.is_conflictive(literal):









