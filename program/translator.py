


from . import program
from . import program_parser
from translate import translator
from translate import check
import re


action_pattern = re.compile(r"(?:([\w\-]+)\(?([\w,\?\s]*)\)?)")


def get_action_from_str(action_str, constants):

	action_str = action_str.strip()
	match = action_pattern.match(action_str)
	if match:
		paras = [ para.strip() for para in match.group(2).split(',')]
		paras = check.__check_variables(paras, constants)
		return program.SimpleAction(match.group(1), paras)
	else:
		print("ERROR: cannot handle action str %s : get_action_from_str"%action_str)
		exit(0)


def translate(program_str, fluents, constants):

	keyword, content = program_parser.parse(program_str)

	if keyword == 'non_deterministric':

		program_list = content
		return  program.NondeterministicProgram([translate(sub_program, fluents,  constants) for sub_program in program_list ])

	elif keyword == 'sequential':

		program_list = content
		return  program.SequentailProgram([translate(sub_program, fluents,  constants) for sub_program in program_list ])

	elif keyword == 'parenthesis':
		sub_program = content
		return translate(sub_program, fluents, constants)

	elif keyword == 'pi_action':
		variables, sub_program = content
		new_variables = check.__check_variables(variables, constants)
		new_variables = check.__parse_typed_list(new_variables)
		return program.PiProgram(new_variables, [translate(sub_program, fluents, constants)])

	elif keyword == 'single':
		action = content
		if action.find('?') ==-1:
			return get_action_from_str(action, constants)
		else:
			formula = action.strip().strip('?')
			condition = translator.translate(formula, fluents, constants)
			return program.TestAction(condition)




