
from mapping import to_mapping
from program import normalize





if __name__ == "__main__":

	from pddl_parser import open
	mytask = open("./input/block.pddl", "./input/problem_005.pddl")

	fluent_names = [pred.name for pred in mytask.predicates]


	m = to_mapping.load_mapping_from_file('./input/1.m', fluent_names, list())
	m.dump()
	print("#################\n\n")

	for e, action_map in enumerate(m.action_maps):
		#if e == len(m.action_maps)-1:
			program = normalize.build_DNF_program(action_map.program)
			# program.dump()
			# program = program.simplified()
			program.dump()
			print("------\n\n")

	# mbat = pddl_to_bat.pddl_to_BAT(mytask)


	# tranSym = to_tranSystem.get_tranSystem(mytask, m, mbat)
	# invariants = tranSym.runPDR()

	# print("find invariants!")
	# print(invariants)



