#!/usr/bin/python
"""
 * Module System
 * 
 * Contains modules for everything except the Inn and the Fighting system.
 * 
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage
"""
import random
from functions import *
from data import *
from menus import *
from forest import forest_special, forest_fight

def module_newuser(user):
	"""Create a user"""
	user.write(func_casebold("\r\nCreating a New Character...\r\n", 2))
	thisLooper = False
	while ( not thisLooper ):
		user.write(func_casebold("\r\nPlease Choose a Username (12 characters MAX) :-: ", 2))
		newname = func_getLine(user.connection, True)
		newname = newname[:12]
		if ( user.userLoginExist(newname) ):
			user.write(func_casebold("\r\nName In Use!\r\n", 1))
		else:
			thisLooper = True
	thisLooper = False
	while ( not thisLooper ):
		user.write(func_casebold("\r\nAnd, how will you be addressed? (a Handle) (40 characters MAX) :-: ", 2))
		newfname = func_getLine(user.connection, True)
		newfname = newfname[:40]
		if ( newfname == "" ):
			user.write(func_casebold("\r\nHEY! No Anonymous Players!\r\n", 1))
		else:
			thisLooper = True
	thisLooper = False
	while ( not thisLooper ):
		user.write(casebold("\r\nPick a Password (12 characters MAX) :-: ", 2))
		newpass = func_getLine(user.connection, True)
		newpass = newpass[:12]
		if ( newpass == "" ):
			user.write(func_casebold("\r\nPassword MUST Not Be Empty\r\n", 1))
		else:
			thisLooper = True
	thisLooper = False
	while ( not thisLooper ):
		user.write(func_casebold("\r\nYour Sex (M/F) :-: ", 2))
		data = user.connection.recv(2)
		if not data: break
		if ( data[0] == 'm' or data[0] == 'M' ):
			user.write('M')
			newsexnum = 1
			thisLooper = True
			user.write(func_casebold("\r\nMy, what a girly man you are...\r\n", 2))
		if ( data[0] == 'f' or data[0] == 'F' ):
			user.write('F')
			newsexnum = 2
			thisLooper = True
			user.write(func_casebold("Gee sweetheart, hope you don't break a nail...\n", 2))
	user.write(func_casebold("\r\nPick that which best describes your childhood.\nFrom an early age, you remember:\r\n\r\n", 2))
	user.write(func_normmenu("(D)abbling in the mystical forces"))
	user.write(func_normmenu("(K)illing a lot of woodland creatures"))
	user.write(func_normmenu("(L)ying, cheating, and stealing from the blind"))
	thisLooper = False
	while ( not thisLooper ):
		user.write(func_casebold("\r\nYour Choice (D/K/L) :-: ", 2))
		data = user.connection.recv(2)
		if not data: break
		if ( data[0] == 'k' or data[0] == 'K' ):
			user.write('K')
			newclassnum = 1
			thisLooper = True
			user.write(func_casebold("\r\nWelcome warrior to the ranks of the Death Knights!\n", 2))
		if ( data[0] == 'd' or data[0] == 'D' ):
			user.write('D')
			newclassnum = 2
			thisLooper = True
			user.write(func_casebold("\r\nFeel the force young jedi.!\n", 2))
		if ( data[0] == 'l' or data[0] == 'L' ):
			user.write('L')
			newclassnum = 3
			thisLooper = True
			user.write(func_casebold("\r\nYou're a real shitheel, you know that?\n", 2))
	thisSQL = "INSERT INTO "+user.thisSord.sqlPrefix()+"users (`username`, `password`, `fullname`) VALUES ('"+newname+"', '"+newpass+"', '"+newfname+"')"
	user.db.execute(thisSQL)
	thisUserID = user.dbc.insert_id()
	thisSQL = "INSERT INTO "+user.thisSord.sqlPrefix()+"stats (`userid`, `sex`, `class`) VALUES ("+str(thisUserID)+", "+str(newsexnum)+", "+str(newclassnum)+")"
	user.db.execute(thisSQL)
	return newname
	

def module_finduser(user, prompter):
	"""Find a user"""
	user.write(prompter + " \x1b[1;32m:\x1b[0;32m-\x1b[1;32m:\x1b[0m ")
	name = func_getLine(user.connection, True)
	returnID = user.userExist(name)
	if ( returnID > 0 ) :
		if ( returnID == user.thisUserID ):
			user.write(func_casebold("\r\n  Masturbation is gross...\r\n", 1))
			return 0
		else:
			user.write("\r\n  \x1b[32mDid you mean \x1b[1m" + user.userGetName(returnID) +"\x1b[0m \x1b[1;30m(Y/N)\x1b[0m\x1b[32m ?\x1b[0m ")
			yesno = user.connection.recv(2)
			if ( yesno[0] == "Y" or yesno[0] == "y" ):
				return returnID
			else:
				return 0
	else:
		return 0


def module_viewstats(user):
	""" View Player Stats
	* @param int $userid User ID
	* @return string Formatted output for display"""
	output  = "\r\n\r\n\x1b[1m\x1b[37m"+user.thisFullname+"\x1b[0m\x1b[32m's Stats...\r\n"
	output += user.art.line()
	output += "\x1b[32m Experience    : \x1b[1m"+str(user.getExperience())+"\x1b[0m\r\n"
	output += "\x1b[32m Level         : \x1b[1m"+str(user.getLevel())+"\x1b[0m" + padnumcol(str(user.getLevel()), 20) + "\x1b[32mHitPoints          : \x1b[1m"+str(user.getHP())+" \x1b[22mof\x1b[1m "+str(user.getHPMax())+"\x1b[0m\r\n"
	output += "\x1b[32m Forest Fights : \x1b[1m"+str(user.getForestFight())+"\x1b[0m" + padnumcol(str(user.getForestFight()), 20) + "\x1b[32mPlayer Fights Left : \x1b[1m"+str(user.getPlayerFight())+"\x1b[0m\r\n"
	output += "\x1b[32m Gold In Hand  : \x1b[1m"+str(user.getGold())+"\x1b[0m" + padnumcol(str(user.getGold()), 20) + "\x1b[32mGold In Bank       : \x1b[1m"+str(user.getBank())+"\x1b[0m\r\n"
	output += "\x1b[32m Weapon        : \x1b[1m"+weapon[user.getWeapon()]+"\x1b[0m" + padnumcol(weapon[user.getWeapon()], 20) + "\x1b[32mAttack Strength    : \x1b[1m"+str(user.getStrength())+"\x1b[0m\r\n"
	output += "\x1b[32m Armor         : \x1b[1m"+armor[user.getArmor()]+"\x1b[0m" + padnumcol(armor[user.getArmor()], 20) + "\x1b[32mDefensive Strength : \x1b[1m"+str(user.getDefense())+"\x1b[0m\r\n"
	output += "\x1b[32m Charm         : \x1b[1m"+str(user.getCharm())+"\x1b[0m" + padnumcol(str(user.getCharm()), 20) + "\x1b[32mGems               : \x1b[1m"+str(user.getGems())+"\x1b[0m\r\n\r\n"
	for skillnum in [1,2,3]:
		if ( user.getClass() == skillnum or user.getSkillPoint(skillnum) > 0 ):
			output += "\x1b[32m The "+classes[skillnum]+" Skills: \x1b[1m"
			if ( user.getSkillUse(skillnum) > 0 ):
				output +=  str(user.getSkillPoint(skillnum)) + padnumcol(str(user.getSkillPoint(skillnum)), 11)
			else:
				output += "NONE     "
			output += padnumcol(classes[skillnum], 12)
			output += "\x1b[0m\x1b[32mUses Today: (\x1b[1m"+str(user.getSkillUse(skillnum))+"\x1b[22m)\x1b[0m\r\n"
	output += "\r\n \x1b[1;32mYou are currently interested in \x1b[37mThe "+classes[user.getClass()]+" \x1b[32mskills.\r\n\r\n";
	return output

def module_dailyhappen(noprmpt, db, prefix):
	""" View Daily Happenings
	* @param bool $noprmpt Do not prompt for additions.
	* @return string Formatted output for display """
	thisSQL = "SELECT data FROM (SELECT * FROM "+prefix+"daily ORDER BY id DESC LIMIT 10) AS tbl ORDER BY tbl.id"
	db.execute(thisSQL)
	output  = "\r\n\r\n\x1b[1;37mRecent Happenings\033[22;32m....\x1b[0m\r\n"
	output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	for line in db.fetchall():
		output += "    " + func_colorcode(line[0])
		output += "\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	if ( not noprmpt ) :
		output +=  "\n\x1b[32m(\x1b[1;35mC\x1b[22;32m)ontinue  \x1b[32m(\x1b[1;35mT\x1b[22;32m)odays happenings again  \x1b[1;32m[\x1b[35mC\x1b[32m] \x1b[22m:-: "
	return output

def module_who(art, db, prefix):
	""" Who's Online
	* @return string Formatted output for display"""
	thisSQL = "SELECT o.userid, fullname, DATE_FORMAT(whence, '%H:%i') as whence FROM "+prefix+"users u, "+prefix+"online o WHERE o.userid = u.userid ORDER BY whence ASC"
	db.execute(thisSQL)
	output  = "\r\n\r\n\x1b[1;37m                     Warriors In The Realm Now\x1b[22;32m\x1b[0m\r\n"
	output += art.line()
	for line in db.fetchall():
		output += "  \x1b[1;32m" + line[1] + padnumcol(line[1], 28)
		output += "\x1b[0m\x1b[32mArrived At                    \x1b[1;37m" + line[2] + "\x1b[0m\r\n"
	return output + "\r\n"

def module_list(art, db, prefix):
	""" Player List
	* @return string Formatted output for display """
	thisSQL = "SELECT u.userid, fullname, exp, level, class, spclm, spcld, spclt, sex, alive FROM "+prefix+"users u, "+prefix+"stats s WHERE u.userid = s.userid ORDER BY exp DESC"
	db.execute(thisSQL)
	output = "\r\n\r\n\x1b[32m    Name                    Experience    Level    Mastered    Status\x1b[0m\r\n";
	output += art.line()
	for line in db.fetchall():
		if ( line[8] == 2 ):
			lineSex = "\x1b[1;35mF\x1b[0m "
		else:
			lineSex = "  "
			
		if ( line[4] == 1 ):
			lineClass = "\x1b[1;31mD \x1b[0m"
		elif ( line[4] == 2 ):
			lineClass = "\x1b[1;31mM \x1b[0m"
		else:
			lineClass = "\x1b[1;31mT \x1b[0m"
		
		lineMaster = ""
		if ( line[6] > 19 ):
			if ( line[6] > 39 ):
				lineMaster += "\x1b[1;37mD \x1b[0m"
			else:
				lineMaster += "\x1b[37mD \x1b[0m"
		else:
			lineMaster += "  "
			
		if ( line[5] > 19 ):
			if ( line[5] > 39 ):
				lineMaster += "\x1b[1;37mM \x1b[0m"
			else:
				lineMaster += "\x1b[37mM \x1b[0m"
		else:
			lineMaster += "  "
						
		if ( line[7] > 19 ):
			if ( line[7] > 39 ):
				lineMaster += "\x1b[1;37mT \x1b[0m"
			else:
				lineMaster += "\x1b[37mT \x1b[0m"
		else:
			lineMaster += "  "
									
		
		if ( line[9] == 1 ):
			lineStatus = "\x1b[1;32mAlive\x1b[0m"
		else:
			lineStatus = "\x1b[31mDead\x1b[0m"
			
		output += lineSex + lineClass + "\x1b[32m" + line[1] + padnumcol(str(line[1]), 23) + padright(str(line[2]), 11)
		output += padright(str(line[3]), 6) + "        " + lineMaster + padnumcol(lineMaster, 12) + lineStatus + "\r\n"
	return output + "\r\n"

def module_heal(user):
	""" Healers Hut Logic """
	thisQuit = False
	while ( not thisQuit ):
		user.write(menu_heal(user))
		data = user.connection.recv(2)
		if not data: break
		if ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			user.write('R')
			thisQuit = True
		if ( data[0] == 'h' or data[0] == 'H' ):
			user.write('H')
			hptoheal = user.getHPMax() - user.getHP()
			if ( hptoheal < 1 ):
				user.write(func_casebold("\r\n  You do NOT need healing!\r\n", 2))
			else:
				perhpgold = user.getLevel() * 5
				usergold = user.getGold()
				if ( usergold < perhpgold ):
					user.write(func_casebold("\r\n  You are too poor to heal anything!\r\n)", 2))
				else:
					fullcosttoheal = hptoheal * perhpgold
					canaffordtoheal =  ( usergold - ( usergold % perhpgold ) ) / perhpgold
					if ( canaffordtoheal >= hptoheal ):
						canaffordtoheal = hptoheal
					user.updateGold((canaffordtoheal * perhpgold) * -1)
					user.updateHP(canaffordtoheal)
					user.write("\r\n  \x1b[32m\x1b[1m"+str(canaffordtoheal)+" \x1b[22mHitPoints are healed and you feel much better!\x1b[0m\r\n")
 					user.pause()
		if ( data[0] == 'c' or data[0] == 'C' ):
			user.write('C')
			hptoheal = user.getHPMax() - user.getHP()
			if ( hptoheal < 1 ):
				user.write(func_casebold("\r\n  You do NOT need healing!\r\n", 2))
			else:
				user.write("\r\n  \x1b[32mHow much to heal warror? \x1b[1m: \x1b[0m")
				try:
					number = int(func_getLine(user.connection, True))
				except ValueError:
					number = 0
				if ( number > hptoheal ):
					number = hptoheal
				if ( number > 0 ):
					perhpgold = user.getLevel() * 5
					costforaction = perhpgold * number
					if ( costforaction > user.getGold() ):
						user.write(func_casebold("\r\n  You do not have enough gold for that!\r\n", 1))
					else:
						user.updateGold(costforaction * -1)
						user.updateHP(number)
						user.write("\r\n  \x1b[32m\x1b[1m"+str(number)+" \x1b[22mHitPoints are healed and you feel much better!\x1b[0m\r\n")
						user.pause()

def module_forest(user):
	""" Forest Fight - Non-Combat """
	thisQuit = False
	while ( not thisQuit ):
		if ( not user.expert ):
			user.write(user.art.forest())
		user.write(menu_forest(user))
		data = user.connection.recv(2)
		if ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			user.write('Q')
			thisQuit = True
		if ( data[0] == '?' ):
			user.write('?')
			if ( user.expert ):
				user.write(user.art.forest())
		if ( data[0] == 'h' or data[0] == 'H' ):
			user.write('H')
			module_heal(user)
		if ( data[0] == 'v' or data[0] == 'V' or data[0] == 'y' or data[0] == 'Y' ):
			module_viewstats(user)
		if ( data[0] == 'l' or data[0] == 'l' ):
			user.write("L\r\n")
			if ( user.getForestFight() > 0 ):
				if ( random.randint(1, 8) == 3 ):
					forest_special(user)
				else:
					forest_fight(user)
			else:
				user.write(func_casebold("\r\n  You are mighty tired.  Try again tommorow\r\n", 2))
		if ( data[0] == 'a' or data[0] == 'A' ):
			user.write('A')
			user.write(func_casebold("\r\n  You brandish your weapon dramatically.\r\n", 2))
		if ( data[0] == 'd' or data[0] == 'D' ):
			user.write('D')
			user.write(func_casebold("\r\n  Your Death Knight skills cannot help your here.\r\n", 2))
		if ( data[0] == 'm' or data[0] == 'M' ):
			user.write('M')
			user.write(func_casebold("\r\n  Your Mystical skills cannot help your here.\r\n", 2))
		if ( data[0] == 't' or data[0] == 'T' ):
			user.write('T')
			user.write(func_casebold("\r\n  Your Thieving skills cannot help your here.\r\n", 2))

def module_bank(user):
	""" Ye Olde Bank """
	thisQuit = False
	while ( not thisQuit ):
		user.write(menu_bank(user))
		data = user.connection.recv(2)
		if not data: break
		if ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
			user.write('Q')
			thisQuit = True
		if ( data[0] == 'd' or data[0] == 'D' ):
			user.write('D')
			user.write("\r\n  \x1b[32mDeposit how much? \x1b[1;30m(1 for all) \x1b[1;32m:\x1b[0m ")
			try:
				number = int(func_getLine(user.connection, True))
			except ValueError:
				number = 0
			if ( number > user.getGold() ):
				user.write(func_casebold("\r\n  You don't have that much gold!\r\n", 1))
				user.pause()
			elif ( number > 0 ):
				if ( number == 1 ):
					number = user.getGold()
				user.updateBank(number)
				user.updateGold(number * -1)
				user.write(func_casebold("\r\n  Gold deposited\r\n", 2))
				user.pause()
			else:
				pass
		if ( data[0] == 'w' or data[0] == 'W' ):
			user.write('W')
			user.write("\r\n  \x1b[32mWithdraw how much? \x1b[1;30m(1 for all) \x1b[1;32m:\x1b[0m ")
			try:
				number = int(func_getLine(user.connection, True))
			except ValueError:
				number = 0
			if ( number > user.getBank() ):
				user.write(func_casebold("\r\n  You don't have that much gold in the bank!\r\n", 1))
				user.pause()
			elif ( number > 0 ):
				if ( number == 1 ):
					number = user.getBank()
				user.updateGold(number)
				user.updateBank(number * -1)
				user.write(func_casebold("\r\n  Gold widthdrawn\r\n", 2))
				user.pause()
			else:
				pass
		if ( data[0] == 't' or data[0] == 'T' ):
			user.write('T')
			touser = module_finduser(user, "\r\n  \x1b[32mTransfer to which player? \x1b[1;32m:\x1b[0m ")
			if ( touser > 0 ):
				user.write("\r\n  \x1b[32mTransfer how much? \x1b[1;32m:\x1b[0m ")
				try:
					number = int(func_getLine(user.connection, True))
				except ValueError:
					number = 0
				if ( number > user.getGold() ):
					user.write(func_casebold("\r\n  You don't have that much gold!\r\n", 1))
					user.pause()
				elif ( number > 0 ):
					thisSQL = "UPDATE "+user.thisSord.sqlPrefix()+"stats SET gold = (gold + "+str(number)+") WHERE userid = "+str(touser)
					user.db.execute(thisSQL)
					user.updateGold(number * -1)
					user.write(func_casebold("\r\n  Gold transfered\r\n", 2))
					user.pause()
				else:
					user.write(func_casebold("\r\n Cheap Ass!\r\n", 2))
			else:
				user.write(func_casebold("\r\n  No user by that name found!\r\n", 1))
				user.pause()

def module_abduls(user):
	""" Abdul's Armor"""
	thisQuit = False
	while ( not thisQuit ):
 		if ( not user.expert ):
			user.write(user.art.abdul())
		user.write(menu_abdul(user))
		data = user.connection.recv(2)
		if not data: break
		if ( data[0] == 'b' or data[0] == 'B' ):
			user.write('B')
			user.write(user.art.armbuy())
			user.write("\r\n\r\n\x1b[32mYour choice? \x1b[1m:\x1b[22m-\x1b[1m:\x1b[0m ")
			try:
				number = int(func_getLine(user.connection, True))
			except ValueError:
				number = 0
			if ( number > 0 and number < 16 ):
				if ( user.getArmor() > 0 ):
					user.write(func_casebold("\r\nYou cannot hold 2 sets of Armor!\r\n", 1))
					user.pause()
				else:
					if ( user.getGold() < armorprice[number] ):
						user.write(func_casebold("\r\nYou do NOT have enough Gold!\n", 1))
						user.pause()
					else:
						if ( user.getDefense() < armorndef[number] ):
							user.write(func_casebold("\r\nYou are NOT strong enough for that!\r\n", 1))
							user.pause()
						else:
							user.write(func_casebold("\r\nI'll sell you my Best "+armor[number]+" for "+str(armorprice[number])+" gold.  OK? ", 2)) 
							yesno = user.connection.recv(2)
							if not yesno: break
							if ( yesno[0] == "Y" or yesno[0] == "y" ):
								user.write('Y')
								user.setArmor(number)
								user.updateGold(armorprice[number] * -1)
								user.updateDefense(armordef[number])
								user.write(func_casebold("\r\nPleasure doing business with you!\r\n", 2))
								user.pause()
							else:
								user.write(func_casebold("\r\nFine then...\r\n", 2))
								user.pause()
		if ( data[0] == 's' or data[0] == 'S' ):
			user.write('S')
			sellpercent = 50 + random.randint(1, 10)
			sellarmor = user.getArmor()
			if ( sellarmor > 0 ):
				sellprice = ((sellpercent * armorprice[sellarmor]) // 100 )
				user.write(func_casebold("\r\nHmm...  I'll buy that "+armor[sellarmor]+" for "+str(sellprice)+" gold.  OK? ", 2))
				yesno = user.connection.recv(2)
				if not yesno: break
				if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
					user.write('Y')
					user.setArmour(0)
					user.updateGold(sellprice)
					unstrength = (60 * armordef[sellweapon]) // 100
					user.updateDefense(unstrength * -1)
					user.write(func_casebold("\r\nPleasure doing business with you!\r\n", 2))
					user.pause()
				else:
					user.write(func_casebold("\r\nFine then...\r\n", 2))
					user.pause()
			else:
				user.write(func_casebold("\r\nYou have nothing I want!\r\n", 1))
				user.pause()
		if ( data[0] == "?" ):
			user.write('?')
			if ( user.expert ):
				user.write(user.art.abdul())
		if ( data[0] == 'Y' or data[0] == 'y' ):
			user.write('Y')
			user.write(module_viewstats(user))
			user.pause()
		if ( data[0] == 'Q' or data[0] == 'q' or data[0] == 'R' or data[0] == 'r' ):
			user.write('R')
			thisQuit = True;

def module_arthurs(user):
	"""King Arthur's Weapons"""
	thisQuit = False
	while ( not thisQuit ):
 		if ( not user.expert ):
			user.write(user.art.arthur())
		user.write(menu_arthur(user))
		data = user.connection.recv(2)
		if not data: break
		if ( data[0] == 'b' or data[0] == 'B' ):
			user.write('B')
			user.write(user.art.wepbuy())
			user.write("\r\n\r\n\x1b[32mYour choice? \x1b[1m:\x1b[22m-\x1b[1m:\x1b[0m ")
			try:
				number = int(func_getLine(user.connection, True))
			except ValueError:
				number = 0
			if ( number > 0 and number < 16 ):
				if ( user.getWeapon() > 0 ):
					user.write(func_casebold("\r\nYou cannot hold 2 Weapons!\r\n", 1))
					user.pause()
				else:
					if ( user.getGold() < weaponprice[number] ):
						user.write(func_casebold("\r\nYou do NOT have enough Gold!\n", 1))
						user.pause
					else:
						if ( user.getStrength() < weaponnstr[number] ):
							user.write(func_casebold("\r\nYou are NOT strong enough for that!\r\n", 1))
							user.pause()
						else:
							user.write(func_casebold("\r\nI'll sell you my Favorite "+weapon[number]+" for "+str(weaponprice[number])+" gold.  OK? ", 2)) 
							yesno = user.connection.recv(2)
							if not yesno: break
							if ( yesno[0] == "Y" or yesno[0] == "y" ):
								user.write('Y')
								user.setWeapon(number)
								user.updateGold(weaponprice[number] * -1)
								user.updateStrength(weaponstr[number])
								user.write(func_casebold("\r\nPleasure doing business with you!\r\n", 2))
								user.pause()
							else:
								user.write(func_casebold("\r\nFine then...\r\n", 2))
								user.pause()
		if ( data[0] == 's' or data[0] == 'S' ):
			user.write('S')
			sellpercent = 50 + random.randint(1, 10)
			sellweapon = user.getWeapon()
			if ( sellweapon > 0 ):
				sellprice = ((sellpercent * weaponprice[sellweapon]) // 100 )
				user.write(func_casebold("\r\nHmm...  I'll buy that "+weapon[sellweapon]+" for "+str(sellprice)+" gold.  OK? ", 2))
				yesno = user.connection.recv(2)
				if not yesno: break
				if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
					user.write('Y')
					user.setWeapon(0)
					user.updateGold(sellprice)
					unstrength = (60 * weaponstr[sellweapon]) // 100
					user.updateStrength(unstrength * -1)
					user.write(func_casebold("\r\nPleasure doing business with you!\r\n", 2))
					user.pause()
				else:
					user.write(func_casebold("\r\nFine then...\r\n", 2))
					user.pause()
			else:
				user.write(func_casebold("\r\nYou have nothing I want!\r\n", 1))
				user.pause()
		if ( data[0] == "?" ):
			user.write('?')
			if ( user.expert ):
				user.write(user.art.abdul())
		if ( data[0] == 'Y' or data[0] == 'y' ):
			user.write('Y')
			user.write(module_viewstats(user))
			user.pause()
		if ( data[0] == 'Q' or data[0] == 'q' or data[0] == 'R' or data[0] == 'r' ):
			user.write('R')
			thisQuit = True;
				

""" Turgon's Warrior Training (pre-combat)
 * 
 * Visit the master
 * 
 * @todo Implement the hall of honor (V)
 */
function module_turgon() {
	GLOBAL $db, $MYSQL_PREFIX, $masters, $userid;
	$quitter = 0;
	while ( !$quitter ) {
		slowecho(menu_turgon());
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
		switch ($choice) {
			case 'R': // QUIT
				$quitter = 1; break;
			case '?': // SHOW MENU
				break;
			case 'Q': // QUESTION MASTER
				$ulvl = user_getlevel($userid);
				$uexp = user_getexp($userid);
				$nexp = $masters[$ulvl][2] - $uexp;
				if ( $nexp < 0 ) { $nexp = 0; }
				foreach ( $masters[$ulvl][3] as $wisdom ) {
					slowecho("\n  \033[32m{$wisdom}\033[0m");
				}
				slowecho("\n\n  \033[1;37m{$masters[$ulvl][0]}\033[0m\033[32m looks at you closely and says...\n");
				if ( $nexp == 0 ) { slowecho("  \033[32m{$masters[$ulvl][4]}\033[0m\n"); }
				else { slowecho("  \033[32mYou need about \033[1;37m{$nexp}\033[0m\033[32m experience before you'll be as good as me.\033[0m\n"); }
				pauser();
				break;
			case 'V': // VIEW HALL OF HONOR
				control_noimp(); break;
			case 'Y': // VIEW STATS
				slowecho(module_viewstats($userid)); break;
			case 'A': // FIGHT MASTER
				if ( user_seenmaster($userid) ) { slowecho("\n\n  \033[32mI'm sorry my son, you may only fight me once per game-day\033[0m\n"); }
				else { master_fight(); }
				break;
		}
	}
}

/** Look at the forest flowers
 * 
 * Yet another in-game message board.
 *
 * @todo random sayings generator for this section
 */
function module_flowers() {
	GLOBAL $db, $MYSQL_PREFIX, $userid;
	$sql = "SELECT data, nombre FROM (SELECT * FROM {$MYSQL_PREFIX}flowers ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id";
	$result = mysql_query($sql, $db);
	$output = "\n\n  \033[1;37mStudy the forest flowers\033[22;32m....\033[0m\n";
	$output .= "\033[32m                                      -=-=-=-=-=-\033[0m\n";
	while ( $line = mysql_fetch_array($result) ) {
		$output .= "    \033[32m{$line['nombre']} \033[1;37msays... \033[0m\033[32m" . func_colorcode($line['data']);
		$output .= "\033[0m\n\033[32m                                      -=-=-=-=-=-\033[0m\n";
	}
	$output .= "\n  \033[32mAdd to the conversation? \033[1m: \033[0m";
	slowecho($output);
	$yesno = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	if ( $yesno == "Y" ) {
		slowecho(func_casebold("\n  What!?  What do you want? :-: ", 2));
		$ann = preg_replace("/\r\n/", "", chop(fgets(STDIN)));
		$insann = mysql_real_escape_string($ann);
		$insnme = user_gethandle($userid);
		$sql = "INSERT INTO {$MYSQL_PREFIX}flowers ( `data`, `nombre` ) VALUES ('{$insann}', '{$insnme}')";
		$result = mysql_query($sql, $db);
		slowecho(func_casebold("\n  Idiocy added!\n", 2));
		pauser();
	}
}
"""

