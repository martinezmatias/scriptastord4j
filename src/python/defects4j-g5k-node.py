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


def initParser():
	parser = argparse.ArgumentParser(description='Run tools on defect4j with grid5000')
	parser.add_argument('-parameters', help='Parameters')
	parser.add_argument('-project', required=True, help='Which project (all, math, lang, time)')
	parser.add_argument('-mode', required=True, help='Execution Mode')
	parser.add_argument('-tool', required=True, help='Which tool (nopol, ranking, ...)')
	parser.add_argument('-id', help='Bug id')
	parser.add_argument('-scope', help='Scope (local, package, global)')
	parser.add_argument('-seed', help='Random Seed')
	parser.add_argument('-jvmtest', required=False,
						help='Path to the JVM used to run tests (must point to the bin folder)')
	parser.add_argument('-jvmapproach', required=False,
						help='Path to the JVM used to run the repair approach (must point to the bin folder)')
	return parser.parse_args()

args = initParser()
print "--> Arguments in Node %s" % args
project = None
tool = None
id = int(args.id)
scope=args.scope
seed=args.seed
mode=args.mode
parameters=args.parameters
if args.project == "Lang":
	project = LangProject()
elif args.project == "Math":
	project = MathProject()
elif args.project == "Chart":
	project = ChartProject()
elif args.project == "Time":
	project = TimeProject()
elif args.project == "Closure":
	project = ClosureProject()
elif args.project == "Mockito":
	project = MockitoProject()



jvmtest=None
jvmapproach=None

if args.jvmtest is not None and not(args.jvmtest == 'None'):
	conf.javaHome=args.jvmtest
	print "node Setting jvm %s " % (conf.javaHome)
	jvmtest=args.jvmtest

if args.jvmapproach is not None and not(args.jvmapproach == 'None'):
	conf.javaHome8=args.jvmapproach
	print "node Setting jvm  8%s " % (conf.javaHome8)
	jvmapproach=args.jvmapproach

print "Configuration %s and %s" % (conf.javaHome, conf.javaHome8)

tool = Astor(mode,scope, seed)
tool.run(project, id,scope,seed,mode,parameters)
