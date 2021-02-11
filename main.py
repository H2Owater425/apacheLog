import re, os
from datetime import datetime
from pytz import timezone

class ApacheLog:
	def __init__(self, timeZone: str, export: str=None):
		self.timeZone = timeZone
		self.export = export

	def log(self, logLevel: str or int, message: str) -> None:
		'''
		Print or saves apache-formed log

		- logLevel: debug=0 | info=1 | notice=2 | warn=3 | alert=4 | error=5 | crit=6 | emerg=7
		'''

		errorMessage = '"{}" is unsupported {} for "{}"'

		if(str(type(self.timeZone)) != '<class \'str\'>'):
			raise TypeError(errorMessage.format(str(type(self.timeZone)).replace('<class \'', '').replace('\'>', '')), 'type', 'timeZone')

		elif(str(type(logLevel)) != '<class \'str\'>' and str(type(logLevel)) != '<class \'int\'>'):
			raise TypeError(errorMessage.format(str(type(logLevel)).replace('<class \'', '').replace('\'>', '')), 'type', 'logLevel')

		elif(str(type(message)) != '<class \'str\'>'):
			raise TypeError(errorMessage.format(str(type(message)).replace('<class \'', '').replace('\'>', '')), 'type', 'message')

		elif(str(type(self.export)) != '<class \'str\'>' and str(type(self.export)) != '<class \'NoneType\'>'):
			raise TypeError(errorMessage.format(str(type(self.export)).replace('<class \'', '').replace('\'>', '')), 'type', 'export')

		# debug: 0, info: 1, notice: 2, warn: 3, alert: 4, error: 5, crit: 6, emerg: 7
		logLevelNameList = ['debug', 'info', 'notice', 'warn', 'alert', 'error', 'crit', 'emerg']

		if(self.export == '<class \'str\'>'):
			self.export = self.export.replace('\\', '/')

		if(re.match(re.compile('^[+-](?:2[0-3]|[01][0-9]):[0-5][0-9]$'), self.timeZone) == None):
			raise ValueError(errorMessage.format(self.timeZone, 'string', 'timeZone'))

		if(str(type(logLevel)) == '<class \'str\'>'):
			if(not logLevel in logLevelNameList):
				raise ValueError(errorMessage.format(logLevel, 'string', 'logLevel'))

		elif(str(type(logLevel)) == '<class \'int\'>'):
			if(logLevel < 8 and logLevel > -1):
				logLevel = logLevelNameList[logLevel]

			else:
				raise ValueError(errorMessage.format(logLevel, 'integer', 'logLevel'))

		if(self.export != None):
			if(len(self.export.split('/')[:-1]) != 0 and not os.path.exists('/'.join(self.export.split('/')[:-1]))):
				os.mkdir('/'.join(self.export.split('/')[:-1]))

			try:
				logFile = open(self.export, 'a', encoding='utf8')

			except PermissionError:
				raise PermissionError(f'Wrong or have no permission for the file "{self.export}"')

			currentTime = datetime.now(timezone("UTC")).strftime('%d/%b/%Y:%H:%M:%S')

			print(f'[{currentTime} {self.timeZone}][{logLevel}] {message}')

			logFile.write(f'[{currentTime} {self.timeZone}][{logLevel}] {message}\n')
			logFile.close()

		else:
			currentTime = datetime.now(timezone("UTC")).strftime('%d/%b/%Y:%H:%M:%S')

			print(f'[{currentTime} {self.timeZone}][{logLevel}] {message}')

		return None

def log(timeZone: str, logLevel: str or int, message: str, export: str=None) -> None:
	'''
	Print or saves apache-formed log

	- logLevel: debug=0 | info=1 | notice=2 | warn=3 | alert=4 | error=5 | crit=6 | emerg=7
	- export: _PathLike
	'''

	log = ApacheLog(timeZone, export).log

	log(logLevel, message)