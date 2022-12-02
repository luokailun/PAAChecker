


import pddl
from literal import literal
from literal import literal_operation


l1 = pddl.Atom("hello", ['x', 'y'])
k = literal.Literal_EQC(l1)
k.dump()


print()
print(k.is_eq(pddl.Atom("hello2", ['x', 'y1'])))
print(k.is_eq(pddl.NegatedAtom("hello", ['x', 'y1'])))
print(k.is_eq(pddl.Atom("hello", ['x', 'y1'])))
print()
print(k.is_conflictive(pddl.NegatedAtom("hello", ['x', 'y2'])))
print(k.is_conflictive(pddl.NegatedAtom("hello1", ['x', 'y1'])))
print(k.is_conflictive(pddl.Atom("hello", ['x', 'y1'])))
print()
print(k.is_relevant(pddl.Atom("hello", ['x', 'y1'])))
print(k.is_relevant(pddl.NegatedAtom("hello", ['x', 'y1'])))
print(k.is_relevant(pddl.Atom("hello2", ['x', 'y1'])))
print()

k2 = literal.Literal_EQC(pddl.Atom("hello2", ['x', 'y1']))
k2.add(pddl.Atom("hello2", ['x1', 'y1']))
k2.dump()

k3 = literal.Literal_EQC(pddl.Atom("hello", ['x', 'y1']))
k3.add(pddl.Atom("hello", ['x1', 'y1']))

k4 = literal.Literal_EQC(pddl.NegatedAtom("hello", ['x', 'y1']))


print(k.is_relevant(k2))
print(k.is_relevant(k3))
print(k.is_relevant(k4))
print()
print(k.is_eq(k2))
print(k.is_eq(k3))
print(k.is_eq(k4))

print("\n\n\n----------------------------\n\n\n")

l1 = pddl.Atom("hello3", ['x', 'y1'])
l2 = pddl.NegatedAtom("hello", ['x', 'y1'])
l4 = pddl.NegatedAtom("hello", ['x', 'y2'])
l3 = pddl.Atom("hello", ['x', 'y1'])
l5 = pddl.NegatedAtom("=", ['x', 'y2'])
l6 = pddl.NegatedAtom("=", ['x1', 'y2'])
l7 = pddl.Atom("=", ['x', 'y2'])
l8 = pddl.Atom("=", ['x', 'y2'])


lp = literal.Literal_Partition([l1,l2,l4,l3, l5, l6, l7, l8])

#lp.dump()



print("\n\n\n----------------------------\n\n\n")


lp2 = literal.Literal_Partition([l1,l4,l3, l5, l6, l7, l8])

lp3 = literal.Literal_Partition([pddl.NegatedAtom("hello", ['x2', 'y3'])])


# print(literal_operation.is_subset(lp2, lp))
# print(literal_operation.is_subset(lp, lp2))
# print(literal_operation.is_subset(lp, lp3))
# print(literal_operation.is_subset(lp3, lp))


print("\n\n\n----------------------------\n\n\n")

for k in literal_operation.cir_minus(lp, lp3):
	k.dump()
	print("\n\n")

print("\n\n\n----------------------------\n\n\n")


for k in literal_operation.uplus(lp, lp3):
	k.dump()
	print("\n\n")

#print(literal_operation.is_subset())

