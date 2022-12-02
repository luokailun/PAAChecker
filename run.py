

from mapping import to_mapping
from program import normalize
from ets.to_ETS import get_ETS
from ets import ETS_checker


import itertools
import copy

import os
import sys
import time
import re
import signal

#
class TimeoutError(Exception):
    def __init__(self):
        super(TimeoutError, self).__init__()


def time_out(interval, callback):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError()

        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)       # interval 
                result = func(*args, **kwargs)
                signal.alarm(0)              # 
                return result
            except TimeoutError:
                callback()
        return wrapper
    return decorator


def timeout_callback():
	print("!!!!TIME----OUT")
	return None




@time_out(3600, timeout_callback)
def run_ABSChecker(mytask, mapping):


	start =time.time()

	ets = get_ETS(mytask, mapping)
	result = ETS_checker.check_SC(ets)

	if result is None:    # if model checking is timing out
		return result

	end = time.time()
	#print('Running time: %s Seconds'%(end-start))
	return end-start, result


num_formula_pattern = re.compile(r"(\d+)\s+formulae\s+successfully\s+read\s+and\s+checked", re.S)
time_pattern = re.compile(r"execution\s+time\s+=\s+([\d\.]+)", re.S)
num_state_pattern = re.compile(r"number\s+of\s+reachable\s+states\s+=\s+([\d\.\+e]+)", re.S)
num_true_pattern = re.compile(r"\bTRUE\b", re.S)
num_false_pattern = re.compile(r"\bFALSE\b", re.S)


def collect_data(result_str):

	match1 = num_formula_pattern.search(result_str)
	if match1:
		num_formula = match1.group(1)
	else:
		return None

	match2 = time_pattern.search(result_str)
	if match2:
		time = match2.group(1)
	else:
		return None

	match3 = num_state_pattern.search(result_str)
	if match3:
		num_state = match3.group(1)
	else:
		return None

	num_true = len(num_true_pattern.findall(result_str))
	num_false = len(num_false_pattern.findall(result_str))


	assert int(num_formula) == num_true+num_false

	return num_formula, str(num_true), str(num_false), time, num_state
		


if __name__ == "__main__":


	run_dir =  os.getcwd()
	input_dir = run_dir+"/input"
	domains = [  dir_name for dir_name in os.listdir(input_dir) if dir_name.find(".")!=0]
	#domains = ["childsnack"]

	domains.sort()


	record_file = open(run_dir+"/result.txt", 'w')
	records = "case  total_time  n_formula  n_true  n_false  ctime  n_state\n"
	record_file.write(records)
	record_file.close()

	import pddl_parser

	for domain_name in domains:
		print("#" * 10, "Parsing domain [%s]"%domain_name)
		domain_dir = input_dir+"/"+domain_name
		
		file_domain = domain_dir+"/domain.pddl"
		problem_dir = domain_dir+ "/problem"
		mapping_dir = domain_dir+ "/mapping"

		for m_name in os.listdir(mapping_dir):
			if m_name.find(".") == 0:
				continue
			print("#" * 15, "handling mapping [%s]"%m_name)

			file_mapping = mapping_dir+ "/" +m_name

			problem_list = os.listdir(problem_dir)
			problem_list.sort()

			for e, problem_name in enumerate(problem_list):
				if problem_name.find(".") == 0:
					continue
				print("#" * 20,  "handling probem [%s]"%problem_name)
				file_problem = problem_dir + "/" + problem_name

				mytask = pddl_parser.open(file_domain, file_problem)

				fluent_names = [pred.name for pred in mytask.predicates]
				constants = [o.name for o in mytask.objects]

				mapping = to_mapping.load_mapping_from_file(file_mapping, fluent_names, constants)

				results = run_ABSChecker(mytask, mapping)

				version_str = "%s|%s|%s"%(domain_name, m_name, problem_name)

				if results is None:
					records = "%s ----- Time Out -----\n"%(version_str)
				else:
					total_time, result_list = results
					datas = collect_data(" ".join([r.decode("utf-8")  for r in result_list]))
					if datas is None:
						records = "%s ----- ERROR -----\n"%(version_str)
					else:
						#num_formula, num_true, num_false, time, num_state
						records = "%s  %s  %s\n"%(version_str, total_time, "  ".join(datas))

				record_file = open(run_dir+"/result.txt", 'a')
				record_file.write(records)
				record_file.close()

		print("\n\n\n\n")

	#record_file.close()

		#### pre_handle
		# import re
		# mpattern = re.compile(r"\(:htn.*?\(:init", re.S)
		# files = os.listdir(domain_dir)
		# for f in files:
		# 	f_name, f_type = os.path.splitext(f)
		# 	if f_type == ".hddl":
		# 		f = open(domain_dir+"/"+f, "r")
		# 		text = "".join(f.readlines())
		# 		new_text = mpattern.sub("(:init", text)
		# 		new_f = open(domain_dir+"/problem/"+f_name+".pddl", "w")
		# 		new_f.write(new_text)
		# 		new_f.close()
	



		#exit(0)
		













