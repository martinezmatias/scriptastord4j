#!/usr/bin/env python

import argparse
from core.projects.LangProject import LangProject
from core.projects.MathProject import MathProject
from core.projects.ChartProject import ChartProject
from core.projects.TimeProject import TimeProject
from core.projects.ClosureProject import ClosureProject
from core.projects.MockitoProject import MockitoProject
from core.Config import conf
from core.tools.Astor import Astor

from core.NodeHandler import NodeHandler
from core.RunnerTask import RunnerTask



def initParser():
	parser = argparse.ArgumentParser(description='Run tools on defect4j with grid5000')
	parser.add_argument('-parameters', help='Parameters')
	parser.add_argument('-projects', nargs='+', required=True, help='Which project (all, math, lang, time)')
	parser.add_argument('-modes', nargs='+', required=True, help='Which execution mode (jgenprog, jkali, etc)')
	parser.add_argument('-id', nargs='+', help='Bug id')
	parser.add_argument('-scope', nargs='+', help='Scope')
	parser.add_argument('-seed',  nargs='+', help='Seed')
	parser.add_argument('--timeout', required=False, help='Node timeout')
	parser.add_argument('--with-angelic', action='store_true', default=False, help='Run only bug with angelic')
	parser.add_argument('-runlocal',  required=False, default=False, help='Indicates if run the script local')
	parser.add_argument('-jvmtest',  required=False,
						help='Path to the JVM used to run tests (must point to the bin folder)')
	parser.add_argument('-jvmapproach', required=False,
						help='Path to the JVM used to run the repair approach (must point to the bin folder)')
	return parser.parse_args()

args = initParser()
print "Arguments %s" % args

projects = []
for project in args.projects:
	if project.lower() == "all":
		projects.append(ChartProject())
		projects.append(LangProject())
		projects.append(MathProject())
		projects.append(TimeProject())
		projects.append(ClosureProject())
	elif project.lower() == "chart":
		projects.append(ChartProject())
	elif project.lower() == "lang":
		projects.append(LangProject())
	elif project.lower() == "math":
		projects.append(MathProject())
	elif project.lower() == "time":
		projects.append(TimeProject())
	elif project.lower() == "closure":
		projects.append(ClosureProject())
	elif project.lower() == "mockito":
		projects.append(MockitoProject())
modes = []
for mode in args.modes:
		modes.append(mode)

tasks = []
scopes = []
if not args.scope:
	scopes = ['local','package','global']
else:
	for s in args.scope:
		scopes.append(s)

parameters=args.parameters


##Configuration:
runlocal=False
jvmtest=None
jvmapproach=None
if args.runlocal is not None:
	runlocalarg = args.runlocal
	print "run local? %s "%runlocalarg
	conf.runlocal=runlocalarg
	runlocal=runlocalarg
if args.jvmtest is not None:
	conf.javaHome=args.jvmtest
	print "Setting jvm %s " % (conf.javaHome)
	jvmtest=args.jvmtest

if args.jvmapproach is not None:
	conf.javaHome8=args.jvmapproach
	print "Setting jvm  8%s " % (conf.javaHome8)
	jvmapproach=args.jvmapproach

print "Configuration %s and %s" % (conf.javaHome, conf.javaHome8)



for project in projects:
	for mode in modes:
		tool=Astor()
		for scope in scopes:
			for seed in args.seed:
				print "seed: %s " % seed
				print "scope in for %s " % scope
				tool.scope = scope
				if args.id:
					for id in args.id:
						task = RunnerTask(tool,mode, project, int(id),scope,seed,parameters, jvmtest, jvmapproach)
						tasks.append(task)
				elif args.with_angelic:
					for i in project.angelicValue:
						task = RunnerTask(tool,mode, project, int(i),scope,seed,parameters, jvmtest, jvmapproach)
						tasks.append(task)
				else:
					for i in range(1, project.nbBugs + 1):
						task = RunnerTask(tool,mode, project, int(i),scope,seed,parameters, jvmtest, jvmapproach)
						tasks.append(task)



nodeHandler = NodeHandler(tasks,runlocal)
nodeHandler.run(args.timeout)
