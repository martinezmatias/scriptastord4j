import os
from os.path import expanduser

class Config(object):
	"""Runner configurations"""
	def __init__(self):
		defects4jRepairRoot = os.path.join(os.path.dirname(__file__),'../../../' )

		self.defects4jRepairRoot = defects4jRepairRoot
		self.projectsRoot = expanduser("~/projects")
		self.defects4jRoot = expanduser("~/d4j8/defects4j/")
		self.resultsRoot = os.path.join(defects4jRepairRoot, "results/")
		self.z3Root = os.path.join(defects4jRepairRoot, "libs", "z3")
		self.javaHome = expanduser("/home/mmartinez/jdk1.8.0_45/bin/")
		self.javaHome8 = expanduser("/home/mmartinez/jdk1.8.0_45/bin/")
		self.javaArgs = "-Xmx8096m"
		self.runlocal=False

conf = Config()
