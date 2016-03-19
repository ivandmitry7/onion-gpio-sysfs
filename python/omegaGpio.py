import sys


__version__ = "0.1"


_EXIT_SUCCESS			= 0
_EXIT_FAILURE			= -1


GPIO_BASE_PATH 			= '/sys/class/gpio'
GPIO_EXPORT 			= GPIO_BASE_PATH + '/export'
GPIO_UNEXPORT 			= GPIO_BASE_PATH + '/unexport'
	
GPIO_PATH 				= GPIO_BASE_PATH + '/gpio%d'
GPIO_VALUE_FILE			= 'value'
GPIO_DIRECTION_FILE		= 'direction'
GPIO_ACTIVE_LOW_FILE	= 'active_low'

_GPIO_INPUT_DIRECTION	= 'in'
_GPIO_OUTPUT_DIRECTION	= 'out'

_GPIO_ACTIVE_HIGH		= 0
_GPIO_ACTIVE_LOW		= 1


class OmegaGpio:
	"""Base class for sysfs GPIO access"""

	def __init__(self, gpio):
		self.gpio 		= gpio
		self.path 		= GPIO_PATH%(self.gpio)

		#print 'GPIO%d path: %s'%(self.gpio, self.path)
		

	def _initGpio(self):
		"""Write to the gpio export to make the gpio available in sysfs"""
		with open(GPIO_EXPORT, 'w') as fd:
			fd.write(str(self.gpio))
			fd.close()
			return _EXIT_SUCCESS

		return _EXIT_FAILURE

	def _freeGpio(self):
		"""Write to the gpio unexport to release the gpio sysfs instance"""
		with open(GPIO_UNEXPORT, 'w') as fd:
			fd.write(str(self.gpio))
			fd.close()
			return _EXIT_SUCCESS

		return _EXIT_FAILURE

	# value functions
	def getValue(self):
		"""Read current GPIO value"""
		# generate the gpio sysfs instance
		status 	= self._initGpio()

		if status == _EXIT_SUCCESS:
			gpioFile 	= self.path + "/" + GPIO_VALUE_FILE
			value 		= 0

			with open(gpioFile, 'r') as fd:
				value 	= fd.read()
				fd.close()

			# release the gpio sysfs instance
			status 	= self._freeGpio()

			return value

		return _EXIT_FAILURE

	def setValue(self, value):
		"""Set the desired GPIO value"""
		ret = _EXIT_FAILURE
		# generate the gpio sysfs instance
		status 	= self._initGpio()

		if status == _EXIT_SUCCESS:
			gpioFile 	= self.path + "/" + GPIO_VALUE_FILE

			with open(gpioFile, 'w') as fd:
				fd.write(str(value))
				fd.close()
				ret = _EXIT_SUCCESS
				
			# release the gpio sysfs instance
			status 	= self._freeGpio()

			return ret

		return _EXIT_FAILURE

	# direction functions
	def getDirection(self):
		"""Read current GPIO direction"""
		# generate the gpio sysfs instance
		status 	= self._initGpio()

		if status == _EXIT_SUCCESS:
			gpioFile 	= self.path + "/" + GPIO_DIRECTION_FILE
			direction	= _EXIT_FAILURE

			with open(gpioFile, 'r') as fd:
				direction 	= fd.read()
				fd.close()

			# release the gpio sysfs instance
			status 	= self._freeGpio()

			return direction

		return _EXIT_FAILURE

	def _setDirection(self, direction):
		"""Set the desired GPIO direction"""
		ret = _EXIT_FAILURE
		# generate the gpio sysfs instance
		status 	= self._initGpio()

		if status == _EXIT_SUCCESS:
			gpioFile 	= self.path + "/" + GPIO_DIRECTION_FILE

			if direction == _GPIO_INPUT_DIRECTION or direction == _GPIO_OUTPUT_DIRECTION:
				with open(gpioFile, 'w') as fd:
					fd.write(direction)
					fd.close()
					ret = _EXIT_SUCCESS

			# release the gpio sysfs instance
			status 	= self._freeGpio()

			return ret

		return _EXIT_FAILURE

	def setInputDirection(self):
		ret 	= self._setDirection(_GPIO_INPUT_DIRECTION)
		return 	ret

	def setOutputDirection(self):
		ret 	= self._setDirection(_GPIO_OUTPUT_DIRECTION)
		return 	ret

	# active-low functions
	def getActiveLow(self):
		"""Read if current GPIO is active-low"""
		# generate the gpio sysfs instance
		status 	= self._initGpio()

		if status == _EXIT_SUCCESS:
			gpioFile 	= self.path + "/" + GPIO_ACTIVE_LOW_FILE
			activeLow	= _EXIT_FAILURE

			with open(gpioFile, 'r') as fd:
				print 'Reading %s file'%(gpioFile),
				activeLow 	= fd.read()
				print ' ... Read %s'%(activeLow)
				fd.close()

			# release the gpio sysfs instance
			status 	= self._freeGpio()

			return activeLow

		return _EXIT_FAILURE

	def _setActiveLow(self, activeLow):
		"""Set the desired GPIO direction"""
		ret = _EXIT_FAILURE
		# generate the gpio sysfs instance
		status 	= self._initGpio()

		if status == _EXIT_SUCCESS:
			gpioFile 	= self.path + "/" + GPIO_ACTIVE_LOW_FILE

			if activeLow == _GPIO_ACTIVE_HIGH or activeLow == _GPIO_ACTIVE_LOW:
				with open(gpioFile, 'w') as fd:
					print 'Writing %s to %s file'%(str(activeLow), gpioFile)
					fd.write(str(activeLow))
					fd.close()
					ret = _EXIT_SUCCESS

			# release the gpio sysfs instance
			status 	= self._freeGpio()

			return ret

		return _EXIT_FAILURE

	def setActiveHigh(self):
		ret 	= self._setActiveLow(_GPIO_ACTIVE_HIGH)
		return 	ret

	def setActiveLow(self):
		ret 	= self._setActiveLow(_GPIO_ACTIVE_LOW)
		return 	ret


