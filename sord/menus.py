#!/usr/bin/python
import time
from functions import *
from data import *
"""
 * Menu Functions.
 * 
 * Contains all menus, and some menu creation functions
 * 
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage
"""


"""Turgons warrior training
 * @return string Fully formatted menu """
def menu_turgon(user):
	ptime = func_maketime(user)
	thismenu  = "\r\n\r\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mTurgons Warrior Training\x1b[0m\r\n"
	thismenu += user.art.blueline()
	thismenu += "  \x1b[32mYou enter the mighty Training Center.  Hundreds of warriors, young,\x1b[0m\r\n"
	thismenu += "  \x1b[32mas well as old, are sparring.  Every few seconds you hear someone\x1b[0m\r\n"
	thismenu += "  \x1b[32mshriek in pain.  Obviously some novice who let his gaurd down.\x1b[0m\r\n\r\n"
	thismenu += func_normmenu("(Q)uestion Master")
	thismenu += func_normmenu("(A)ttack Master")
	thismenu += "  \x1b[32m(\x1b[1;37mV\x1b[0m\x1b[32m)\x1b[1;37misit The Hall Of Honor\x1b[0m\r\n"
	thismenu += func_normmenu("(R)eturn to Town")
	thismenu += "\r\n  \x1b[32mYour master is \x1b[1;37m"+masters[user.getLevel()][0]+"\x1b[0m\x1b[32m.\x1b[0m\r\n\r\n"
	thismenu += "\x1b[1;35m  Turgon's Warrior Training \x1b[1;30m(Q,A,V,R) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

"""Ye olde bank
 * @return string Fully formatted menu"""
def menu_bank(user):
	ptime = func_maketime(user)
	thismenu  = "\r\n\r\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mBank\x1b[0m\r\n"
	thismenu += user.art.line()
	thismenu += "  \x1b[32mA polite clerk approaches. \x1b[1;35m\"Can I help you sir?\"\x1b[0m\r\n\r\n"
	thismenu += func_normmenu("(D)eposit Gold")
	thismenu += func_normmenu("(W)ithdraw Gold")
	thismenu += func_normmenu("(T)ransfer Gold")
	thismenu += func_normmenu("(R)eturn to Town")
	thismenu += "\r\n\r\n\x1b[32m  Gold In Hand: \x1b[1m" + str(user.getGold())
	thismenu += "\x1b[0m\x1b[32m Gold In Bank: \x1b[1m" + str(user.getBank()) + "\r\n"
	thismenu += "\x1b[1;35m  The Bank \x1b[1;30m(W,D,R,T,Q) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

""" Forest fight menu (pre-battle)
 * @return string Fully formatted menu """
def menu_forest(user):
	ptime = func_maketime(user)
	thismenu = "  \x1b[32mHitPoints: (\x1b[1m" + str(user.getHP()) + "\x1b[22m of \x1b[1m" + str(user.getHPMax())
	thismenu += "\x1b[22m)  Fights: \x1b[1m" + str(user.getForestFight()) + "\x1b[22m  Gold: \x1b[1m" + str(user.getGold())
	thismenu += "\x1b[22m  Gems: \x1b[1m" + str(user.getGems()) + "\x1b[0m\r\n"
	thismenu += "  \x1b[1;35mThe Forest  \x1b[1;30m(L,H,R,Q) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

""" Healers Hut
 * @return string Fully formatted menu """
def menu_heal(user):
	ptime = func_maketime(user)
	thismenu  = "\r\n\r\n  \x1b[1;37mSaga of the Red Dragon - \x1b[0m\x1b[32mHealers Hut\x1b[0m\r\n"
	thismenu += user.art.line()
	thismenu += "  \x1b[32mYou enter the smoky healers hut.\r\n  \x1b[1;35m\"What is your wish, warrior?\" \x1b[0m\x1b[32m the old\r\n  \x1b[32mhealer asks.\x1b[0m\r\n\r\n"
	thismenu += func_normmenu("(H)eal all possible")
	thismenu += func_normmenu("(C)ertain amount healed")
	thismenu += func_normmenu("(R)eturn")
	thismenu += "\r\n\x1b[32m  HitPoints: \x1b[1m" + str(user.getHP()) + "\x1b[22m of \x1b[1m" + str(user.getHPMax()) + "\x1b[0m"
	thismenu += "\x1b[32m  Gold In Hand: \x1b[1m" + str(user.getGold())
	thismenu += "\x1b[22m.\r\n  It costs \x1b[1m" + str(user.getLevel() * 5) + "\x1b[22m gold to heal 1 HitPoint\x1b[0m\r\n"
	thismenu += "\x1b[1;35m  The Healers Hut \x1b[1;30m(H,C,R) (? for menu)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

"""Main Menu - Non-Expert
 * @todo Married List and Other Places
 * @return string Fully formatted menu"""
def menu_mainlong(user):
	thismenu  = "\r\n\r\n\x1b[1;37m  Saga of the Red Dragon - \x1b[0m\x1b[32mTown Square\x1b[0m\r\n"
	thismenu += user.art.line()
	thismenu += "\x1b[32m  The streets are crowded, it is difficult to\r\n  push your way through the mob....\r\n\r\n"
	thismenu += func_menu_2col("(F)orest", "(S)laughter other players", 5, 5)
	thismenu += func_menu_2col("(K)ing Arthurs Weapons", "(A)bduls Armour", 5, 5)
	thismenu += func_menu_2col("(H)ealers Hut", "(V)iew your stats", 5, 5)
	thismenu += func_menu_2col("(I)nn", "(T)urgons Warrior Training", 5, 5)
	thismenu += func_menu_2col("(Y)e Old Bank", "(L)ist Warriors", 5, 5)
	thismenu += func_menu_2col("(W)rite Mail", "(D)aily News", 5, 5)
	#thismenu += func_menu_2col("(C)onjugality List", "(O)ther Places", 5, 5)
	thismenu += func_menu_2col("(X)pert Mode", "(M)ake Announcement", 7, 5)
	thismenu += func_menu_2col("(P)eople Online", "(Q)uit to Fields", 5, 2)
	return thismenu

""" Main Menu - Expert
 * Generate short main menu with prompt.  Appended to Non-Expert menu as well.
 * @return string Fully formatted menu """
def menu_mainshort(user):
	ptime = func_maketime(user)
	thismenu  = "\r\n  \x1b[1;35mThe Town Square\x1b[0m\x1b[1;30m (? for menu)\x1b[0m\r\n"
	thismenu += "  \x1b[1;30m(F,S,K,A,H,V,I,T,Y,L,W,D,X,M,P,Q)\x1b[0m\r\n\r\n"
	thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

"""Abdul's Armor
 * @return string Fully formatted menu"""
def menu_abdul(user):
	ptime = func_maketime(user)
	thismenu  = "\r\n  \x1b[32mCurrent armour: \x1b[1m"+armor[user.getArmor()]+"\x1b[0m\r\n"
	thismenu += "  \x1b[1;35mAbduls Armour \x1b[1;30m(B,S,Y,R) (? for menu)\r\n\r\n"
	thismenu += "  \x1b[0m\x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu

"""King Arthur's Weapons
 * @return string Fully formatted menu """
 
def menu_arthur(user):
	ptime = func_maketime(user)
	thismenu  = "\r\n  \x1b[32mCurrent weapon: \x1b[1m"+weapon[user.getWeapon()]+"\x1b[0m\r\n"
	thismenu += "  \x1b[1;35mKing Arthur's Weapons \x1b[1;30m(B,S,Y,R) (? for menu)\r\n\r\n"
	thismenu += "  \x1b[0m\x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
	return thismenu
