


from literal import literal
from literal import literal_operation

import pddl


# p1 = pddl.Atom("holding", ['?top'])
# p2 = pddl.Atom("clear", ['?bottom'])
# p3 = pddl.NegatedAtom("clear", ['?b'])
# p4 = pddl.Atom("holding",['?b'])

# lp1 = literal.Literal_Partition([p1, p2])
# lp2 = literal.Literal_Partition([p3, p4])

# lp1.dump()
# print()
# lp2.dump()
# print()

# results = literal_operation.cir_minus(lp1, lp2)

# print("@###------result\n")
# for lp in results:
# 	lp.dump()
# 	print("======\n\n")


print("\n\n\n==========================================\n\n\n")

p1 = pddl.Atom("clear", ['x'])
p2 = pddl.Atom("clear", ['y'])
p3 = pddl.Atom("clear", ['x'])
p4 = pddl.Atom("clear",['y'])

lp1 = literal.Literal_Partition([p1, p2])
lp2 = literal.Literal_Partition([p3, p4])

lp1.dump()
print()
lp2.dump()
print()

results = literal_operation.cir_minus(lp1, lp2)

print("@###------result\n")
for lp in results:
	lp.dump()
	print("======\n\n")