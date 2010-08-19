#!/usr/bin/python
"""
 * Fighting Subsystem.
 * Contains forest fights, events, player fights, leveling up
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage """
import random, re, time
from ..base import func
from . import data
from . import util
from . import menu
from ..igm import dht

class getenemy():
	def __init__(self, level):
		self.level = level
		topenemy = len(data.enemies[level]) - 1
		enemynum = random.randint(0, topenemy)
		
		if ( random.randint(1,10) == 8 ):
			self.underdog = True
		else:
			self.underdog = False
			
		self.hit    = data.enemies[level][enemynum][2] / 2
		self.hp     = data.enemies[level][enemynum][3]
		self.name   = data.enemies[level][enemynum][0]
		self.weapon = data.enemies[level][enemynum][1]
		self.win    = data.enemies[level][enemynum][6]
		self.exp    = data.enemies[level][enemynum][5]
		self.gold   = data.enemies[level][enemynum][4]


class ffight():
	def __init__(self, user, healers):
		self.user = user
		self.healers = healers
	
	def run(self):
		""" Forest Fight - Non-Combat """
		user = self.user
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if ( not user.expert ):
					user.write(user.art.forest())
					if ( user.horse == True ): 
						user.write(func.normmenu("(T)ake Horse to Dark Horse Tavern"))
				user.write(menu.forest(self.user))
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( user.config.fulldebug and key[0] == '!' ): # Debug happenings - by number
				try:
					number = int(func.getLine(user.ntcon, True))
				except ValueError:
					number = 0
				if ( number > 0 and number < 13 ):
					user.write("\r\n")
					self.special(True, number)
			elif ( key[0] == 'q' or key[0] == 'Q' or key[0] == 'r' or key[0] == 'R' ):
				user.write('Q')
				thisQuit = True
			elif ( key[0] == '?' ):
				user.write('?')
				if ( user.expert ):
					user.write(user.art.forest())
			elif ( key[0] == 'x' or key[0] == 'X' ):
				user.write('X')
				user.toggleXprt()
			elif ( key[0] == 's' or key[0] == 'S' ):
				if ( user.level == 12 ):
					user.write('S')
					self.dragon()
			elif ( key[0] == 'h' or key[0] == 'H' ):
				user.write('H')
				self.healers.run()
			elif ( key[0] == 'v' or key[0] == 'V' or key[0] == 'y' or key[0] == 'Y' ):
				user.write(util.viewstats(user))
			elif ( key[0] == 'l' or key[0] == 'l' ):
				user.write("L\r\n")
				if ( user.ffight > 0 ):
					if ( random.randint(1, 8) == 3 ):
						self.special()
					else:
						self.fight()
				else:
					user.write(func.casebold("\r\n  You are mighty tired.  Try again tommorow\r\n", 2))
			elif ( key[0] == 'a' or key[0] == 'A' ):
				user.write('A')
				user.write(func.casebold("\r\n  You brandish your weapon dramatically.\r\n", 2))
			elif ( key[0] == 'd' or key[0] == 'D' ):
				user.write('D')
				user.write(func.casebold("\r\n  Your Death Knight skills cannot help your here.\r\n", 2))
			elif ( key[0] == 'm' or key[0] == 'M' ):
				user.write('M')
				user.write(func.casebold("\r\n  Your Mystical skills cannot help your here.\r\n", 2))
			elif ( key[0] == 't' or key[0] == 'T' ):
				user.write('T')
				if ( user.horse == True ):
					thismod = dht.dht()
					thismod.run()
					del thismod
				else:
					user.write(func.casebold("\r\n  Your Thieving skills cannot help your here.\r\n", 2))
			elif ( key[0] == 'b' or key[0] == 'B' ):
				user.write('B')
				user.write(func.casebold("\r\n  A buzzard swoops down and grabs all your gold on hand.\r\n", 2))
				if ( user.gold > 0 ):
					user.bank += user.gold
					user.gold = 0
			else:
				skipDisp = True

	def menu(self, user, enemy) : 
		""" Forest Fight Menu """
		thismenu  = "\r\n  \x1b[32mYour Hitpoints : \x1b[1m"+str(user.hp)+"\x1b[0m\r\n"
		thismenu += "  \x1b[32m"+enemy.name+"'s Hitpoints : \x1b[1m"+str(enemy.hp)+"\x1b[0m\r\n\r\n"
		thismenu += func.normmenu("(A)ttack")
		thismenu += func.normmenu("(S)tats")
		thismenu += func.normmenu("(R)un")
		thismenu += "\r\n"
		if ( user.getSkillUse(1) > 0 ):
			thismenu += func.normmenu("(D)eath Knight Attack ("+str(user.getSkillUse(1))+")")
		if ( user.getSkillUse(2) > 0 ):
			thismenu += func.normmenu("(M)ystical Powers ("+str(user.getSkillUse(2))+")")
		if ( user.getSkillUse(3) > 0 ):
			thismenu += func.normmenu("(T)heiving Sneak Attack ("+str(user.getSkillUse(3))+")")
		thismenu += "\r\n  \x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? [\x1b[1;35mA\x1b[0m\x1b[32m] : \x1b[0m"
		return thismenu
		
	def dmenu(self, user, ehp, ename) : 
		""" Forest Fight Menu """
		thismenu  = "\r\n  \x1b[32mYour Hitpoints : \x1b[1m"+str(user.hp)+"\x1b[0m\r\n"
		thismenu += "  \x1b[32m"+ename+"'s Hitpoints : \x1b[1m"+str(ehp)+"\x1b[0m\r\n\r\n"
		thismenu += func.normmenu("(A)ttack")
		thismenu += func.normmenu("(S)tats")
		thismenu += func.normmenu("(R)un")
		thismenu += "\r\n"
		if ( user.getSkillUse(1) > 0 ):
			thismenu += func.normmenu("(D)eath Knight Attack ("+str(user.getSkillUse(1))+")")
		if ( user.getSkillUse(2) > 0 ):
			thismenu += func.normmenu("(M)ystical Powers ("+str(user.getSkillUse(2))+")")
		if ( user.getSkillUse(3) > 0 ):
			thismenu += func.normmenu("(T)heiving Sneak Attack ("+str(user.getSkillUse(3))+")")
		thismenu += "\r\n  \x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? [\x1b[1;35mA\x1b[0m\x1b[32m] : \x1b[0m"
		return thismenu

	def fight(self):
		""" Forest Fight System """
		user = self.user
		user.ffight -= 1
		enemy = getenemy(user.level)
		udef = user.defence
		uhit = user.str / 2
		
		ctrlDead = False
		ctrlRan  = False
		ctrlWin  = False
		
		user.write("\r\n\r\n  \x1b[32m**\x1b[1;37mFIGHT\x1b[0m\x1b[32m**\r\n")
		user.write("\r\n  \x1b[32mYou have encountered "+enemy.name+"!!\x1b[0m\r\n")
	
		if ( enemy.underdog ): # User is the underdog 
			if ( user.horse == True and random.randint(1, 3) == 2 ): # Saved by the horse 
				user.write("\r\n  \x1b[32m\"Prepare to die, fool!\" "+enemy.name+" screams.\r\n  He takes a Death Crystal from his cloak and throws it at you.\r\n  Your horse moves its huge body to intercept the crystal.\r\n")
				user.write("\r\n  \x1b[1mYOUR HORSE IS VAPORIZED!\x1b[0;32m\r\n\r\n  Tears of anger flow down your cheeks.  Your valiant steed must be\r\n  avenged.\r\n")
				user.write("\r\n  \x1b[1mYOU PUMMEL "+enemy.name+" WITH BLOWS!\x1b[0;32m\r\n\r\n  A few seconds later, your adversary is dead.\r\n  You bury your horse in a small clearing.  The best friend you ever\r\n  had.\r\n")
				enemy.hp = 0
				ctrlWin = True
				user.horse = 0
			else:
				hisAttack = ( enemy.hit + random.randint(0, ememy.hit)) - udef
				if ( hisAttack > 0 ):
					if ( hisAttack >= user.hp ):
						ctrlDead = True
						hisAttack = user.hp
					user.write("\r\n  \x1b[32m"+enemy.name+" executes a sneak attach for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage!\x1b[0m\r\n")
					user.hp -= hisAttack
				else:
					user.write("\r\n  \x1b[32m"+enemy.name+" misses you completely!\x1b[0m\r\n")
		else:
			user.write("\r\n  \x1b[32mYour skill allows you to get the first strike.\x1b[0m\r\n")
	
		skipDisp = False
		while ( user.hp > 0 and enemy.hp > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
			if ( not skipDisp ):
				user.write(self.menu(user, enemy))
			skipDisp = False
			key = user.ntcon.recv(2)
			if not key: break
			elif ( key[0] == 's' or key[0] == 'S' ):
				user.write('S')
				user.write(util.viewstats(user))
			elif ( key[0] == 'a' or key[0] == 'A' ): # Attack!
				user.write("A\r\n")
				hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
				myAttack  = ( uhit + random.randint(0, uhit))
				if ( not enemy.underdog ): # We Hit First
					if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
						hisAttack = 0
				if ( hisAttack >= user.hp ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.hp # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  \x1b[32m"+enemy.name+" hits you with "+enemy.weapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
					user.hp -= hisAttack
				else: 
					user.write("\r\n  \x1b[32m"+enemy.name+" misses you completely\x1b[0m\r\n")
				if ( myAttack > 0 and not ctrlDead ): # We hit him!
					user.write("\r\n  \x1b[32mYou hit "+enemy.name+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
					enemy.hp -= myAttack
					if ( enemy.hp < 1 ): # We Win!
						ctrlWin = True
						user.write("\r\n  \x1b[31m"+enemy.win+"\x1b[0m\r\n")
						
			elif ( key[0] == 'd' or key[0] == 'D' ): # Death Knight Attack!
				user.write("D\r\n")
				if ( user.getSkillUse(1) > 0 ):
					user.updateSkillUse(1, -1)
					hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
					myAttack  = ( uhit + (random.randint(2,5) * random.randint((uhit / 2), uhit))) + uhit
					if ( not enemy.underdog ): # We Hit First
						if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
							hisAttack = 0
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  \x1b[32m"+enemy.name+" hits you with "+enemy.weapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
						user.hp -= hisAttack
					else: 
						user.write("\r\n  \x1b[32m"+enemy.name+" misses you completely\x1b[0m\r\n")
					if ( myAttack > 0 and not ctrlDead ): # We hit him!
						user.write("\r\n  \x1b[1;32mUltra Powerful Move!\x1b[0m\r\n  \x1b[32mYou hit "+enemy.name+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
						enemy.hp -= myAttack
						if ( thisEnemyHP < 1 ): # We Win!
							ctrlWin = True
							user.write("\r\n  \x1b[31m"+enemy.win+"\x1b[0m\r\n")
				else:
					user.write("\r\n  \x1b[32mYou have no Death Knight Skill Use Points!\x1b[0m\r\n\r\n")
					
			elif ( key[0] == 't' or key[0] == 'T' ): # Thief Sneaky Attack!
				user.write("T\r\n")
				if ( user.getSkillUse(3) > 0 ):
					user.updateSkillUse(3, -1)
					hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - ( udef * 2 )
					myAttack  = ( uhit + (random.randint(1,3) * random.randint((uhit / 2), uhit))) + uhit
					if ( not enemy.underdog ): # We Hit First
						if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
							hisAttack = 0
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  \x1b[32m"+enemy.name+" hits you with "+enemy.weapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
						user.hp -= hisAttack
					else: 
						user.write("\r\n  \x1b[32m"+enemy.name+" misses you completely\x1b[0m\r\n")
					if ( myAttack > 0 and not ctrlDead ): # We hit him!
						user.write("\r\n  \x1b[1;32mUltra Sneaky Move!\x1b[0m\r\n  \x1b[32mYou hit "+enemy.name+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
						enemy.hp -= myAttack
						if ( enemy.hp < 1 ): # We Win!
							ctrlWin = True
							user.write("\r\n  \x1b[31m"+enemy.win+"\x1b[0m\r\n")
				else:
					user.write("\r\n  \x1b[32mYou have no Thief Skill Use Points!\x1b[0m\r\n\r\n")
					
			elif ( key[0] == 'r' or key[0] == 'R' ): # Run Away
				if ( random.randint(1, 10) == 4 ): # Hit in the back.
					hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  \x1b[32m"+enemy.name+" hits you in the back with it's "+enemy.weapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\r\n")
						user.hp -= hisAttack
						ctrlRan = True
				else:
					user.write("\r\n  \x1b[32mYou narrowly escape harm.\x1b[0m\r\n")
					ctrlRan = True
			elif ( key[0] == 'q' or key[0] == 'Q' ):
				user.write("\r\n  \x1b[31mYou are in Combat!  Try Running!\x1b[0m\r\n")
			elif ( key[0] == 'h' or key[0] == 'H' ):
				user.write("\r\n  \x1b[32mYou are in combat, and they don't make house calls!\x1b[0m\r\n")
			elif ( key[0] == 'l' or key[0] == 'L' ):
				user.write("\r\n  \x1b[32mWhat?!  You want to fight two at once?\x1b[0m\r\n")
			elif ( key[0] == 'm' or key[0] == 'M' ): #Magic!
				if ( user.getSkillUse(2) < 1 ):
					user.write("\r\n  \x1b[32mYou have no Magical Use Points!\x1b[0m\r\n\r\n")
				else:
					user.write("\r\n" + func.normmenu("(N)evermind") + func.normmenu("(P)inch Real Hard (1)"))
					if ( user.getSkillUse(2) > 3 ):
						user.write(func.normmenu("(D)isappear (4)"))
						if ( user.getSkillUse(2) > 7 ):
							user.write(func.normmenu("(H)eat Wave (8)"))
							if ( user.getSkillUse(2) > 11 ):
								user.write(func.normmenu("(L)ight Shield (12)"))
								if ( user.getSkillUse(2) > 15 ):
									user.write(func.normmenu("(S)hatter (16)"))
									if ( user.getSkillUse(2) > 19 ):
										user.write(func.normmenu("(M)ind Heal (20)"))
					user.write("\r\n  \x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? [\x1b[1;35mA\x1b[0m\x1b[32m] : \x1b[0m")
					tinyQuit = False
					while ( not tinyQuit ):
						miniData = user.ntcon.recv(2)
						if not miniData: break
						elif ( minikey[0] == 'n' or minikey[0] == 'N' ): #Nothing
							user.write("N\r\n  \x1b[32mSure thing boss.\x1b[0m\r\n")
							tinyQuit = True
						elif ( minikey[0] == 'p' or minikey[0] == 'P' ): #Pinch!
							user.write("P")
							user.updateSkillUse(2, -1)
							tinyQuit = True
							hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
							myAttack  = ( uhit + random.randint(0, uhit)) + ( uhit / 4 )
							if ( not enemy.underdog ): # We Hit First
								if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  \x1b[32m"+enemy.name+" hits you with "+enemy.weapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  \x1b[32m"+enemy.name+" misses you completely\x1b[0m\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  \x1b[32mYou pinch "+enemy.name+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
								enemy.hp -= myAttack
								if ( enemy.hp < 1 ): # We Win!
									ctrlWin = True
									user.write("\r\n  \x1b[31m"+enemy.win+"\x1b[0m\r\n")
						elif ( (minikey[0] == 'd' or minikey[0] == 'D') and ( user.getSkillUse(2) > 3 ) ): #Disappear
							user.write("D\r\n  \x1b[32mYou disapper like a ghost!\x1b[0m\r\n")
							user.updateSkillUse(2, -4)
							tinyQuit = True
							ctrlRan = True
						elif ( (minikey[0] == 'h' or minikey[0] == 'H') and ( user.getSkillUse(2) > 7 ) ): #Heat Wave
							user.write("H")
							user.updateSkillUse(2, -8)
							tinyQuit = True
							hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
							myAttack  = ( uhit + random.randint(0, uhit)) + (uhit / 2)
							if ( not enemy.underdog ): # We Hit First
								if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  \x1b[32m"+enemy.name+" hits you with "+enemy.weapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  \x1b[32m"+enemy.name+" misses you completely\x1b[0m\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  \x1b[32mYou blast "+enemy.name+" with Heat Wave for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
								enemy.hp -= myAttack
								if ( enemy.hp < 1 ): # We Win!
									ctrlWin = True
									user.write("\r\n  \x1b[31m"+enemy.win+"\x1b[0m\r\n")
						elif ( (minikey[0] == 'l' or minikey[0] == 'L') and ( user.getSkillUse(2) > 11 ) ): #Light Shield
							user.write("L\r\n  \x1b[32mYou feel a bit odd.  You dig in a feel better defended\x1b[0m\r\n")
							user.updateSkillUse(2, -12)
							udef = udef * 2
							tinyQuit = True
						elif ( (minikey[0] == 's' or minikey[0] == 'S') and ( user.getSkillUse(2) > 15 ) ): #Shatter
							user.write("S")
							user.updateSkillUse(2, -16)
							tinyQuit = True
							hisAttack = ( enemy.hit + random.randint(0, enemy.hit)) - udef
							myAttack  = ( uhit + random.randint(0, uhit)) + (uhit * 2)
							if ( not enemy.underdog ): # We Hit First
								if ( myAttack >= enemy.hp ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  \x1b[32m"+enemy.name+" hits you with "+enemy.weapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  \x1b[32m"+enemy.name+" misses you completely\x1b[0m\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  \x1b[32mYou Shatter "+enemy.name+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
								enemy.hp -= myAttack
								if ( enemy.hp < 1 ): # We Win!
									ctrlWin = True
									user.write("\r\n  \x1b[31m"+enemy.win+"\x1b[0m\r\n")
						elif ( (minikey[0] == 'm' or minikey[0] == 'M') and ( user.getSkillUse(2) > 19 ) ): #Mind Heal
							user.write("M\r\n  \x1b[32mYou feel much better!\x1b[0m\r\n")
							user.updateSkillUse(2, -20)
							hptoadd = user.hpmax - user.hp
							user.hp = user.hpmax
							if ( hptoadd < 5 ):
								user.write("\r\n  \x1b[32mThough, you are likely clinicly retarded.\x1b[0m\r\n")
							tinyQuit = True
			else: #Catch non-options
				skipDisp = True
	
		if ( ctrlWin ) :
			user.exp += enemy.exp
			user.gold += enemy.gold
			user.write("\r\n  \x1b[32mYou have recieved \x1b[1m"+str(enemy.gold)+"\x1b[22m gold and \x1b[1m"+str(enemy.exp)+"\x1b[22m experience\x1b[0m\r\n")
			user.pause()
		if ( ctrlDead ) :
			if ( user.fairy == True ):
				user.hp = 1
				user.fairy = 0
				user.write(func.casebold("  Miraculously, your fairy saves you from the edge of defeat.  You escape with your life.\r\n", 2))
			else:
				user.alive = 0
				#exception handles, do it later. user.logout()
				lamentTop = len(data.forestdie) - 1
				lamentThis = data.forestdie[random.randint(0, lamentTop)]
				lamentThis = re.sub("`n", "\r\n", lamentThis)
				lamentThis = re.sub("`g", user.thisFullname, lamentThis)
				lamentThis = re.sub("`e", enemy.name, lamentThis)
				user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (lamentThis,))
				user.dbcon.commit()
				user.write(func.casebold("  Tragically, you died.  Returning to the mundane world for the day...\n", 1))
				raise Exception('normal', "User is DOA.  Bummer.")

	def special(self, preset = False, option = 0):
		""" Forest Special Events """
		user = self.user
		if ( preset ):
			happening = option
		else:
			if ( user.horse == True ):
				happening = random.randint(1, 11)
			else:
				happening = random.randint(1, 12)
				
		if ( happening == 1 ):   # Find Gems GOOD!
			thisfind = random.randint(1, 4)
			user.write(user.art.line())
			user.write("  \x1b[32mFortune Smiles Upon You.  You find \x1b[1;37m"+str(thisfind)+"\x1b[0m\x1b[32m gems!\x1b[0m\r\n")
			user.write(user.art.line())
			user.pause()
			user.gems += thisfind
		elif ( happening == 2 ): # Find Gold  GOOD!
			thisfind = random.randint(1, 4) * 200 * user.level
			user.write(user.art.line())
			user.write("  \x1b[32mFortune Smiles Upon You.  You find a sack full of \x1b[1;37m"+str(thisfind)+"\x1b[0m\x1b[32m gold!\x1b[0m\r\n")
			user.write(user.art.line())
			user.pause()
			user.gold += thisfind
		elif ( happening == 3 ): # Hammerstone (attack str++)  GOOD!
			user.write(user.art.line())
			user.write("  \x1b[32mYou find a hammer stone.  You quickly hit it as hard as possible.\r\n\r\n  \x1b[1mYour attack strength is raised by 1!\x1b[0m\r\n")
			user.write(user.art.line())
			user.pause()
			user.str += 1
		elif ( happening == 4 ): # Merry Men (hp = hpmax)
			user.write(user.art.line())
			user.write("  \x1b[32mYou stumble across a group of merry men.\r\n  They offer you ale you can't resist.\r\n  \x1b[1mYou feel refreshed!\x1b[0m\r\n")
			user.write(user.art.line())
			user.pause()
			user.hp = user.hpmax
		elif ( happening == 5 ): # Old Man (gold + (lvl * 500) && charm +1 on help) (costs 1 fight) GOOD!
			user.write(user.art.line())
			user.write("  \x1b[32mYou come upon an old man wandering around.\r\n  He asks you for help back to town.\x1b[0m\r\n\r\n")
			user.write(func.normmenu("(H)elp the old man"))
			user.write(func.normmenu("(I)gnore him"))
			user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
			miniQuit = False
			while ( not miniQuit ):
				data = user.ntcon.recv(2)
				if ( data[0] == 'h' or data[0] == 'H' ):
					user.write('H')
					goldtoadd = user.level * 500
					user.write("\r\n\r\n  \x1b[32mYou help the old gentleman home.\r\n  \x1b[1mHe gives you "+str(goldtoadd)+" gold and 1 charm!.\x1b[0m\r\n")
					user.gold += goldtoadd
					user.charm += 1
					user.ffight -= 1
					miniQuit = True
				elif ( data[0] == 'i' or data[0] == 'I' ):
					user.write('I')
					user.write("\r\n  \x1b[31mYou just really \x1b[1mSUCK\x1b[0;31m, don't you?\x1b[0m\r\n")
					miniQuit = True
				else:
					pass
			user.pause()
		elif ( happening == 6 ): # Ugly (33%) and Pretty (66%) stick GOOD!
			user.write(user.art.line())
			user.write("  \x1b[32mA demented penguin jumps from the bushes and whacks you with a")
			sticktype = random.randint(1, 3)
			if ( sticktype == 2 ):
				user.write("\x1b[1;31m ugly \x1b[0;32m")
			else:
				user.write("\x1b[1m pretty \x1b[0;32m")
			user.write("stick!\r\n  Your charm is ")
			if ( sticktype == 2 ):
				user.write("lowered")
				if ( user.charm > 0 ):
					user.charm -= 1
			else:
				user.write("raised")
				user.charm += 1
			user.write(" by 1!!\x1b[0m\r\n")
			user.pause()
		elif ( happening == 7 ): # Old Hag GOOD!
			user.write(user.art.line())
			user.write("  \x1b[32mYou come across an old hag.\r\n\r\n  \x1b[1m\"Give me a gem my pretty, and I will completely heal you!\"\x1b[0;32m\r\n  She screeches!\x1b[0m\r\n\r\n")
			user.write(func.normmenu("(G)ive her a gem"))
			user.write(func.normmenu("(K)ick her and run"))
			user.write(func.normmenu("(L)eave polietly"))
			miniQuit = False
			while ( not miniQuit ):
				user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
				data = user.ntcon.recv(2)
				if ( data[0] == 'l' or data[0] == 'L' ):
					user.write("L\r\n\r\n  \x1b[32mThe old hag begins following you like a lost puppy.\x1b[0m\r\n")
				elif ( data[0] == 'k' or data[0] == 'K' ):
					user.write("K\r\n\r\n  \x1b[32mYou hate to be rude to your elders, but sometimes deperate times call for\r\n  deperate measures.  You which the old hag in the shin and run for it.\x1b[0m\r\n")
					miniQuit = True
				elif ( data[0] == 'g' or data[0] == 'G' ):
					user.write('G')
					if ( user.gems > 0 ):
						user.write("\r\n\r\n  \x1b[1;32m\"Thank you\"\x1b[0;32m she cackles.\r\n  \x1b[1mYou feel refreshed and renewed\x1b[0m\r\n")
						user.hpmax += 1
						user.hp = user.hpmax
						user.gems -= 1
						miniQuit = True
					else:
						user.write("\r\n\r\n  \x1b[1;32m\"You don't have any gems you stinky cow-pox pustule!\"\[33[0;32m she yells.\r\n  \x1b[1mCome to think of it, you feel rather like a cow-pie.\x1b[0m\r\n")
						user.hp = 1
						miniQuit = True
				else: 
					pass
			user.pause()
		elif ( happening == 8 ): # Flowers in the forest. GOOD!
			user.write(user.art.line())
			user.write("  \x1b[32mYou come across a grove of flowers, and decide to inspect them closer...\r\n  \x1b[1mThere is something written here!\x1b[0m\r\n")
			user.pause()
			util.flowers(user)
		elif ( happening == 9 ): # rescue man/maiden GOOD!
			user.write(user.art.line())
			user.write("  \x1b[32mYou come upon a dead bird.  While gross, you begin to put it out of your\r\n  mind when you notice a scroll attached to it's leg\r\n\r\n")
			user.write("  \x1b[1mTo Whome It May Concern:\r\n    I have been locked in this terrible tower for many cycles.\r\n    Please save me soon!\n        ~ Elora\r\n\r\n")
			user.write(func.normmenu("(S)eek the maiden"))
			user.write(func.normmenu("(I)gnore her plight"))
			user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
			miniQuit = False
			while ( not miniQuit ):
				data = user.ntcon.recv(2)
				if ( data[0] == 'i' or data[0] == 'I' ):
					user.write('I')
					miniQuit = True
				elif ( data[0] == 's' or data[0] == 'S' ):
					user.write('S')
					user.ffight -= 1
					thisMiniQuit = False
					thisTower = 0
					user.write("\r\n\r\n  \x1b[32mWhere do you wish to seek the maiden?\x1b[0m\r\n")
					user.write(func.normmenu("(K)eep of Hielwain"))
					user.write(func.normmenu("(S)tarbucks Seattle Spaceneedle"))
					user.write(func.normmenu("(C)astle Morbidia"))
					user.write(func.normmenu("(S)ty of Pigashia"))
					user.write(func.normmenu("(B)logshares Brutal Belfry"))
					user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
					while ( not thisMiniQuit ):
						miniData = user.ntcon.recv(2)
						if ( miniData[0] == 'k' or miniData[0] == 'K' ):
							user.write('K')
							thisTower = 1
							thisMiniQuit = True
						elif ( miniData[0] == 's' or miniData[0] == 'S' ):
							user.write('S')
							thisTower = 2
							thisMiniQuit = True
						elif ( miniData[0] == 'c' or miniData[0] == 'C' ):
							user.write('C')
							thisTower = 3
							thisMiniQuit = True
						elif ( miniData[0] == 's' or miniData[0] == 'S' ):
							user.write('S')
							thisTower = 4
							thisMiniQuit = True
						elif ( miniData[0] == 'b' or miniData[0] == 'B' ):
							user.write('B')
							thisTower = 5
							thisMiniQuit = True
						else:
							pass
					user.write(user.art.tower())
					user.pause()
					if ( thisTower == random.randint(1, 5) ): # Correct Choice
						user.write("\r\n  \x1b[32mYou have choosen \x1b[1mwisely.\x1b[0m\r\n")
						user.write("  \x1b[32mElora gasps in suprise, saunters over, and thanks you 'properly'\r\n  \x1b[1mYou feel smarter, more gem laden, and -erm- 'satisfied'\x1b[0m\r\n")
						user.gems += 5
						user.gold += (user.level * 500)
					else: # WRONG
						if ( random.randint(1, 2) == 1 ): # REALLY, REALLY WRONG
							user.write("\r\n  \x1b[32mYou have choosen \x1b[1mpoorly.  really poorly.\x1b[0m\r\n\r\n")
							user.write("  \x1b[32mYou hear a strange groan and out pops Ken the Magnificent,\r\n  the disfigured midget (er, 'little person').\r\n  Sadly, 'little person' doesn't refer to all of him.\r\n\r\n  \x1b[1mYou feel terrible, both physically and mentally\x1b[0m\r\n")
							user.hp = 1
						else: # NOT SO BAD
							user.write("\r\n  \x1b[32mYou have choosen \x1b[1mpoorly.\x1b[0m\r\n")
							user.write("  \x1b[32mYou run like hell before anything bad happens.\x1b[0m\r\n")
					miniQuit = True
			user.pause()
		elif ( happening == 10 ): # lessons DKNIGHT GOOD, 
			if ( user.cls == 1 ):
				self.lesson_d()
			elif ( user.cls == 2 ):
				self.lesson_m()
			else:
				self.lesson_t()
			user.pause()
		elif ( happening == 11 ): # fairies
			self.fairies()
			user.pause()
		elif ( happening == 12 ): # darkhorse
			thismod = dht.dht()
			thismod.run(user)
			del thismod
		else:
			pass

	def fairies(self):
		user = self.user
		user.write(user.art.fairies())
		user.pause()
		user.write("  \x1b[32mYou glance at the fairies, trying to decide what to do.\r\n\r\n")
		user.write(func.normmenu("(A)sk for a Blessing"))
		user.write(func.normmenu("(T)ry and catch one"))
		miniQuit = False
		while ( not miniQuit ):
			user.write("\r\n  \x1b[0m\x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
			miniData = user.ntcon.recv(2)
			if ( miniData[0] == 'a' or miniData[0] == 'A' ):
				user.write('A')
				miniQuit = True
				blessingIs = random.randint(1, 4)
				if ( blessingIs == 4 and user.horse == True ):
					# Trap for already has a horse!
					blessingIs = 2
				if ( blessingIs == 1 ): # A Kiss
					user.write("\r\n\r\n  \x1b[32mYou recieve a kiss from Teesha and feel better!\x1b[0m\r\n\r\n")
					user.hp = user.hpmax
				elif ( blessingIs == 2 ): # Sad Stories
					user.write("\r\n\r\n  \x1b[32mThe fairies tell you sad stories.\r\n  \x1b[1mYou're tears turn into gems!\x1b[0m\r\n\r\b")
					user.gems += 2
				elif ( blessingIs == 3 ): # Fairy lore.
					user.write("\r\n\r\n  \x1b[32mThe fairies tell you secret fairly lore.\r\n  \x1b[1mYou feel smarter\x1b[0m\r\n\r\b")
					user.exp += ( user.level * 20 )
				elif ( blessingIs == 4 ): # The Horse
					user.write("\r\n\r\n  \x1b[32mThe fairys bless you with a new companion!\r\n  Please remember, horses are for riding, not, er... \x1b[1m*riding*\x1b[0m\r\n\r\n")
					user.horse = 1
				else:
					user.write("\r\n\r\n  \x1b[1;37mWTF?\x1b[0m\r\n\r\n")
			if ( miniData[0] == 't' or miniData[0] == 'T' ):
				user.write('T')
				miniQuit = True
				caughtIt = random.randint(1, 3)
				if ( caughtIt == 3 ):  # Grabbed One!
					user.write("\r\n\r\n  \x1b[32mYou managed to grab one!\r\n  You place it in your pocket for later.\x1b[0m\r\n")
					user.fairy = 1
				else:
					user.write("\r\n\r\n  \x1b[32mYou MISS!  And grab a thornberry bush instead!\x1b[0m\r\n")
					user.hp = 1
	
	def lesson_d(self) :
		""" Learn to be a death kniofht"""
		user = self.user
		user.write(user.art.line())
		user.write("\r\n  \x1b[32mYou come upon a group of warriors, they carry the look of a proud people.\x1b[0m\r\n")
		user.write("\r\n   \x1b[1;32mDeath Knight #1: \x1b[0;32mWe shall teach you the ways of the death knights weakling.\x1b[0m\r\n\r\n")
		user.write("   \x1b[1;32mDeath Knight #2: \x1b[0;32mAye.  But you must prove your wisdom first.\r\n                    This man is guilty of a crime.\x1b[0m\r\n\r\n")
		user.write("   \x1b[1;32mDeath Knight #1: \x1b[0;32mYup.  Or he's completely innocent.  Decide wisely.!\x1b[0m\r\n\r\n")
		user.write(func.normmenu("(K)ill Him"))
		user.write(func.normmenu("(F)ree him as an innocent"))
		user.write("\r\n  \x1b[0m\x1b[32mYour choice, \x1b[1m"+user.thisFullname+"\x1b[22m? (K,F) \x1b[0m\x1b[32m:-: \x1b[0m")
		miniQuit = False
		while ( not miniQuit ):
			data = user.ntcon.recv(2)
			if not data: break
			elif ( data[0] == 'k' or data[0] == 'K' ):
				user.write('K')
				user.write("\r\n  \x1b[32mYou draw your weapon, and ram it as hard as you can through his midsection.\x1b[0m\r\n")
				thisChoice = 1
				miniQuit = True
			elif ( data[0] == 'f' or data[0] == 'F' ):
				user.write('F')
				user.write("\r\n  \x1b[32mYou consider a moment, and shout \"Let him live!  He's done nothing wrong!\"\x1b[0m\r\n")
				thisChoice = 2
				miniQuit = True
	
		user.write("\r\n  \x1b[1;37m...")
		time.sleep(1)
		user.write("\x1b[31mAND\x1b[37m")
		time.sleep(1)
		user.write("...\x1b[0m")
		
		if ( thisChoice == random.randint(1,2) ):
			user.write("\r\n   \x1b[1;32mDeath Knight #1: \x1b[0;32mWell spotted young warrior.\r\n                    We shall teach you!\x1b[0m\r\n\r\n")
			user.write("  \x1b[32mYou recieve \x1b[1m1\x1b[0;32m use point")
			user.updateSkillUse(1, 1)
			user.hp = user.hpmax
			if ( user.getSkillPoint(1) < 40 ):
				user.updateSkillPoint(1, 1)
				user.write(" and \x1b[1m1\x1b[0;32m skill point")
			user.write(".\x1b[0m\r\n")
		else:
			user.write("\r\n   \x1b[1;32mDeath Knight #3: \x1b[0;32mOh god no!  That wasn't right at all!\r\n                    Somebody get a mop and a bandaid!\x1b[0m\r\n\r\n")
	
	def lesson_t(self) :
		""" LEarn to be a thief """
		user = self.user
		user.write(user.art.line())
		user.write("\r\n  \x1b[32mYou come upon a gathering of the theives guild, they kinda smell bad.\x1b[0m\r\n")
		user.write("\r\n   \x1b[1;32mThief #1: \x1b[0;32mWe can make you a better thief.  Just cost ya a gem.\x1b[0m\r\n")
		user.write(func.normmenu("(G)ive him the gem"))
		user.write(func.normmenu("(S)pit on him and walk away"))
		user.write(func.normmenu("(M)utter incoherantly, hoping he'll leave"))
		user.write("\r\n  \x1b[0m\x1b[32mYour choice, \x1b[1m"+user.thisFullname+"\x1b[22m? (G,S,M) \x1b[0m\x1b[32m:-: \x1b[0m")
		miniQuit = False
		while ( not miniQuit ):
			data = user.ntcon.recv(2)
			if not data: break
			elif ( data[0] == 's' or data[0] == 'S' ):
				user.write("S\r\n  \x1b[32mAs you spit on him, the thief looks at you closely.  He almost looks proud.\x1b[0m\r\n")
				miniQuit = True
			elif ( data[0] == 'm' or data[0] == 'M' ):
				user.write("M\r\n  \x1b[32mAs the thief leaves, you distincly hear the words \"nutjob\" and \"jackass\".  Oh well.\x1b[0m\r\n")
				miniQuit = True
			elif ( data[0] == 'g' or data[0] == 'G' ):
				user.write('G')
				if ( user.gems > 0 ):
					user.updateSkillUse(3, 1)
					user.write("\r\n  \x1b[32mYou recieve \x1b[1m1\x1b[0;32m use point")
					if ( user.getSkillPoint(3) < 40 ):
						user.updateSkillPoint(3, 1)
						user.write(" and \x1b[1m1\x1b[0;32m skill point")
					user.write(".\x1b[0m\n")
					user.gems -= 1
				else:
					user.write("\r\n  \x1b[1;32mThief #1: \x1b[0;32mYou don't have any gems dumbass.\x1b[0m\r\n")
				miniQuit = True
	
	def lesson_m(self) :
		""" Learn about magic """
		user = self.user
		user.write(user.art.line())
		user.write("\r\n  \x1b[32mYou come upon an old house.  You sense an old mage might live here.\x1b[0m\r\n")
		user.write(func.normmenu("(K)nock on the door"))
		user.write(func.normmenu("(B)ang on the door"))
		user.write(unc_normmenu("(L)eave"))
		user.write("\r\n  \x1b[0m\x1b[32mYour choice, \x1b[1m"+user.thisFullname+"\x1b[22m? (K,B,L) \x1b[0m\x1b[32m:-: \x1b[0m")
		miniQuit1 = False
		miniQuit2 = False
		
		while ( not miniQuit1 ):
			data = user.ntcon.recv(2)
			if not data: break
			elif ( data[0] == 'k' or data[0] == 'K' ):
				user.write(data[0])
				user.write("\r\n  \x1b[32mYou knock polietly on the door.\x1b[0m\n")
				miniQuit1 = True
			elif ( data[0] == 'b' or data[0] == 'B' ):
				user.write(data[0])
				user.write("\r\n  \x1b[32mYou bang wildly on the door.\x1b[0m\n")
				miniQuit1 = True
			elif ( data[0] == 'l' or data[0] == 'L' ):
				user.write("\n  \x1b[32mYou leave, confident in finding better things to do.\x1b[0m\n")
				miniQuit1 = True
				miniQuit2 = True
	
		if ( not miniQuit2 ):
			if ( random.randint(1, 5) == 2 ):
				user.write("\r\n  \x1b[32mNothing happens, and you leave.\x1b[0m\r\n")
			else:
				user.write("\r\n  \x1b[32mThe old man rips open the door and screams \"WHAT?!?\"\x1b[0m\r\n")
				user.write("  \x1b[32mHe then gazes at you and says \"I'll teach you magic if you can guess\r\n  the number I'm thinking of.  It's between 1 and 100\x1b[0m\r\n")
				magicNumber  = random.randint(1, 100)
				magicCorrect = False
				magicGuess   = 0
				while ( magicGuess < 7 ):
					user.write("\r\n  \x1b[0m\x1b[32mYour guess, \x1b[1m"+user.thisFullname+"\x1b[22m? \x1b[0m\x1b[32m:-: \x1b[0m")
					try: 
						thisGuess = int(func.getLine(user.ntcon, True))
					except ValueError:
						thisGuess = 1
					if ( thisGuess == magicNumber ):
						magicGuess = 7
						magicCorrect = True
					else:
						if ( thisGuess < magicNumber ):
							user.write("\r\n  \x1b[32mHigher!\x1b[0m\r\n")
						if ( thisGuess > magicNumber ):
							user.write("\r\n  \x1b[32mLower!\x1b[0m\r\n")
					magicGuess += 1
	
				if ( magicCorrect ):
					user.write("\r\n  \x1b[32mWell Done young mage!\x1b[0m\r\n")
					user.updateSkillUse(2, 1)
					user.write("  \x1b[32mYou recieve \x1b[1m1\x1b[0;32m use point")
					if ( user.getSkillPoint(2) < 40 ):
						user.updateSkillPoint(2, 1)
						user.write(" and \x1b[1m1\x1b[0;32m skill point")
					user.write(".\x1b[0m\r\n")
				else:
					user.write("\r\n  \x1b[32mBetter luck next time!\x1b[0m\r\n")

	def dragon(self):
		""" Forest Fight System """
		user = self.user
		user.write(user.art.lair())
		thisUserDefense = user.defence
		thisUserHit     = user.str / 2
		ctrlDead = False
		ctrlRan  = False
		ctrlWin  = False
		thisEnemyHit    = 2000
		thisEnemyHP     = 15000
		thisEnemyName   = "The Red Dragon"
		thisEnemyWeapon = "Set Later."
		
		user.write("\r\n\r\n  \x1b[32m**\x1b[1;37mFIGHT\x1b[0m\x1b[32m**\r\n")
		user.write("\r\n  \x1b[32mYou have encountered "+thisEnemyName+"!!\x1b[0m\r\n")
	
		user.write("\r\n  \x1b[32mYour skill allows you to get the first strike.\x1b[0m\r\n")
	
		skipDisp = False
		while ( user.hp > 0 and thisEnemyHP > 0 and not ctrlDead and not ctrlRan ): # FIGHT LOOP
			if ( not skipDisp ):
				user.write(self.dmenu(user, thisEnemyHP, thisEnemyName))
			hisType = random.randint(1, 7)
			if ( hisType == 1 or hisType == 2 ):
				thisEnemyWeapon = "Huge Fucking Claws"
				thisEnemyHit = 2100
			elif ( hisType == 3 or hisType == 4 ):
				thisEnemyWeapon = "Swishing Tail"
				thisEnemyHit = 1800
			elif ( hisType == 5 or hisType == 6 ):
				thisEnemyWeapon = "Stomping the Ground"
				thisEnemyHit = 1500
			else:
				thisEnemyWeapon = "Flaming Breath"
				thisEnemyHit = 3000
			skipDisp = False
			data = user.ntcon.recv(2)
			if not data: break
			elif ( data[0] == 's' or data[0] == 'S' ):
				user.write('S')
				user.write(util.viewstats(user))
			elif ( data[0] == 'a' or data[0] == 'A' ): # Attack!
				user.write("A\r\n")
				hisAttack = ( thisEnemyHit + random.randint(500, thisEnemyHit)) - thisUserDefense
				myAttack  = ( thisUserHit + random.randint(0, thisUserHit))
				if ( True ): # We Hit First
					if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
						hisAttack = 0
				if ( hisAttack >= user.hp ): # We are dead.  Bummer.
					ctrlDead = True
					hisAttack = user.hp # No insult to injury
				if ( hisAttack > 0 ): # He hit us
					user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
					user.hp -= hisAttack
				else: 
					user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely\x1b[0m\r\n")
				if ( myAttack > 0 and not ctrlDead ): # We hit him!
					user.write("\r\n  \x1b[32mYou hit "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
					thisEnemyHP = thisEnemyHP - myAttack
					if ( thisEnemyHP < 1 ): # We Win!
						ctrlWin = True
			elif ( data[0] == 'd' or data[0] == 'D' ): # Attack!
				user.write("D\r\n")
				if ( user.getSkillUse(1) > 0 ):
					user.updateSkillUse(1, -1)
					hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
					myAttack  = ( thisUserHit + (random.randint(2,5) * random.randint((thisUserHit / 2), thisUserHit))) + thisUserHit
					if ( True ): # We Hit First
						if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
							hisAttack = 0
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
						user.hp -= hisAttack
					else: 
						user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely\x1b[0m\r\n")
					if ( myAttack > 0 and not ctrlDead ): # We hit him!
						user.write("\r\n  \x1b[1;32mUltra Powerful Move!\x1b[0m\r\n  \x1b[32mYou hit "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
						thisEnemyHP = thisEnemyHP - myAttack
						if ( thisEnemyHP < 1 ): # We Win!
							ctrlWin = True
				else:
					user.write("\r\n  \x1b[32mYou have no Death Knight Skill Use Points!\x1b[0m\r\n\r\n")
			elif ( data[0] == 't' or data[0] == 'T' ): # Attack!
				user.write("T\r\n")
				if ( user.getSkillUse(3) > 0 ):
					user.updateSkillUse(3, -1)
					hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - ( thisUserDefense * 2 )
					myAttack  = ( thisUserHit + (random.randint(1,3) * random.randint((thisUserHit / 2), thisUserHit))) + thisUserHit
					if ( True ): # We Hit First
						if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
							hisAttack = 0
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
						user.hp -= hisAttack
					else: 
						user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely\x1b[0m\r\n")
					if ( myAttack > 0 and not ctrlDead ): # We hit him!
						user.write("\r\n  \x1b[1;32mUltra Sneaky Move!\x1b[0m\r\n  \x1b[32mYou hit "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
						thisEnemyHP = thisEnemyHP - myAttack
						if ( thisEnemyHP < 1 ): # We Win!
							ctrlWin = True
				else:
					user.write("\r\n  \x1b[32mYou have no Thief Skill Use Points!\x1b[0m\r\n\r\n")
			elif ( data[0] == 'r' or data[0] == 'R' ): # Run Away
				if ( random.randint(1, 10) == 4 ): # Hit in the back.
					hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
					if ( hisAttack >= user.hp ): # We are dead.  Bummer.
						ctrlDead = True
						hisAttack = user.hp # No insult to injury
					if ( hisAttack > 0 ): # He hit us
						user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you in the back with it's "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\r\n")
						user.hp -= hisAttack
						ctrlRan = True
				else:
					user.write("\r\n  \x1b[32mYou narrowly escape harm.\x1b[0m\r\n")
					ctrlRan = True
			elif ( data[0] == 'q' or data[0] == 'Q' ):
				user.write("\r\n  \x1b[31mYou are in Combat!  Try Running!\x1b[0m\r\n")
			elif ( data[0] == 'h' or data[0] == 'H' ):
				user.write("\r\n  \x1b[32mYou are in combat, and they don't make house calls!\x1b[0m\r\n")
			elif ( data[0] == 'l' or data[0] == 'L' ):
				user.write("\r\n  \x1b[32mWhat?!  You want to fight two at once?\x1b[0m\r\n")
			elif ( data[0] == 'm' or data[0] == 'M' ): #Magic!
				if ( user.getSkillUse(2) < 1 ):
					user.write("\r\n  \x1b[32mYou have no Magical Use Points!\x1b[0m\r\n\r\n")
				else:
					user.write("\r\n" + func.normmenu("(N)evermind") + func.normmenu("(P)inch Real Hard (1)"))
					if ( user.getSkillUse(2) > 3 ):
						user.write(func.normmenu("(D)isappear (4)"))
						if ( user.getSkillUse(2) > 7 ):
							user.write(func.normmenu("(H)eat Wave (8)"))
							if ( user.getSkillUse(2) > 11 ):
								user.write(func.normmenu("(L)ight Shield (12)"))
								if ( user.getSkillUse(2) > 15 ):
									user.write(func.normmenu("(S)hatter (16)"))
									if ( user.getSkillUse(2) > 19 ):
										user.write(func.normmenu("(M)ind Heal (20)"))
					user.write("\r\n  \x1b[32mYour command, \x1b[1m"+user.thisFullname+"\x1b[22m? [\x1b[1;35mA\x1b[0m\x1b[32m] : \x1b[0m")
					tinyQuit = False
					while ( not tinyQuit ):
						miniData = user.ntcon.recv(2)
						if not miniData: break
						elif ( miniData[0] == 'n' or miniData[0] == 'N' ): #Nothing
							user.write("N\r\n  \x1b[32mSure thing boss.\x1b[0m\r\n")
							tinyQuit = True
						elif ( miniData[0] == 'p' or miniData[0] == 'P' ): #Pinch!
							user.write("P")
							user.updateSkillUse(2, -1)
							tinyQuit = True
							hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
							myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + ( thisUserHit / 4 )
							if ( True ): # We Hit First
								if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely\x1b[0m\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  \x1b[32mYou pinch "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
								thisEnemyHP = thisEnemyHP - myAttack
								if ( thisEnemyHP < 1 ): # We Win!
									ctrlWin = True
						elif ( (miniData[0] == 'd' or miniData[0] == 'D') and ( user.getSkillUse(2) > 3 ) ): #Disappear
							user.write("D\r\n  \x1b[32mYou disapper like a ghost!\x1b[0m\r\n")
							user.updateSkillUse(2, -4)
							tinyQuit = True
							ctrlRan = True
						elif ( (miniData[0] == 'h' or miniData[0] == 'H') and ( user.getSkillUse(2) > 7 ) ): #Heat Wave
							user.write("H")
							user.updateSkillUse(2, -8)
							tinyQuit = True
							hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
							myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + (thisUserHit / 2)
							if ( True ): # We Hit First
								if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely\x1b[0m\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  \x1b[32mYou blast "+thisEnemyName+" with Heat Wave for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
								thisEnemyHP = thisEnemyHP - myAttack
								if ( thisEnemyHP < 1 ): # We Win!
									ctrlWin = True
						elif ( (miniData[0] == 'l' or miniData[0] == 'L') and ( user.getSkillUse(2) > 11 ) ): #Light Shield
							user.write("L\r\n  \x1b[32mYou feel a bit odd.  You dig in a feel better defended\x1b[0m\r\n")
							user.updateSkillUse(2, -12)
							thisUserDefense = thisUserDefense * 2
							tinyQuit = True
						elif ( (miniData[0] == 's' or miniData[0] == 'S') and ( user.getSkillUse(2) > 15 ) ): #Shatter
							user.write("S")
							user.updateSkillUse(2, -16)
							tinyQuit = True
							hisAttack = ( thisEnemyHit + random.randint(0, thisEnemyHit)) - thisUserDefense
							myAttack  = ( thisUserHit + random.randint(0, thisUserHit)) + (thisUserHit * 2)
							if ( not thisUnderdog ): # We Hit First
								if ( myAttack >= thisEnemyHP ): # If he's dead, he didn't hit us at all
									hisAttack = 0
							if ( hisAttack >= user.hp ): # We are dead.  Bummer.
								ctrlDead = True
								hisAttack = user.hp # No insult to injury
							if ( hisAttack > 0 ): # He hit us
								user.write("\r\n  \x1b[32m"+thisEnemyName+" hits you with "+thisEnemyWeapon+" for \x1b[1;31m"+str(hisAttack)+"\x1b[0m\x1b[32m damage\x1b[0m\r\n")
								user.hp -= hisAttack
							else: 
								user.write("\r\n  \x1b[32m"+thisEnemyName+" misses you completely\x1b[0m\r\n")
							if ( myAttack > 0 and not ctrlDead ): # We hit him!
								user.write("\r\n  \x1b[32mYou Shatter "+thisEnemyName+" for \x1b[1;31m"+str(myAttack)+"\x1b[0m\x1b[32m damage\r\n")
								thisEnemyHP = thisEnemyHP - myAttack
								if ( thisEnemyHP < 1 ): # We Win!
									ctrlWin = True
						elif ( (miniData[0] == 'm' or miniData[0] == 'M') and ( user.getSkillUse(2) > 19 ) ): #Mind Heal
							user.write("M\r\n  \x1b[32mYou feel much better!\x1b[0m\r\n")
							user.updateSkillUse(2, -20)
							hptoadd = user.hpmax - user.hp
							user.hp = user.hpmax
							if ( hptoadd < 5 ):
								user.write("\r\n  \x1b[32mEven though you are clearly a fuck-tard...\x1b[0m\r\n")
							tinyQuit = True
			else: #Catch non-options
				skipDisp = True
	
		if ( ctrlWin ) :
			user.gold = 500
			user.bank = 0
			user.str = 10
			user.defence = 1
			user.level = 1
			user.exp = 1
			user.dragon += 1
			user.ffight = user.config.ffights
			user.pfight = user.config.pfights
			user.hp = 20
			user.hpmax = 20
			user.gems = 10
			user.weapon = 1
			user.armor = 1
			
			lamentThis = "{32}{1}"+user.thisFullname+" {0}{32}Decimated {0}{31}{1}The Red Dragon!!! {0}{32}Rejoice!!!{0}"
			user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (lamentThis,))
			user.dbcon.commit()
			user.write(func.casebold("\r\n\r\n  You have defeated the Dragon, and saved the town.  Your stomach\r\n", 2))
			user.write(func.casebold("\x1b[32m  churns at the site of stacks of clean white bones - Bones of small\r\n", 2))
			user.write(func.casebold("\x1b[32m  children.\r\n\r\n", 2))
			user.write(func.casebold("  THANKS TO YOU, THE HORROR HAS ENDED!\r\n\r\n", 2))
			user.pause()
			for myline in data.endstory[user.cls]:
				user.write("\x1b[32m"+myline+"\x1b[0m\r\n")
			user.pause()
			user.write(func.casebold("                  ** YOUR QUEST IS NOT OVER **\r\n\r\n", 2))
			user.write(func.casebold("  You are a hero.  Bards will sing of your deeds, but that doesn't\r\n", 2))
			user.write(func.casebold("\x1b[32m  mean your life doesn't go on.\r\n", 2))
			user.write(func.casebold("  YOUR CHARACTER WILL NOW BE RESET.  But you will keep a few things\r\n", 2))
			user.write(func.casebold("\x1b[32m  you have earned.  Like the following.\r\n", 2))
			user.write(func.casebold("  ALL SPECIAL SKILLS.\r\n  CHARM.\r\n  A FEW OTHER THINGS.\r\n", 2))			
			user.pause()
			
		if ( ctrlDead ) :
			if ( user.fairy == True ):
				user.hp = 1
				user.fairy = 0
				user.write(func.casebold("  Miraculously, your fairy saves you from the edge of defeat.  You escape with your life.\r\n", 2))
			else:
				user.alive = 0
				#exception handles, do it later. user.logout()
				lamentThis = "{31}{1}The Red Dragon{0}{32} Decimated "+user.thisFullname+"{0}"
				user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (lamentThis,))
				user.dbcon.commit()
				user.write(func.casebold("\r\n\r\n  The Dragon pauses to look at you, then snorts in a Dragon laugh, and\r\n", 1))
				user.write(func.casebold("\x1b[31m  delicately rips your head off, with the finess only a Dragon well\r\n", 1))
				user.write(func.casebold("\x1b[31m  practiced in the art could do.\r\n", 1))
				raise Exception('normal', "User is DOA.  Bummer.")
	
