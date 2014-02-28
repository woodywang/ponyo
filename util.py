import subprocess
import datetime
import os
import yaml
import sys
import ponyo

_scriptDir = os.path.dirname(os.path.realpath(__file__))
CONFIG = dict()
with open(os.path.join(_scriptDir, 'config.yml')) as fp:
	CONFIG = yaml.load(fp)



def makeDate(ymd):
	year = int(ymd[0 : 4])
	month = int(ymd[4 : 6])
	day = int(ymd[6 : 8])
	
	return datetime.date(year, month, day)

def hive(hql, outputFile):
	global context
	
	hivePath = context.config['path']['hive']
	
	fout = open(outputFile, 'w')
	subprocess.call('%s -e "%s"' % (hivePath, hql), stdout = fout, shell = True)
	fout.close()
	pass

def readTSV(src, fields = []):
	data = list()
	with open(src, 'r') as fp:
		for line in fp:
			if len(fields) == 0:
				item = line.strip().split('\t')
			else:
				fieldsLength = len(fields)
				itemArray = line.strip().split('\t')[0 : fieldsLength]
				zipped = zip(fields, itemArray)
				item = dict()
				for tp in zipped:
					item[tp[0]] = item[tp[1]]
			data.append(item)
	return data
	pass

def findPrevMonday(aday):
	weekday = aday.weekday()
	return aday - datetime.timedelta(days = weekday)

def findNextSunday(aday):
	weekday = aday.weekday()
	diffdays = 6 - weekday
	return aday + datetime.timedelta(days = diffdays)

def makeEmptyCommentFile(aday):
	global context
	
	firstDayOfWeek = findPrevMonday(aday)
	fileDir = os.path.join(context.rootDir, 'data', firstDayOfWeek.strftime('%Y%m%d'))
	filePath = os.path.join(fileDir, "comments.yml")
	
	if not os.path.exists(fileDir):
		os.makedirs(fileDir)
	
	content = '''all_kpi_comment:

web_kpi_comment:
web_muv_forecast:

ios_kpi_comment:
ios_muv_forecast:

pc_kpi_comment:
pc_muv_forecast:
pc_version_comment:

android_kpi_comment:
android_muv_forecast:
android_version_comment:'''
	
	with open(filePath, 'w') as fp:
		fp.write(content)

def render(data = dict()):
	pass

def sendMail(addresses, subject, body, attachments = dict()):
	pass

class Context(object):
	_instance = None
	
	@staticmethod
	def instance():
		if Context._instance is None:
			Context._instance = Context()
		return Context._instance
	
	def __init__(self):
		self.config = CONFIG
		self.rootDir = os.path.dirname(os.path.realpath(__file__))
		
		aday = makeDate(sys.argv[1])
		self.firstMonday = findPrevMonday(aday) - datetime.timedelta(days = 7)
		self.secondMonday = findPrevMonday(aday)
		self.firstSunday = findNextSunday(aday) - datetime.timedelta(days = 7)
		self.secondSunday = findNextSunday(aday)

context = Context.instance()