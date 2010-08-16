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
import time, socket
from config import sord

class sorduser(object):
	
	expert = False
	quick = False
	skills = ['', 'd', 'm', 't' ]
	thisSord = sord()
	
	def __init__(self, loginname, dbcon, ntcon, art):
		
		self.dbcon = dbcon
		self.ntcon = ntcon
		self.art = art
		self.jennielevel = 0
		self.jennieused = False
		
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
		if ( name == 'alive' ):
			db = self.dbcon.cursor()
			db.execute("SELECT alive FROM users WHERE userid = ?", (self.thisUserID,))
			return db.fetchone()[0]
			db.close()
		elif name in ['level', 'armor', 'weapon', 'gold', 'bank', 'defence', 'str', 'hp', 'hpmax', 'exp', 'gems', 'charm', 'pkill', 'fuck', 'ffight', 'pfight', 'dkill', 'cls', 'sex', 'sung', 'flirt', 'atinn', 'master', 'horse', 'fairy'] :
			db = self.dbcon.cursor()
			db.execute("SELECT "+name+" FROM stats WHERE userid = ?", (self.thisUserID,))
			return db.fetchone()[0]
			db.close()
		else: 
			return object.__getattr__(self,name)
			
	def __setattr__(self,name,value):
		if ( name == 'alive' ):
			self.dbcon.execute('UPDATE users SET alive=? WHERE userid=?', (value, self.thisUserID))
			self.dbcon.commit()
		elif name in ['level', 'armor', 'weapon', 'gold', 'bank', 'defence', 'str', 'hp', 'hpmax', 'exp', 'gems', 'charm', 'pkill', 'fuck', 'ffight', 'pfight', 'dkill', 'cls', 'sex', 'sung', 'flirt', 'atinn', 'master', 'horse', 'fairy'] :
			self.dbcon.execute("UPDATE stats SET "+name+"=? WHERE userid=?", (value, self.thisUserID))
			self.dbcon.commit()
		else:
			object.__setattr__(self,name,value)

	def isOnline(self):
		db = self.dbcon.cursor()
		db.execute("SELECT * FROM online WHERE userid = ?", (self.thisUserID,))
		row = db.fetchone()
		if not row:
			return False
		else:
			return True

	def getSkillUse(self, skill):
		db = self.dbcon.cursor()
		db.execute("SELECT use"+self.skills[skill]+" FROM stats WHERE userid = ?", (self.thisUserID, ))
		return db.fetchone()[0]
		db.close()
		
	def getSkillPoint(self, skill):
		db = self.dbcon.cursor()
		db.execute("SELECT spcl"+self.skills[skill]+" FROM stats WHERE userid = ?", (self.thisUserID, ))
		return db.fetchone()[0]
		db.close()

	def updateSkillUse(self, skill, value):
		self.dbcon.execute("UPDATE stats SET use"+self.skills[skill]+"= use"+self.skills[skill]+" + ? WHERE userid=?", (value, self.thisUserID))
		self.dbcon.commit()
		
	def updateSkillPoint(self, skill, value):
		self.dbcon.execute("UPDATE stats SET spcl"+self.skills[skill]+"= spcl"+self.skills[skill]+" + ? WHERE userid=?", (value, self.thisUserID))
		self.dbcon.commit()
		
	def toggleXprt(self):
		if self.expert == False:
			self.expert = True
		else:
			self.expert = False
		
	def toggleQuick(self):
		if ( self.quick ):
			self.quick = False
		else:
			self.quick = True
			
	def write(self, data):
		for thisData in list(data):
			if ( not self.quick ):
				time.sleep(0.001)
			self.ntcon.send(thisData)

	def pause(self):
		self.write("\r\n    \x1b[1m\x1b[32m:\x1b[0m\x1b[32m-\x1b[1m\x1b[32m: P\x1b[0m\x1b[32mress \x1b[1m\x1b[32mA\x1b[0m\x1b[32mny \x1b[1m\x1b[32mK\x1b[0m\x1b[32mey \x1b[1m\x1b[32m:\x1b[0m\x1b[32m-\x1b[1m\x1b[32m:")
		pauser_quit = False
		while ( not pauser_quit ):
			data = self.ntcon.recv(5)
			if not data: break
			pauser_quit = True
			self.ntcon.send("\r\n")
			
	def login(self):
		self.dbcon.execute("UPDATE users SET last = ? WHERE userid = ?", (time.ctime(time.time()),self.thisUserID))
		self.dbcon.execute("INSERT INTO online ( userid, whence ) VALUES ( ?, ? )", (self.thisUserID, time.ctime(time.time())))
		self.dbcon.execute("UPDATE stats SET atinn = 0 WHERE userid = ?", (self.thisUserID,))
		self.logontime = time.time()
		self.dbcon.commit()
		
	def logout(self):
		self.dbcon.execute("DELETE FROM online WHERE userid = ?", (self.thisUserID,))
		self.dbcon.commit()

	def userExist(self, value):
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
		db = self.dbcon.cursor()
		db.execute("SELECT username FROM users WHERE userid = ?", (value, ))
		row = db.fetchone()
		if not row:
			retrn = 0
		else:
			retrn = row[0]
		db.close()
		return retrn
