import json
import re
import os
import subprocess
import datetime
from core.Tool import Tool
from core.Config import conf
from pprint import pprint

class Astor(Tool):
	"""docstring for Astor"""
	def __init__(self, name="jgenprog",scope="local",seed="1"): ##mm
		super(Astor, self).__init__(name, "astor")
		self.maxExecution = "05:30:00"
		self.scope=scope
		self.seed=seed

	def runAstor(self, 
		project, 
		id,
		scope,
		seed="0",
		mode="jgenprog",
		maxgen="1000000",
		population="1",
		parameters="x:x"):
		print "seed AstorRun %s " % (seed)
		source = None
		for index, src in project.src.iteritems():
			if id <= int(index):
				source = src
				break
		cmdInfo = 'export PATH="' + conf.defects4jRoot + '/framework/bin:$PATH";'
		cmdInfo += 'defects4j info -p ' + project.name + ' -b ' + str(id)
		info = subprocess.check_output(cmdInfo, shell=True)
		workdir = self.initTask(project, id)	

		print "jvms 8 %s" %conf.javaHome8

		#New Astor: 
		classpath = ""
		for index, cp in project.classpath.iteritems():
			if id <= int(index):
				for c in cp.split(":"):
					if classpath != "":
						classpath += ":"
						classpath += os.path.join(workdir, c)
				break
		##
		for lib in project.libs:
			if os.path.exists(os.path.join(workdir, "lib", lib)):
				classpath += ":" + os.path.join(workdir, "lib", lib)
		classpath += ":" + self.jar
		##end new
		# extracts failing test cases
		failingTest = ""
		reg = re.compile('- (.*)::(.*)')
		m = reg.findall(info)
		for i in m:
			failingTest += i[0] + ":"

		cmd = 'cd ' + workdir +  ';'
		cmd += 'export JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8;'
		cmd += 'TZ="America/New_York"; export TZ;'
		cmd += 'export PATH="' + conf.javaHome + ':$PATH";'
		cmd += 'time '+conf.javaHome8+'/java %s -cp %s %s' % (conf.javaArgs, self.jar, self.main)
		cmd += ' -mode ' + self.name 
		cmd += ' -location .'
		cmd += ' -id '+project.name
		cmd += ' -dependencies ' + classpath		
		cmd += ' -failing ' + failingTest
		cmd += ' -package ' + project.package
		cmd += ' -jvm4testexecution ' + conf.javaHome
		cmd += ' -jvm4evosuitetestexecution '+ conf.javaHome8
		cmd += ' -javacompliancelevel ' + str(project.complianceLevel[str(id)]['source'])
		cmd += ' -maxgen ' + maxgen
		cmd += ' -seed ' + seed
		cmd += ' -scope ' + scope
		cmd += ' -population ' + population 
		cmd += ' -srcjavafolder ' + source['srcjava']
		cmd += ' -srctestfolder ' + source['srctest']
		cmd += ' -binjavafolder ' + source['binjava']
		cmd += ' -bintestfolder ' + source['bintest']
		cmd += ' -parameters '+parameters 
		cmd +=  ';'
	
		pathEvo = os.path.join(workdir,"output_astor")#mm
		pathBug = os.path.join(project.logPath,"seed",seed, scope, str(id), self.name)#mm
		path = os.path.join(project.logPath,"seed",seed, scope, str(id), self.name, 'result')#mm
		print path
		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))
		cmd += 'echo "\n\nNode: `hostname`\n";'
		cmd += 'echo "\nDate: `date`\n";'
		cmd += ' find '+pathEvo+' -name "*.class" -type f -delete;'
		cmd += 'echo "removed classes \n";'
		#
		cmd += ' find . -name bin  -type d -print0|xargs -0 rm -r --;'
		#zip
		cmd += ' zip -r -q out.zip '+pathEvo+'; '#mm2
		cmd += 'echo "zipped \n";'
		#copy
		cmd += 'cp out.zip '+ pathBug  +'; ' #mm2
		cmd += 'echo "copied zip \n";'
		#rm
		cmd += 'rm -rf ' + workdir + ';'

		logPath = os.path.join(project.logPath, "seed",seed, scope ,str(id), self.name, "stdout.log.full")
		logFile = file(logPath, 'w')
		print "Running command %s" % cmd
		subprocess.call(cmd, shell=True, stdout=logFile)
		with open(logPath) as data_file:
			log = data_file.read()
			slittedLog = log.split('----SUMMARY_EXECUTION---')
			if(len(slittedLog) > 1):
				print slittedLog[1]
				self.parseLog(slittedLog[1], project, id, scope,seed) ##mm
			else:
				slittedLog = log.split('End Repair Loops:')
				if(len(slittedLog) > 1):
					print slittedLog[1]
					self.parseLog(slittedLog[1], project, id, scope,seed) ##mm
		

	def run(self, 
		project, 
		id,
		scope,
		seed="1",
		mode="jgenprog",
		parameters="x:x"):
		self.runAstor(project, id,scope,seed,mode=mode,parameters=parameters)

	def parseLog(self, log, project, id, scope,seed):
		programVariant = None
		timeEvaluation = None
		timeTotal = None
		date = datetime.datetime.now().isoformat()
		node = self.getHostname()

		m = re.search('ProgramVariant ([0-9]+)', log)
		if m:
			programVariant = m.group(1)
		m = re.search('Time Repair Loop \(s\): ([0-9]+)', log)
		if m:
			timeEvaluation = m.group(1)
		m = re.search('Time Total\(s\): ([0-9]+)', log)
		if m:
			timeTotal = m.group(1)
		else:
			return
		m = re.search('Node: ([a-zA-Z0-9\-\.]+)', log)
		if m:
			node = m.group(1)
		m = re.search('Date: ([^`]+)$', log)
		if m:
			date = m.group(1)

		operations = []

		operationsSplit = log.split('ProgramVariant ')
		if (len(operationsSplit) > 1):
			for op in operationsSplit:
				generation = None
				className = None
				line = None
				lineSusp = None
				patch = None
				buggyStatement = None
				type = None
				variant = 0
				timepatch = 0
				scopepatch = None
				ingrpatch = None
				#
				fvaltcfailing = None
				fvalresult = None
				fvaltcall = None
				#
				#
				mvaltcfailing = None
				mvalresult = None
				mvaltcall = None
				#
				evaltcfailing = None
				evalresult = None
				evaltcall = None
				m = re.search('^([0-9]+)$', op, flags=re.MULTILINE + re.DOTALL)
				if m:
					variant = m.group(1)
				# m = re.search('(REPLACE|DELETE|INSERT_BEFORE|INSERT_AFTER)', op)
				m = re.search('operation: (.*)', op)
				if m:
					type = m.group(1)
				m = re.search('location= (.*)', op)
				if m:
					className = m.group(1)
				else:
					continue
				m = re.search('line= ([0-9]+)', op)
				if m:
					line = m.group(1)
				m = re.search('lineSuspiciousness= ([0-9]+)', op)
				if m:
					lineSusp = m.group(1)
				m = re.search('^original statement= "?(.*)"?\nbuggy kind', op, flags=re.MULTILINE + re.DOTALL)
				if m:
					buggyStatement = m.group(1)
				m = re.search('^fixed statement= "?(.*)"?\nPatch kind', op, flags=re.MULTILINE + re.DOTALL)
				if m:
					patch = m.group(1)
				if type == "RemoveOp":
					patch = 'remove'
				m = re.search('generation= ([0-9]+)', op)
				if m:
					generation = m.group(1)
				m = re.search('time\(sec\)= ([0-9]+)', op)
				if m:
					timepatch = m.group(1)
				m = re.search('ingredientScope= (.*)', op)
				if m:
					scopepatch = m.group(1)
				m = re.search('ingredients= (.*)', op)
				if m:
					ingrpatch = m.group(1)
				# new
				m = re.search('failing: (.*)', op)
				if m:
					sl = m.group(1).split("|")
					fvaltcfailing = sl[2]
					fvalresult = sl[1]
					fvaltcall = sl[3]
				#
				# new
				m = re.search('manual_regression: (.*)', op)
				if m:
					sl = m.group(1).split("|")
					mvaltcfailing = sl[2]
					mvalresult = sl[1]
					mvaltcall = sl[3]
				#
				m = re.search('evo_regression: (.*)', op)
				if m:
					sl = m.group(1).split("|")
					evaltcfailing = sl[2]
					evalresult = sl[1]
					evaltcall = sl[3]
				#
				# if(patch == None):
				#	continue

				operations.append({
					'type': type,
					'generation': int(generation),
					'variant': int(variant),
					'patchLocation': {
						'className': className,
						'line': int(line),
						'lineSusp': lineSusp

					},
					'patch': patch,
					'buggyStatement': buggyStatement,
					'time': timepatch,
					'scope': scopepatch,
					'ingredients': ingrpatch,
					'patchvalidation': {
						'fvaltcfailing': fvaltcfailing,
						'fvalresult': fvalresult,
						'fvaltcall': fvaltcall,
						#
						'mvaltcfailing': mvaltcfailing,
						'mvalresult': mvalresult,
						'mvaltcall': mvaltcall,
						#
						'evaltcfailing': evaltcfailing,
						'evalresult': evalresult,
						'evaltcall': evaltcall
					},
				})
		results = {
			'programVariant': programVariant,
			'operations': operations,
			'timeEvaluation': timeEvaluation,
			'timeEvaluation': timeEvaluation,
			'timeTotal': timeTotal,
			'node': node,
			'date': date
		}
		reg = re.compile('#([a-zA-Z]+) *: *([0-9]+)')
		m = reg.findall(log)
		for i in m:
			results[i[0]] = i[1]
		reg = re.compile("time val([0-9]+) \[[0-9]+\]: \[([0-9, ]+)\]")
		m = reg.findall(log)
		for i in m:
			results["timeVal" + i[0]] = []
			t = re.compile('([0-9]+)')
			v = t.findall(i[1])
			for j in v:
				results["timeVal" + i[0]].append(int(j))
			

		path = os.path.join(project.logPath, "seed",seed ,scope, str(id), self.name, "results.json")#scope
		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))
		file = open(path, "w")
		file.write(json.dumps(results, indent=4, sort_keys=True))
		file.close()
