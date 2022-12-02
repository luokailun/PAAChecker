


from literal import literal
import itertools


# lp1 is a subset of lp2

def __simplified(lp_list):

	return [lp for lp in lp_list if lp is not None]


################################################################################################



def __interpret_lp(pre_lp):

	lp = literal.Literal_Partition(list())	

	for elem in pre_lp:
		if isinstance(elem, literal.Literal_EQC):
			lp.add_eqc(elem)
		elif isinstance(elem, list):
			for m in elem:
				if isinstance(m, literal.Literal_EQC):
					lp.add_eqc(m)
				else:
					assert isinstance(m, tuple)
					sym, p1, p2 = m
					if sym == "!=":
						lp.add_nes([(p1,p2)])
					else:
						assert sym == "="
						lp.add_es([(p1,p2)])
		else:
			assert isinstance(elem, tuple)
			sym, p1, p2 = elem
			if sym == "!=":
				lp.add_nes([(p1,p2)])
			else:
				assert sym == "="
				lp.add_es([(p1,p2)])

	return lp



def __interpret(lp1, lp2, pre_lp_list):

	lp_list = list()
	for pre_lp in itertools.product(*pre_lp_list):

		lp = __interpret_lp(pre_lp)

		## we really need to add lp2's equal predicates and un-equal predicates ??
		lp.add_es(lp1.e_parts)
		#lp.add_es(lp2.e_parts)
		lp.add_nes(lp1.ne_parts)
		#lp.add_nes(lp2.ne_parts)

		lp = lp.simplified()
		if lp is not None:
			lp_list.append(lp)

	return lp_list


################################################################################################

def __add_paras_product_neq(eqc1, eqc2, mlist):

	paras_set1 = eqc1.paras_set
	paras_set2 = eqc2.paras_set

	#assert len(paras_set1) == len(paras_set2
	for paras1, paras2 in itertools.product(paras_set1, paras_set2):
		mlist.append([ ("!=", p1, p2) for p1, p2 in zip(paras1, paras2)])




def __add_neq_constraint(lp1, lp2, pre_lp_list):

	for eqc1 in lp1.eqc_list:
		for eqc2 in lp2.eqc_list:
			if eqc1.is_conflictive(eqc2):
				__add_paras_product_neq(eqc1, eqc2, pre_lp_list)
				break


################################################################################################

# def __paras_product_not_or(eqc1, eqc2):
# 	paras_set1 = eqc1.paras_set
# 	paras_set2 = eqc2.paras_set

# 	#assert len(paras_set1) == len(paras_set2

# 	nes_list = list()
# 	for para1, para2 in itertools.product(paras_set1, paras_set2):
# 		nes_list.append(tuple(zip(para1, para2),))

# 	return nes_list






def __add_minus(eqc1, eqc2, mlist):

	paras_set1 = eqc1.paras_set
	paras_set2 = eqc2.paras_set

	## no paras eqc
	if len(paras_set1) == 0:
		assert len(paras_set2) == 0
		return mlist

	choice_list = [[eqc1]]
	for paras2 in paras_set2:
		# recursively
		new_choice_list = list()
		for choice in choice_list:

			# each choice has the form: [(EQC), =/!=,... =/!=]
			if isinstance(choice[0], literal.Literal_EQC):
				eqc = choice[0]
			else:
				new_choice_list.append(choice)
				continue

			#### minus a literal: two possible operation
			#1 move a parameter from EQC
			for paras1 in eqc.paras_set:
				con_list = list()
				eqc_new = eqc.remove_paras(paras1)
				if eqc_new is not None:
					con_list.append(eqc_new)
				con_list += [ ("=", p1, p2) for p1, p2 in zip(paras1, paras2)]

				con_list += choice[1:]
				new_choice_list.append(con_list)

			#2 move no parameter from EQC
			pre_list = list()
			############ not equal to  any literal (at least one para of a literal is different) in eqc,
			for paras1 in eqc.paras_set:
				pre_list.append([ ("!=", p1, p2) for p1, p2 in zip(paras1, paras2)])

			for d in itertools.product(*pre_list):
				con_list = [eqc]+list(d) + choice[1:]
				new_choice_list.append(con_list)

		#for c in new_choice_list:


		choice_list = new_choice_list		
		# print("cccccccccc")
		# print(choice_list)
		# print("cccccccccc")
	mlist.append(choice_list)
			


def __minus(lp1, lp2):

	pre_lp_list = list()
	for eqc1 in lp1.eqc_list:
		in_flag = False
		for eqc2 in lp2.eqc_list:
			if eqc1.is_eq(eqc2):
				# print("EQEQEQ----")
				# eqc1.dump()
				# eqc2.dump()
				# print("EQEQEQ----")
				in_flag = True
				__add_minus(eqc1, eqc2, pre_lp_list)
				break
		if in_flag is False:
			pre_lp_list.append([eqc1])
	return pre_lp_list


################################################################################################

def minus(lp1, lp2):

	pre_lp_list = __minus(lp1, lp2)
	lp_list =  __interpret(lp1, lp2, pre_lp_list)

	return __simplified(lp_list)


################################################################################################

def cir_minus(lp1, lp2):
	# return a list of literal_partitions
	pre_lp_list = list()

	__add_neq_constraint(lp1, lp2, pre_lp_list)
	pre_lp_list += __minus(lp1, lp2)

	lp_list =  __interpret(lp1, lp2, pre_lp_list)
	return __simplified(lp_list)


################################################################################################


def __add_uplus(eqc1, eqc2, mlist):

	new_eqc = eqc1.add_EQC(eqc2)
	mlist.append([new_eqc])


def __plus(lp1, lp2):

	pre_lp_list = list()

	eq_list = list()
	for eqc1 in lp1.eqc_list:
		is_eq = False
		for eqc2 in lp2.eqc_list:
			if eqc1.is_eq(eqc2):
				is_eq = True
				eq_list.append(eqc2)
				__add_uplus(eqc1, eqc2, pre_lp_list)
				break

		if is_eq is False:
			pre_lp_list.append([eqc1])

	for eqc2 in lp2.eqc_list:
		if eqc2 not in eq_list:
			pre_lp_list.append([eqc2])

	return pre_lp_list


################################################################################################

def plus(lp1, lp2):

	pre_lp_list = __plus(lp1, lp2)
	lp_list =  __interpret(lp1, lp2, pre_lp_list)

	return __simplified(lp_list)


################################################################################################


def uplus(lp1, lp2):
	
	pre_lp_list = list()

	__add_neq_constraint(lp1, lp2, pre_lp_list) 
	pre_lp_list += __plus(lp1, lp2)

	lp_list =  __interpret(lp1, lp2, pre_lp_list)
	return __simplified(lp_list)




