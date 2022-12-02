

import os
import re
import subprocess



################################################################################################################################################

result_string = r"Formula number (\d+):.+?, is (.+?) in the model"
result_pattern = re.compile(result_string)

def interpret_result(result):
	results = result_pattern.findall(' '.join(result))
	if results is None:
		print('ERROR')
		exit(0)
	else:
		# for num, result in results:
		# 	print(num, result)
		return results

		




################################################################################################################################################


def check_SC(ETS):

	with open("./mcmas/ets.ispl","w") as input_file:
		print("---Translating to MCMAS....")
		ispl_input_str = ETS.to_ispl("sc")
		print("---Writing to File....")
		input_file.writelines(ispl_input_str)
		input_file.close()
		#cmd = "./mcmas/mcmas -c 1 -l 1 -f 1 ./mcmas/ets.ispl"
		print("Calling MCMAS....")
		cmd = "./mcmas/mcmas -c 2 ./mcmas/ets.ispl"
		
		child = subprocess.Popen(cmd, stdout= subprocess.PIPE, shell=True)
		try:
			k = child.wait(3600)
			return child.stdout.readlines()
		except Exception as e:
			print("TIMEOUT")
			child.kill()
			return None


def check_DTM(ETS):

	with open("./mcmas/ets.ispl","w") as input_file:
		input_file.writelines(ETS.to_ispl("dtm"))
		input_file.close()
		print("Calling MCMAS....")
		#cmd = "./mcmas/mcmas -c 1 -l 1 -f 1 ./mcmas/ets.ispl"
		cmd = "./mcmas/mcmas -c 2 ./mcmas/ets.ispl"
		return os.popen(cmd).readlines()



def check_SC_and_DTM(ETS):

	with open("./mcmas/ets.ispl","w") as input_file:
		input_file.writelines(ETS.to_ispl("sc_dtm"))
		input_file.close()
		print("Calling MCMAS....")
		#cmd = "./mcmas/mcmas -c 1 -l 1 -f 1 ./mcmas/ets.ispl"
		cmd = "./mcmas/mcmas -c 2 ./mcmas/ets.ispl"

		child = subprocess.Popen(cmd, stdout= subprocess.PIPE, shell=True)
		try:
			k = child.wait(3600)
			return child.stdout.readlines()
		except Exception as e:
			print("TIMEOUT")
			child.kill()
			return None
			#print(k)
		
		#os.popen(cmd).readlines()




################################################################################################################################################


