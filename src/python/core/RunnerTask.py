import os
import json
import collections

class RunnerTask(object):
	"""docstring for NodeHandler"""
	def __init__(self, tool, mode, project, id, scope,seed, parameters,jvmtest,approach):
		self.tool = tool
		self.mode=mode
		self.project = project
		self.id = id
		self.scope = scope
		self.seed=seed
		self.parameters = parameters
		self.jvmtest=jvmtest
		self.jvmapproach =approach