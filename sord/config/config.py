#!/usr/bin/python
"""
 * Configuration file.
 * 
 * Contains all configuration data for the game
 * 
"""
from random import randint

class sordConfig():
	def __init__(self, testing=0):
		self.sqlitefile = "sord.db"
		
		self.gameadmin = "jtsage"
		self.gameadminpass = "legend"
		
		self.host = "sord.jtsage.com"
		self.admin = "J.T.Sage"
		
		self.daylength = 24
		self.bankinterest = 2
		self.delinactive = 256
		self.ffight = 30
		self.pfight = 5
		
		self.version = "2.0-pysqlite"

		self.port = 6969
		self.fulldebug = False
		self.ansiskip = False
		
		if ( testing ):
			self.port += randint(1, 10)
			
if ( __name__ == "__main__" ):
	cc = config()
	print "SORD Version: ", cc.version
	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print cc.host, " :: ", cc.port
	print "Admin: ", cc.admin
	print "Day is ", cc.daylength, " hours"
	print "Inactive deletes after ", cc.delinactive, " days"
	print "Forest fights ", cc.ffight, "/day"
	print "Player fights ", cc.pfight, "/day"
	print "Game admin: ", cc.gameadmin, "/", cc.gameadminpass
	
