#!/usr/bin/python
"""
 * Logging class
 * 
 * Contains specialized sord logging class
 * 
"""
import time

class sordLogger():
	""" Logger class """
	def __init__(self):
		self.__mainLogger = list()
		self.__activePeers = 0
		self.__totalPeers = 0
		
	def add(self, value):
		"""Add *arg to log"""
		tmptime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
		self.__mainLogger.append(tmptime+" :: "+value)
		self.__mainLogger = self.__mainLogger[-100:]
		
	def show(self, value):
		""" Show *arg log items """
		return self.__mainLogger[(value * -1):]
		
	def addcon(self):
		""" Increment connection """
		self.__activePeers += 1
		self.__totalPeers += 1
		
	def remcon(self):
		""" Remove connection from active """
		self.__activePeers -= 1
		
	def getactive(self):
		""" Get active peers """
		return self.__activePeers
		
	def gettotal(self):
		""" Get total peers """
		return self.__totalPeers

