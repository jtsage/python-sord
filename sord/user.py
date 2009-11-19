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
#import MySQLdb, time
import time, socket
from config import sord

class sordUser():
	thisSord = sord()
	#Passed at init now. dbc = MySQLdb.connect(host=str(thisSord.sqlServer()), db=str(thisSord.sqlDatabase()), user=str(thisSord.sqlUser()), passwd=str(thisSord.sqlPass()))
	#Passed at init now. db = dbc.cursor()
	expert = False
	
	def __init__(self, loginname, dbc, db, connection, art):
		""" Find and set the userID in the object """
		self.dbc = dbc
		self.db = db
		self.connection = connection
		self.art = art
		self.jennielevel = 0
		self.jennieused = False
		thisSQL = "SELECT userid,password,fullname FROM "+self.thisSord.sqlPrefix()+"users WHERE username = '"+loginname+"'"
		self.thisUserName = loginname
		self.db.execute(thisSQL)
			
		if self.db.rowcount > 0:
			for (userid, password, fullname) in self.db.fetchall():
				self.thisUserID = userid
				self.thisPassword = password
				self.thisFullname = fullname
		else:
			self.thisUserID = 0
			self.thisPassword = ""
			self.thisFullname = "unregistered"

	def write(self, data):
		for thisData in list(data):
			time.sleep(0.001)
			self.connection.send(thisData)

	def pause(self):
		self.write("\r\n    \x1b[1m\x1b[32m:\x1b[0m\x1b[32m-\x1b[1m\x1b[32m: P\x1b[0m\x1b[32mress \x1b[1m\x1b[32mA\x1b[0m\x1b[32mny \x1b[1m\x1b[32mK\x1b[0m\x1b[32mey \x1b[1m\x1b[32m:\x1b[0m\x1b[32m-\x1b[1m\x1b[32m:")
		pauser_quit = False
		while ( not pauser_quit ):
			data = self.connection.recv(5)
			if not data: break
			pauser_quit = True
			self.connection.send("\r\n")

	def userExist(self, fullname):
		searchname = self.dbc.escape_string(fullname)
		thisSQL = "SELECT userid FROM "+self.thisSord.sqlPrefix()+"users WHERE fullname = '"+searchname+"'"
		self.db.execute(thisSQL)
		
		if self.db.rowcount > 0:
			thisReturn = self.db.fetchone()
			return thisReturn[0]
		else:
			return 0
	
	def userLoginExist(self, username):
		searchname = self.dbc.escape_string(username)
		thisSQL = "SELECT userid FROM "+self.thisSord.sqlPrefix()+"users WHERE username = '"+searchname+"'"
		self.db.execute(thisSQL)
		
		if self.db.rowcount > 0:
			return True
		else:
			return False
	
	def userGetName(self, someID):
		thisSQL = "SELECT fullname FROM "+self.thisSord.sqlPrefix()+"users WHERE userid = "+str(someID)
		self.db.execute(thisSQL)
		if self.db.rowcount > 0:
			thisReturn = self.db.fetchone()
			return thisReturn[0]
		else:
			return 0
			
	def userGetLogin(self, someID):
		thisSQL = "SELECT username FROM "+self.thisSord.sqlPrefix()+"users WHERE userid = "+str(someID)
		self.db.execute(thisSQL)
		if self.db.rowcount > 0:
			thisReturn = self.db.fetchone()
			return thisReturn[0]
		else:
			return 0
			
	def isOnline(self):
		thisSQL = "SELECT * FROM "+self.thisSord.sqlPrefix()+"online WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		if self.db.rowcount > 0:
			return True
		else:
			return False
			
	def toggleXprt(self):
		if self.expert == False:
			self.expert = True
		else:
			self.expert = False

	def logout(self):  
		"""Log a user out"""
		thisSQL = "DELETE FROM "+self.thisSord.sqlPrefix()+"online WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)

	def login(self):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"users SET last = CURRENT_TIMESTAMP WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisSQL = "INSERT INTO "+self.thisSord.sqlPrefix()+"online ( `userid` ) VALUES ( "+str(self.thisUserID)+" )"
		self.db.execute(thisSQL)
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET atinn = 0 WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		self.logontime = time.time()
		
	def setDead(self, inst=0):
		"""Set a user as dead"""
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"users SET alive = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def isDead(self):
		"""Check if a user is dead"""
		thisSQL = "SELECT alive FROM "+self.thisSord.sqlPrefix()+"users WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisAlive = self.db.fetchone()
		if ( thisAlive[0] == 1 ):
			return False
		else:
			return True

	def getLevel(self):
		"""Get user level"""
		thisSQL = "SELECT level FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getClass(self):
		""" Get Player class """
		thisSQL = "SELECT class FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getSex(self):
		thisSQL = "SELECT sex FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def didBard(self):
		thisSQL = "SELECT sung FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		if ( thisReturn[0] == 1 ):
			return True
		else:
			return False
			
	def didFlirt(self):
		thisSQL = "SELECT flirt FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		if ( thisReturn[0] == 1 ):
			return True
		else:
			return False
			
	def didInn(self):
		thisSQL = "SELECT atinn FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		if ( thisReturn[0] == 1 ):
			return True
		else:
			return False
			
	def didMaster(self):
		thisSQL = "SELECT master FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		if ( thisReturn[0] == 1 ):
			return True
		else:
			return False
			
	def didHorse(self):
		thisSQL = "SELECT horse FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		if ( thisReturn[0] == 1 ):
			return True
		else:
			return False
			
	def didFairy(self):
		thisSQL = "SELECT fairy FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		if ( thisReturn[0] == 1 ):
			return True
		else:
			return False
			
	def getArmor(self):
		thisSQL = "SELECT armor FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getWeapon(self):
		thisSQL = "SELECT weapon FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getGold(self):
		thisSQL = "SELECT gold FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getBank(self):
		thisSQL = "SELECT bank FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getDefense(self):
		thisSQL = "SELECT def FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getStrength(self):
		thisSQL = "SELECT str FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getHP(self):
		thisSQL = "SELECT hp FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getHPMax(self):
		thisSQL = "SELECT hpmax FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getExperience(self):
		thisSQL = "SELECT exp FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getGems(self):
		thisSQL = "SELECT gems FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getCharm(self):
		thisSQL = "SELECT charm FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getKiller(self):
		thisSQL = "SELECT pkill FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getFuck(self):
		thisSQL = "SELECT fuck FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getDragon(self):
		thisSQL = "SELECT dkill FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getForestFight(self):
		thisSQL = "SELECT ffight FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getPlayerFight(self):
		thisSQL = "SELECT pfight FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def setHorse(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET horse = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setFairy(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET fairy = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setInn(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET atinn = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setFlirt(self, inst=1):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET flirt = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setMaster(self, inst=1):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET master = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setKiller(self, inst=1):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET pkill = pkill + "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setDragon(self, inst=1):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET dkill = dkill + "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setClass(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET class = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setBard(self, inst=1):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET sung = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setSex(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET sex = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setArmor(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET armor = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def setWeapon(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET weapon = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)

	def setLevel(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET level = "+str(inst)+" WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)

	def updateGold(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET gold = (gold + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateBank(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET bank = (bank + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateDefense(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET def = (def + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)

	def updateStrength(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET str = (str + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateFuck(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET fuck = (fuck + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateExperience(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET exp = (exp + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateHP(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET hp = (hp + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateHPMax(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET hpmax = (hpmax + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateGems(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET gems = (gems + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateCharm(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET charm = (charm + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateForestFight(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET ffight = (ffight + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updatePlayerFight(self, inst):
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET pfight = (pfight + "+str(inst)+") WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)

	def nameSkill(self, skill):
		if ( skill == 1 ):
			return 'used'
		if ( skill == 2 ):
			return 'usem'
		if ( skill == 3 ):
			return 'uset'
	
	def nameSkillPoint(self, skill):
		if ( skill == 1 ):
			return 'spcld'
		if ( skill == 2 ):
			return 'spclm'
		if ( skill == 3 ):
			return 'spclt'
		
	def getSkillUse(self, skill):
		skillname = self.nameSkill(skill)
		thisSQL = "SELECT "+skillname+" FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])
		
	def getSkillPoint(self, skill):
		skillname = self.nameSkillPoint(skill)
		thisSQL = "SELECT "+skillname+" FROM "+self.thisSord.sqlPrefix()+"stats WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		thisReturn = self.db.fetchone()
		return int(thisReturn[0])

	def updateSkillUse(self, skill, inst):
		skillname = self.nameSkill(skill)
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET "+skillname+" = ( "+skillname+" + "+str(inst)+" ) WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
		
	def updateSkillPoint(self, skill, inst):
		skillname = self.nameSkillPoint(skill)
		thisSQL = "UPDATE "+self.thisSord.sqlPrefix()+"stats SET "+skillname+" = ( "+skillname+" + "+str(inst)+" ) WHERE userid = "+str(self.thisUserID)
		self.db.execute(thisSQL)
