#!/usr/bin/python
"""
 * Contains utility displays
 *
"""
from ..base import func
from . import data

def viewstats(user):
	""" View Player Stats
	* @param int $userid User ID
	* @return string Formatted output for display"""
	output  = "\r\n\r\n\x1b[1m\x1b[37m"+user.thisFullname+"\x1b[0m\x1b[32m's Stats...\r\n"
	output += user.art.line()
	output += "\x1b[32m Experience    : \x1b[1m"+str(user.exp)+"\x1b[0m\r\n"
	output += "\x1b[32m Level         : \x1b[1m"+str(user.level)+"\x1b[0m" + func.padnumcol(str(user.level), 20) + "\x1b[32mHitPoints          : \x1b[1m"+str(user.hp)+" \x1b[22mof\x1b[1m "+str(user.hpmax)+"\x1b[0m\r\n"
	output += "\x1b[32m Forest Fights : \x1b[1m"+str(user.ffight)+"\x1b[0m" + func.padnumcol(str(user.ffight), 20) + "\x1b[32mPlayer Fights Left : \x1b[1m"+str(user.pfight)+"\x1b[0m\r\n"
	output += "\x1b[32m Gold In Hand  : \x1b[1m"+str(user.gold)+"\x1b[0m" + func.padnumcol(str(user.gold), 20) + "\x1b[32mGold In Bank       : \x1b[1m"+str(user.bank)+"\x1b[0m\r\n"
	output += "\x1b[32m Weapon        : \x1b[1m"+data.weapon[user.weapon]+"\x1b[0m" + func.padnumcol(data.weapon[user.weapon], 20) + "\x1b[32mAttack Strength    : \x1b[1m"+str(user.str)+"\x1b[0m\r\n"
	output += "\x1b[32m Armor         : \x1b[1m"+data.armor[user.armor]+"\x1b[0m" + func.padnumcol(data.armor[user.armor], 20) + "\x1b[32mDefensive Strength : \x1b[1m"+str(user.defence)+"\x1b[0m\r\n"
	output += "\x1b[32m Charm         : \x1b[1m"+str(user.charm)+"\x1b[0m" + func.padnumcol(str(user.charm), 20) + "\x1b[32mGems               : \x1b[1m"+str(user.gems)+"\x1b[0m\r\n\r\n"
	for skillnum in [1,2,3]:
		if ( user.cls == skillnum or user.getSkillPoint(skillnum) > 0 ):
			output += "\x1b[32m The "+data.classes[skillnum]+" Skills: \x1b[1m"
			if ( user.getSkillPoint(skillnum) > 0 ):
				output +=  str(user.getSkillPoint(skillnum)) + func.padnumcol(str(user.getSkillPoint(skillnum)), 11)
			else:
				output += "NONE     "
			output += func.padnumcol(data.classes[skillnum], 12)
			output += "\x1b[0m\x1b[32mUses Today: (\x1b[1m"+str(user.getSkillUse(skillnum))+"\x1b[22m)\x1b[0m\r\n"
	output += "\r\n \x1b[1;32mYou are currently interested in \x1b[37mThe "+data.classes[user.cls]+" \x1b[32mskills.\r\n\r\n";
	return output
	
def who(user):
	""" Who's Online
	* @return string Formatted output for display"""
	db = user.dbcon.cursor()
	db.execute("SELECT o.userid, fullname, whence FROM users u, online o WHERE o.userid = u.userid ORDER BY whence ASC")
	output  = "\r\n\r\n\x1b[1;37m                     Warriors In The Realm Now\x1b[22;32m\x1b[0m\r\n"
	output += user.art.line()
	for line in db.fetchall():
		output += "  \x1b[1;32m" + line[1] + func.padnumcol(line[1], 28)
		output += "\x1b[0m\x1b[32mArrived At             \x1b[1;37m" + str(line[2]) + "\x1b[0m\r\n"
	db.close()
	return output + "\r\n"

def dailyhappen(noprmpt, user):
	""" View Daily Happenings
	* @param bool $noprmpt Do not prompt for additions.
	* @return string Formatted output for display """
	db = user.dbcon.cursor()
	db.execute("SELECT data FROM (SELECT * FROM daily ORDER BY id DESC LIMIT 10) AS tbl ORDER BY tbl.id")
	output  = "\r\n\r\n\x1b[1;37mRecent Happenings\033[22;32m....\x1b[0m\r\n"
	output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	for line in db.fetchall():
		output += "    " + func.colorcode(line[0])
		output += "\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
	if ( not noprmpt ) :
		output +=  "\n\x1b[32m(\x1b[1;35mC\x1b[22;32m)ontinue  \x1b[32m(\x1b[1;35mT\x1b[22;32m)odays happenings again  \x1b[1;32m[\x1b[35mC\x1b[32m] \x1b[22m:-: "
	db.close()
	return output

def list(art, dbc):
	""" Player List
	* @return string Formatted output for display """
	db = dbc.cursor()
	db.execute("SELECT users.userid, fullname, exp, level, cls, spclm, spcld, spclt, sex, alive FROM users, stats WHERE users.userid = stats.userid ORDER BY exp DESC")
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
			
		output += lineSex + lineClass + "\x1b[32m" + line[1] + func.padnumcol(str(line[1]), 23) + func.padright(str(line[2]), 11)
		output += func.padright(str(line[3]), 6) + "        " + lineMaster + func.padnumcol(lineMaster, 12) + lineStatus + "\r\n"
	db.close()
	return output + "\r\n"
