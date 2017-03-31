from multiprocessing import Lock

class CircularBuffer(object):
	def __init__(self, size, isPushLock, isPopLock):		
		self.__maxSize = size
		self.__mask = CircularBuffer.nextGreaterPowerOf2(size) - 1
		self.__data = [None] * self.__maxSize
		self.__consumerIdx = 0
		self.__producerIdx = 0
		if isPopLock:
			self.__consLock = Lock()
		else:
			self.__consLock = None
		if isPushLock:
			self.__prodLock = Lock()
		else:
			self.__consLock = None

	@staticmethod
	def nextGreaterPowerOf2(x):
		return 1<<(x-1).bit_length()

	def count(self):
		return self.__producerIdx - self.__consumerIdx

	def isFull(self):
		return self.count() == self.__maxSize

	def push(self, value):
		if self.isFull():
			return False
		if self.__prodLock is None:
			self.__push(value)
		else:
			with self.__prodLock:
				self.__push(value)
		return True

	def __push(self, value):
		self.__producerIdx += 1
		self.__data[self.__producerIdx & self.__mask] = value

	def	pop(self):
		if self.count() == 0:
			return None
		if self.__consLock is Lock:
			with self.__consLock:
				return self.__pop()
		return self.__pop()

	def __pop(self):
		self.__consumerIdx += 1
		return self.__data[self.__consumerIdx & self.__mask]