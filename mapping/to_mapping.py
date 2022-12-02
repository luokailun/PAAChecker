



from . import mapping 
from pddl import pddl_types
from program import translator as program_translator
from translate import translator as formula_translator
from translate import check
import re
import json


pattern = re.compile(r"(?:([\w\-]+)\(?([\w,\:\-\?\s]*)\)?)")






def get_name_paras_from_str(the_str, constants):

	the_str = the_str.strip()
	match = pattern.match(the_str)
	if match:
		paras = [ para.strip() for para in match.group(2).split(',')]
		paras = check.__check_variables(paras, constants)
		paras = check.__parse_typed_list(paras)
		return match.group(1), paras
	else:
		print("ERROR: cannot handle action str %s : get_name_paras_from_str"%the_str)
		exit(0)



def load_mapping_from_file(filename, fluent_names, constants):

	json_dict = json.loads("".join(open(filename).readlines()))

	fluent_maps = list()
	action_maps = list()

	for fluent in json_dict['fluent'].keys():
		fluent_name, paras = get_name_paras_from_str(fluent, constants)
		condition = formula_translator.translate(json_dict['fluent'][fluent], fluent_names, constants)

		fluent_map = mapping.FluentMap(fluent_name, paras, condition)
		fluent_maps.append(fluent_map)

	for action in json_dict['action'].keys():
		action_name, paras = get_name_paras_from_str(action, constants)
		program = program_translator.translate(json_dict['action'][action], fluent_names, constants)

		action_map = mapping.ActionMap(action_name, paras, program)
		action_maps.append(action_map)

	m = mapping.Mapping(fluent_maps, action_maps)
	m.uniquify_variables()

	return m




