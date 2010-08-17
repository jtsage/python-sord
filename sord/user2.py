#!/usr/bin/python
"""
 * User Control Functions and Class.
 * 
 * Controls user statistics and calls
 * 
 * @package phpsord
 * @subpackage phpsord-general
 * @author J.T.Sage
"""
import time, socket, random
from config import sord

class sorduser(object):
	
	expert = False # Expert mode enabled
	quick = False # No modem pause
	skills = ['', 'd', 'm', 't' ] # Enumerated skill names (db)
	thisSord = sord() # Local copy of config
	directsql = [ # Direct SQL name access
		'level', 'armor', 'weapon', 'gold', 'bank', 'defence', 
		'str', 'hp', 'hpmax', 'exp', 'gems', 'charm', 'pkill', 
		'fuck', 'ffight', 'pfight', 'dkill', 'cls', 'sex', 
		'sung', 'flirt', 'atinn', 'master', 'horse', 'fairy', 
		'dragon', 'alive']
	
	def __init__(self, loginname, dbcon, ntcon, art, speed = 0, noise=0):
		""" Create a sord user class - all functions through here"""
		self.dbcon = dbcon
		self.ntcon = ntcon
		self.art = art
		self.jennielevel = 0
		self.jennieused = False
		self.linespeed = speed
		self.noise = noise
		
		if ( speed == 0 ):
			self.ppause = 0.001
		elif ( speed == 1 ):
			self.ppause = 0.002
		elif ( speed == 2 ):
			self.ppause = 0.0005
		elif ( speed == 3 ):
			self.ppause = 0.00001
		
		thisSQL = "SELECT userid,password,fullname FROM users WHERE username = '"+loginname+"'"
		self.thisUserName = loginname
		
		db = dbcon.cursor()
		db.execute(thisSQL)
		
		row = db.fetchone()
		if not row:
			self.thisUserID = 0
			self.thisPassword = ""
			self.thisFullname = "unregistered"
		else:
			userid, password, fullname = row
			self.thisUserID = userid
			self.thisPassword = password
			self.thisFullname = fullname
		db.close()
		
	def __getattr__(self,name):
		""" Get object attribute - hijack sql attributes for lookup from sqlite """
		if name in self.directsql :
			db = self.dbcon.cursor()
			db.execute("SELECT "+name+" FROM stats WHERE userid = ?", (self.thisUserID,))
			return db.fetchone()[0]
			db.close()
		else: 
			return object.__getattr__(self,name)
			
	def __setattr__(self,name,value):
		""" Set object attribute - hijack sql attributes - set immediatly in sqlite """
		if name in self.directsql :
			self.dbcon.execute("UPDATE stats SET "+name+"=? WHERE userid=?", (value, self.thisUserID))
			self.dbcon.commit()
		else:
			object.__setattr__(self,name,value)

	def isOnline(self):
		""" Check if user is online """
		db = self.dbcon.cursor()
		db.execute("SELECT * FROM online WHERE userid = ?", (self.thisUserID,))
		row = db.fetchone()
		if not row:
			return False
		else:
			return True

	def getSkillUse(self, skill):
		""" Get skill use points """
		db = self.dbcon.cursor()
		db.execute("SELECT use"+self.skills[skill]+" FROM stats WHERE userid = ?", (self.thisUserID, ))
		return db.fetchone()[0]
		db.close()
		
	def getSkillPoint(self, skill):
		""" Get skill experience points """
		db = self.dbcon.cursor()
		db.execute("SELECT spcl"+self.skills[skill]+" FROM stats WHERE userid = ?", (self.thisUserID, ))
		return db.fetchone()[0]
		db.close()

	def updateSkillUse(self, skill, value):
		""" Update skill use points """
		self.dbcon.execute("UPDATE stats SET use"+self.skills[skill]+"= use"+self.skills[skill]+" + ? WHERE userid=?", (value, self.thisUserID))
		self.dbcon.commit()
		
	def updateSkillPoint(self, skill, value):
		""" Update skill experience points """
		self.dbcon.execute("UPDATE stats SET spcl"+self.skills[skill]+"= spcl"+self.skills[skill]+" + ? WHERE userid=?", (value, self.thisUserID))
		self.dbcon.commit()
		
	def toggleXprt(self):
		""" Toggle expert mode """
		if self.expert == False:
			self.expert = True
		else:
			self.expert = False
		
	def toggleQuick(self):
		""" Toggle quick (no modem pause) mode """
		if ( self.quick ):
			self.quick = False
		else:
			self.quick = True
			
	def write(self, data):
		""" Send data to connected client """
		if ( self.quick ): 
			self.ntcon.send(data)
		else:
			for thisData in list(data):
				if ( self.noise ):
					if ( random.randint(1, 2000) == 3 ):
						thisData = ''
				time.sleep(self.ppause)
				self.ntcon.send(thisData)

	def pause(self):
		""" Send pause string and wait for input """
		self.write("\r\n    \x1b[1m\x1b[32m:\x1b[0m\x1b[32m-\x1b[1m\x1b[32m: P\x1b[0m\x1b[32mress \x1b[1m\x1b[32mA\x1b[0m\x1b[32mny \x1b[1m\x1b[32mK\x1b[0m\x1b[32mey \x1b[1m\x1b[32m:\x1b[0m\x1b[32m-\x1b[1m\x1b[32m:")
		pauser_quit = False
		while ( not pauser_quit ):
			data = self.ntcon.recv(5)
			if not data: break
			pauser_quit = True
			self.ntcon.send("\r\n")
			
	def login(self):
		""" Process user login """
		self.dbcon.execute("UPDATE users SET last = ? WHERE userid = ?", (time.strftime('%Y%j', time.localtime()),self.thisUserID))
		self.dbcon.execute("INSERT INTO online ( userid, whence ) VALUES ( ?, ? )", (self.thisUserID, time.ctime(time.time())))
		self.dbcon.execute("UPDATE stats SET atinn = 0 WHERE userid = ?", (self.thisUserID,))
		self.logontime = time.time()
		self.dbcon.commit()
		
	def logout(self):
		""" Process user logout """
		self.dbcon.execute("DELETE FROM online WHERE userid = ?", (self.thisUserID,))
		self.dbcon.commit()

	def userExist(self, value):
		""" Check is user (fullname) exists.  Return userid on true """
		db = self.dbcon.cursor()
		db.execute("SELECT userid FROM users WHERE fullname = ?", (value, ))
		row = db.fetchone()
		if not row:
			retrn = 0
		else:
			retrn = row[0]
		db.close()
		return retrn
	
	def userLoginExist(self, value):
		""" Check is user (login name) exists.  Return userid on true """
		db = self.dbcon.cursor()
		db.execute("SELECT userid FROM users WHERE username = ?", (value, ))
		row = db.fetchone()
		if not row:
			retrn = False
		else:
			retrn = row[0]
		db.close()
		return retrn
	
	def userGetName(self, value):
		""" Get user fullname from userid """
		db = self.dbcon.cursor()
		db.execute("SELECT fullname FROM users WHERE userid = ?", (value, ))
		row = db.fetchone()
		if not row:
			retrn = 0
		else:
			retrn = row[0]
		db.close()
		return retrn
			
	def userGetLogin(self, value):
		""" Get user login name from userid """
		db = self.dbcon.cursor()
		db.execute("SELECT username FROM users WHERE userid = ?", (value, ))
		row = db.fetchone()
		if not row:
			retrn = 0
		else:
			retrn = row[0]
		db.close()
		return retrn
