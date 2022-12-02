



def negate(lset):
	# print("inputinput----")
	# print(lset)
	# print("inputinput----")
	return {l.negate() for l in lset}



def cir_minus(lset1, lset2):

	if negate(lset1).isdisjoint(lset2):
		return lset1 - lset2
	else:
		return None


def uplus(lset1, lset2):
	
	if negate(lset1).isdisjoint(lset2):
		return lset1 | lset2
	else:
		return None