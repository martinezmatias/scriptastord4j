#!/usr/bin/env python

import argparse
from core.projects.LangProject import LangProject
from core.projects.MathProject import MathProject
from core.projects.ChartProject import ChartProject
from core.projects.TimeProject import TimeProject
from core.projects.ClosureProject import ClosureProject
from core.projects.MockitoProject import MockitoProject


from core.tools.Ranking import Ranking
from core.tools.NopolPC import NopolPC
from core.tools.NopolC import NopolC
from core.tools.BrutpolPC import BrutpolPC
from core.tools.BrutpolC import BrutpolC
from core.tools.Astor import Astor
from core.tools.Kali import Kali

from core.NodeHandler import NodeHandler
from core.RunnerTask import RunnerTask



def initParser():
    parser = argparse.ArgumentParser(description='Run tools on defect4j with grid5000')
    parser.add_argument('-parameters', help='Parameters')
    parser.add_argument('-project', required=True, help='Which project (all, math, lang, time)')
    parser.add_argument('-mode', required=True, help='Execution Mode')
    parser.add_argument('-tool', required=True, help='Which tool (nopol, ranking, ...)')
    parser.add_argument('-id', help='Bug id')
    parser.add_argument('-scope', help='Scope (local, package, global)')
    parser.add_argument('-seed', help='Random Seed')
    return parser.parse_args()

args = initParser()
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


tool = Astor()


tool.run(project, id,scope,seed,mode,parameters)