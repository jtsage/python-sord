#!/usr/bin/python
from functions import *
from modules import *
"""
 * Communications functions
 * 
 * @package phpsord
 * @subpackage phpsord-general
 * @author J.T.Sage
"""

def msg_readmail(user):
	""" Read waiting in-game e-mail. Very simple.
	* @param int $userid User ID to pull in game mail for."""
	thisSQL = "SELECT `id`, `from`, `message`, DATE_FORMAT(sent, '%W %M %Y, %H:%i') as sent FROM "+user.thisSord.sqlPrefix()+"mail WHERE `to` = "+str(user.thisUserID)
	user.db.execute(thisSQL)
	for (id, sender, message, sent) in user.db.fetchall():
		thismail  = "\r\n  \x1b[1;37mNew Mail...\x1b[0m\r\n"
		thismail += "\x1b[32m-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\x1b[0m\r\n"
		thismail += "\x1b[32m  From: \x1b[1m" + user.userGetName(sender) + "\x1b[0m\r\n"
		thismail += "\x1b[32m  Date: \x1b[1m" + sent + "\x1b[0m\r\n"
		thismail += "\x1b[32m  Message: " + func_colorcode(message) + "\x1b[0m\r\n\r\n"
		user.write(thismail)
		user.pause()
	thisSQL = "DELETE FROM "+user.thisSord.sqlPrefix()+"mail WHERE `to` = "+str(user.thisUserID)
	user.db.execute(thisSQL)

def msg_sendmail(user):
	""" Send in game mail to a user """
	toid = module_finduser(user, "\r\n  \x1b[32mSend mail to which user?")
	if ( toid == 0 ):
		return False
	else:
		user.write("\r\n  \x1b[32mYour message \x1b[1m:\x1b[0m ")
		msg = func_getLine(user.connection, True)
		safemsg = user.dbc.escape_string(msg)
		thisSQL = "INSERT INTO "+user.thisSord.sqlPrefix()+"mail (`to`, `from`, `message`) VALUES ('"+str(toid)+"', '"+str(user.thisUserID)+"', '"+safemsg+"')"
		user.db.execute(thisSQL)
		user.write(func_casebold("\r\n  Message Sent\r\n", 2))
		user.pause()

def msg_announce(user):
	""" Make announcment """
	user.write(func_casebold("\r\n  Your announcment? :-: ", 2))
	ann = func_getLine(user.connection, True)
	safeann = user.dbc.escape_string(ann)
	thisSQL = "INSERT INTO "+user.thisSord.sqlPrefix()+"daily ( `data` ) VALUES ('"+safeann+"')"
	user.db.execute(thisSQL)
	user.write(func_casebold("\r\n  Announcment Made!\r\n", 2))
	user.pause()
