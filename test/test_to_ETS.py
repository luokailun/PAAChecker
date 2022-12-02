



from mapping import to_mapping
from program import normalize
from ets.to_ETS import get_ETS
from ets import ETS_checker


import itertools
import copy




if __name__ == "__main__":

	from pddl_parser import open
	
	mytask = open("./input/block/block.pddl", "./input/block/problem_010.pddl")
	#mytask = open("./input/childsnack/domain.pddl", "./input/childsnack/p03.hddl")
	#mytask = open("./input/Robot/domain.pddl", "./input/Robot/pfile_02_001.hddl")
	#mytask = open("./input/Robot/domain.pddl", "./input/Robot/pfile_03_005.hddl") # success for 4.m
	#mytask = open("./input/Robot/domain.pddl", "./input/Robot/pfile_04_005.hddl") # success for 5.m
	#mytask = open("./input/Robot/domain.pddl", "./input/Robot/pfile_10_020.hddl") # success for 5.m
	#mytask = open("./input/Robot/domain.pddl", "./input/Robot/pfile_05_010.hddl") # success for 4.m

	fluent_names = [pred.name for pred in mytask.predicates]
	constants = [o.name for o in mytask.objects]
	#mapping = to_mapping.load_mapping_from_file('./input/block/7.m', fluent_names, constants)
	mapping = to_mapping.load_mapping_from_file('./input/block/7_2.m', fluent_names, constants)
	#mapping = to_mapping.load_mapping_from_file('./input/childsnack/14test.m', fluent_names, constants)
	#mapping = to_mapping.load_mapping_from_file('./input/childsnack/14.m', fluent_names, constants)
	#mapping = to_mapping.load_mapping_from_file('./input/Robot/5.m', fluent_names, constants)

	# for f in mapping.fluent_maps:
	# 	f.dump()
	# exit(0)

	# for a in mytask.actions:
	# 	a.dump()
	# exit(0)

	ets = get_ETS(mytask, mapping)

	#results = ETS_checker.check_DTM(ets)
	#print("aaaa")
	results = ETS_checker.check_SC(ets)
	# print("bbbbb")
	print(results)

	for num, result in ETS_checker.interpret_result(results):
		if result.strip() == "FALSE":
			print(num)
			print("FAILS")
			exit(0)

	print("SUCCESS")

