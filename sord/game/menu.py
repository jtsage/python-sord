#!/usr/bin/python
"""
 * Menu Functions.
 * 
 * Contains all menus, and some menu creation functions
 * 
"""
import time
from . import data
from ..base import func

def menu_turgon(user):
	"""Turgons warrior training
	* @return string Fully formatted menu """
	ptime = func.maketime(user)
	try:
		thismenu = "\r\n  \x1b[32mYour master is \x1b[1;37m"+data.masters[user.level][0]+"\x1b[0m\x1b[32m.\x1b[0m\r\n\r\n"
	except IndexError:
		thismenu = "\r\n  \x1b[32mYou have no master.  You are as smart as you can possibly get.\x1b[0m\r\n\r\n"
	thismenu += "\x1b[1;35m  Turgon's Warrior Training \x1b[1;30m(Q,A,V,R) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

def bank(user):
	"""Ye olde bank
	* @return string Fully formatted menu"""
	ptime = func.maketime(user)
	thismenu = "\r\n\r\n\x1b[32m  Gold In Hand: \x1b[1m" + str(user.gold)
	thismenu += "\x1b[0m\x1b[32m Gold In Bank: \x1b[1m" + str(user.bank) + "\r\n"
	thismenu += "\x1b[1;35m  The Bank \x1b[1;30m(W,D,R,T,Q) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

def forest(user):
	""" Forest fight menu (pre-battle)
	* @return string Fully formatted menu """
	ptime = func.maketime(user)
	thismenu = "\r\n  \x1b[32mHitPoints: (\x1b[1m" + str(user.hp) + "\x1b[22m of \x1b[1m" + str(user.hpmax)
	thismenu += "\x1b[22m)  Fights: \x1b[1m" + str(user.ffight) + "\x1b[22m  Gold: \x1b[1m" + str(user.gold)
	thismenu += "\x1b[22m  Gems: \x1b[1m" + str(user.gems) + "\x1b[0m\r\n"
	thismenu += "  \x1b[1;35mThe Forest  \x1b[1;30m(L,H,R,Q) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

def slaughter(user):
	ptime = func.maketime(user)
	thismenu = "\r\n\x1b[1;35m  Slaughter Other Players\r\n  \x1b[1;30m(S,L,E,W,R) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu
	
def heal(user):
	""" Healers Hut
	* @return string Fully formatted menu """
	ptime = func.maketime(user)
	thismenu  = "\r\n\r\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mHealers Hut\x1b[0m\r\n"
	thismenu += user.art.line()
	thismenu += "  \x1b[32mYou enter the smoky healers hut.\r\n  \x1b[1;35m\"What is your wish, warrior?\" \x1b[0m\x1b[32m the old\r\n  \x1b[32mhealer asks.\x1b[0m\r\n\r\n"
	thismenu += func.normmenu("(H)eal all possible")
	thismenu += func.normmenu("(C)ertain amount healed")
	thismenu += func.normmenu("(R)eturn")
	thismenu += "\r\n\x1b[32m  HitPoints: \x1b[1m" + str(user.hp) + "\x1b[22m of \x1b[1m" + str(user.hpmax) + "\x1b[0m"
	thismenu += "\x1b[32m  Gold In Hand: \x1b[1m" + str(user.gold)
	thismenu += "\x1b[22m.\r\n  It costs \x1b[1m" + str(user.level * 5) + "\x1b[22m gold to heal 1 HitPoint\x1b[0m\r\n"
	thismenu += "\x1b[1;35m  The Healers Hut \x1b[1;30m(H,C,R) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

def mainlong(user):
	"""Main Menu - Non-Expert
	* @todo Married List and Other Places
	* @return string Fully formatted menu"""
	thismenu  = "\r\n\r\n\x1b[1;37m  Saga of the Red Dragon - \x1b[0m\x1b[32mTown Square\x1b[0m\r\n"
	thismenu += user.art.line()
	thismenu += "\x1b[32m  The streets are crowded, it is difficult to\r\n  push your way through the mob....\r\n\r\n"
	thismenu += func.menu_2col("(F)orest", "(S)laughter other players", 5, 5)
	thismenu += func.menu_2col("(K)ing Arthurs Weapons", "(A)bduls Armour", 5, 5)
	thismenu += func.menu_2col("(H)ealers Hut", "(V)iew your stats", 5, 5)
	thismenu += func.menu_2col("(I)nn", "(T)urgons Warrior Training", 5, 5)
	thismenu += func.menu_2col("(Y)e Old Bank", "(L)ist Warriors", 5, 5)
	thismenu += func.menu_2col("(W)rite Mail", "(D)aily News", 5, 5)
	#thismenu += func_menu_2col("(C)onjugality List", "(O)ther Places", 5, 5)
	thismenu += func.menu_2col("(X)pert Mode", "(M)ake Announcement", 7, 5)
	thismenu += func.menu_2col("(P)eople Online", "(Q)uit to Fields", 5, 2)
	return thismenu

def mainshort(user):
	""" Main Menu - Expert
	* Generate short main menu with prompt.  Appended to Non-Expert menu as well.
	* @return string Fully formatted menu """
	ptime = func.maketime(user)
	thismenu  = "\r\n  \x1b[1;35mThe Town Square\x1b[0m\x1b[1;30m (? for menu)\x1b[0m\r\n"
	thismenu += "  \x1b[1;30m(F,S,K,A,H,V,I,T,Y,L,W,D,X,M,P,Q)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

def abdul(user):
	"""Abdul's Armor
	* @return string Fully formatted menu"""
	ptime = func.maketime(user)
	thismenu  = "\r\n  \x1b[32mCurrent armour: \x1b[1m"+data.armor[user.armor]+"\x1b[0m\r\n"
	thismenu += "  \x1b[1;35mAbduls Armour \x1b[1;30m(B,S,Y,R) (? for menu)\r\n\r\n"
	thismenu += "  \x1b[0m\x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu
 
def arthur(user):
	"""King Arthur's Weapons
	* @return string Fully formatted menu """
	ptime = func.maketime(user)
	thismenu  = "\r\n  \x1b[32mCurrent weapon: \x1b[1m"+data.weapon[user.weapon]+"\x1b[0m\r\n"
	thismenu += "  \x1b[1;35mKing Arthur's Weapons \x1b[1;30m(B,S,Y,R) (? for menu)\r\n\r\n"
	thismenu += "  \x1b[0m\x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu
