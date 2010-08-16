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
	db = user.dbcon.cursor()
	db.execute("SELECT `id`, `from`, `message`, DATE_FORMAT(sent, '%W %M %Y, %H:%i') as sent FROM mail WHERE `to` = ?", (user.thisUserID,))
	for (id, sender, message, sent) in db.fetchall():
		thismail  = "\r\n  \x1b[1;37mNew Mail...\x1b[0m\r\n"
		thismail += "\x1b[32m-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\x1b[0m\r\n"
		thismail += "\x1b[32m  From: \x1b[1m" + user.userGetName(sender) + "\x1b[0m\r\n"
		thismail += "\x1b[32m  Date: \x1b[1m" + sent + "\x1b[0m\r\n"
		thismail += "\x1b[32m  Message: " + func_colorcode(message) + "\x1b[0m\r\n\r\n"
		user.write(thismail)
		user.pause()
	db.close()
	user.dbcon.execute("DELETE FROM mail WHERE `to` = ?", (user.thisUserID,))
	user.dbcon.commit()

def msg_sendmail(user):
	""" Send in game mail to a user """
	toid = module_finduser(user, "\r\n  \x1b[32mSend mail to which user?")
	if ( toid == 0 ):
		return False
	else:
		user.write("\r\n  \x1b[32mYour message \x1b[1m:\x1b[0m ")
		msg = func_getLine(user.ntcon, True)
		user.dbcon.execute("INSERT INTO mail (`to`, `from`, `message`) VALUES ( ?, ?, ? )", (toid, user.thisUserID, msg))
		user.dbcon.commit()
		user.write(func_casebold("\r\n  Message Sent\r\n", 2))
		user.pause()

def msg_announce(user):
	""" Make announcment """
	user.write(func_casebold("\r\n  Your announcment? :-: ", 2))
	ann = func_getLine(user.ntcon, True)
	user.dbcon.execute("INSERT INTO daily ( `data` ) VALUES ( ? )", (ann, ))
	user.dbcon.commit()
	user.write(func_casebold("\r\n  Announcment Made!\r\n", 2))
	user.pause()
