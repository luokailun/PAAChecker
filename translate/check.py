




from pddl import conditions
from pddl import pddl_types


def __parse_typed_list(alist, only_variables=False,
                     constructor=pddl_types.TypedObject,
                     default_type="object"):
    result = []
    for element in alist:

        elems = element.split(":")

        if len(elems) == 1:
        	item = elems[0].strip()
        	_type = default_type
        elif len(elems) == 2:
            item = elems[0]
            _type = elems[1].strip()
        else:
        	print("some error occur when __parse_typed_list")

        entry = constructor(item, _type)
        result.append(entry)
    return result


def __check_variables(variables, constants):

	new_variables = list()
	constants = tuple(constants)
	for var in variables:
		var = var.strip()
		if var == "":
			continue
		elif var not in constants and var.find('?') == -1:
			new_variables.append("?%s"%var)
		else:
			new_variables.append(var)
	return new_variables


def check_variables(formula, constants):

	if isinstance(formula, conditions.Literal):
		
		parameters = __check_variables(formula.args, constants)

		return formula.__class__(formula.predicate, parameters)


	elif isinstance(formula, conditions.QuantifiedCondition):

		parameters = __check_variables(formula.parameters, list())
		parameters = __parse_typed_list(parameters)

		return formula.__class__(parameters, [check_variables(part,constants) for part in formula.parts])
		
	elif isinstance(formula, conditions.JunctorCondition):

		return formula.__class__([check_variables(part,constants) for part in formula.parts])

	elif isinstance(formula, conditions.ConstantCondition):

		return formula

	else:
		print('---ERORR: when check_variables')
		exit(0)







