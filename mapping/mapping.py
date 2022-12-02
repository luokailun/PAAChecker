


import json


class FluentMap:

	def __init__(self, fluent_name, parameters, condition):

		self.fluent_name = fluent_name
		self.parameters = parameters
		self.condition = condition

	def dump(self):
		print("# High-level fluent %s(%s)"%(self.fluent_name, ",".join(map(str,self.parameters))))
		print("# Low-level formula:")
		self.condition.dump()
		print('')

	def uniquify_variables(self, type_map = {}):
		self.type_map = type_map
		self.type_map.update({arg.name: arg.type_name for arg in self.parameters})
		self.condition = self.condition.uniquify_variables(self.type_map)


class ActionMap:

	def __init__(self, action_name, parameters, program):
		
		self.action_name = action_name
		self.parameters = parameters
		self.program = program

	def dump(self):
		print("# High-level action: %s(%s)"%(self.action_name, ",".join(map(str,self.parameters))))
		print("# Low-level program:")
		self.program.dump()
		print('')

	def uniquify_variables(self, type_map = {}):
		self.type_map = type_map
		self.type_map.update({arg.name: arg.type_name for arg in self.parameters})
		self.program = self.program.uniquify_variables(self.type_map)


class Mapping:

    def __init__(self, fluent_maps, action_maps):

    	self.fluent_maps = fluent_maps
    	self.action_maps = action_maps

    def dump(self):
    	print("------Fluent Mapping------")
    	for fluent_map in self.fluent_maps:
    		fluent_map.dump()
    	print('\n')	
    	print("------Action Mapping------")
    	for action_map in self.action_maps:
    		action_map.dump()

    def uniquify_variables(self):

    	for fluent_map in self.fluent_maps:
    		fluent_map.uniquify_variables()

    	for action_map in self.action_maps:
    		action_map.uniquify_variables()




#####################################################################################################################










