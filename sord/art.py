#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 * Artwork headers.
 * 
 * Contains all ANSI/ASCII art headers used throughout.
 * 
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage
 * @author Seth Able Robinson original artwork
 * 
 * To Add ANSI Files, convert all high-ascii characters to variables as follows:
 * 
 * 				ASCII			UTF
 * VAR		OCT		DEC		DEC		HEX
 * a176		260		176		9617	2591
 * a178		261		177		9618	2592
 * a179		262		178		9619	2593
 * a219		333		219		9608	2588
 * a220		334		220		9604	2584
 * a221		335		221		9612	258C
 * a222		336		222		9616	2590
 * a223		337		223		9600	2580
 * a254		376		254		9642	25AA
"""

A176 = unichr(9617).encode('UTF-8')
A177 = unichr(9618).encode('UTF-8')
A178 = unichr(9619).encode('UTF-8')
A219 = unichr(9608).encode('UTF-8')
A220 = unichr(9604).encode('UTF-8')
A221 = unichr(9612).encode('UTF-8')
A222 = unichr(9616).encode('UTF-8')
A223 = unichr(9600).encode('UTF-8')
A254 = unichr(9642).encode('UTF-8')
ESC = "\x1b["
	
class art():
	
	""" Dark Green Horizontal Rule """
	def line(self):
		return ESC+"32m-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"+ESC+"0m\n"

	""" Dark Blue Horizontal Rule """
	def blueline(self): 
		return ESC+"34m-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"+ESC+"0m\n"

	""" Game System Information Banner"""
	def banner(self, sordGame):
		#$rundays = control_getruntime();
		rundays = 0
		thismsg  = ESC+"32m                           Saga Of The Red Dragon"+ESC+"0m\n"
		thismsg += ESC+"32m                           "+sordGame.host()+"\n\n"+ESC+"0m\n"
		thismsg += ESC+"32m                    Compiled June 25, 2009: Version "+ESC+"1;37m"+sordGame.version()+ESC+"0m\n"
		thismsg += ESC+"22;32m                        (c) pre-2009 by Someone Else\n\n"+ESC+"0m\n"
		thismsg += ESC+"32m                           "+ESC+"1;37mREGISTERED TO "+ESC+"0m"+ESC+"1;34m"+sordGame.admin()+ESC+"0m\n\n"
		thismsg += ESC+"32m             The current game has been running for "+ESC+"1m"+str(rundays)+ESC+"22m game days.\n"+ESC+"0m\n"
		thismsg += ESC+"32m            Players are deleted after "+ESC+"1m"+str(sordGame.deleteInactive())+ESC+"22m real days of inactivity."+ESC+"0m\n"
		thismsg += ESC+"32m               Players are enjoying "+ESC+"1m"+str(sordGame.forestFights())+ESC+"22m forest fights per day."+ESC+"0m\n"
		thismsg += ESC+"32m               Players are enjoying "+ESC+"1m"+str(sordGame.playerFights())+ESC+"22m player fights per day."+ESC+"0m\n"
		thismsg += ESC+"32m            Players are enjoying "+ESC+"1m"+str(sordGame.bankInterest())+"%"+ESC+"22m interest at the bank per day."+ESC+"0m\n"
		thismsg += ESC+"32m                   The current game day is "+ESC+"1m"+str(sordGame.dayLength())+ESC+"22m real hours long.\n"+ESC+"0m\n"
		thismsg += ESC+"32m                         ("+ESC+"1mE"+ESC+"22m)nter the realm of the Dragon"+ESC+"0m\n"
		thismsg += ESC+"32m                         ("+ESC+"1mL"+ESC+"22m)ist Warriors"+ESC+"0m\n"
		thismsg += ESC+"32m                         ("+ESC+"1mQ"+ESC+"22m)uit the game server\n"+ESC+"0m\n"
		thismsg += ESC+"32m                         Your choice, warrior? ["+ESC+"1mE"+ESC+"22m]: "+ESC+"0m"+ESC+"0m\n"
		return thismsg

	""" Game Welcome Screen - in use """
	def header(self):
		thismsg = ESC + "0m                          " + A220 + A220 + A220 + A220 + A220 +"                                                " + ESC + "0m\n"
		thismsg += "                      "+A220+A220+A219+A219+A219+A219+ESC+"1;47m"+A176+A177+A178+ESC+"40m"+A219+A219+A220+A220+ESC+"0m                                            "+ESC+"0m\n"
		thismsg += ESC+"1m  "+ESC+"31mS"+ESC+"0;31mAGA"+ESC+"37m               "+A219+A219+ESC+"30;47mo"+ESC+"37;40m"+A219+ESC+"1;47m"+A176+A176+A177+A177+A178+ESC+"40m"+A219+A219+A219+A219+A219+A219+ESC+"0m                                           "+ESC+"0m\n"
		thismsg += ESC+"1m  "+ESC+"31mO"+ESC+"0;31mF THE"+ESC+"37m            "+A219+A219+ESC+"30;47mO"+ESC+"37;40m"+A219+A219+ESC+"1;47m"+A176+A177+A177+A178+ESC+"40m"+A219+A219+A219+A219+A219+A219+A219+A219+ESC+"0m                 "+A220+A220+A220+ESC+"1m"+A220+A220+ESC+"0m                    "+ESC+"0m\n"
		thismsg += ESC+"1m  "+ESC+"31mR"+ESC+"0;31mED"+ESC+"37m               "+A219+ESC+"30;47mo"+ESC+"37;40m"+A219+A219+ESC+"1;47m"+A176+A176+A177+A178+ESC+"40m"+A219+A219+A219+A219+A219+A219+A219+A219+A219+ESC+"0m                   "+A223+A219+ESC+"1;47m"+A176+A219+A219+A219+ESC+"40m"+A220+A220+" "+ESC+"0;31m"+A220+ESC+"37m             "+ESC+"0m\n"
		thismsg += ESC+"31m  "+ESC+"1mD"+ESC+"0;31mRAGON 0.9.9"+ESC+"37m      "+A223+A219+A219+ESC+"1;47m"+A176+A177+A177+A178+A219+ESC+"40m"+A219+A219+A219+A219+A219+A219+A219+A219+A223+ESC+"0m                     "+A219+ESC+"1;47m"+A219+A219+ESC+"40m"+A223+A223+ESC+"0;31m"+A220+ESC+"1;41m"+A176+" "+ESC+"0;31m"+A220+ESC+"37m           "+ESC+"0m\n"
		thismsg += ESC+"31m  concept"+ESC+"37m            "+A223+ESC+"1;47m"+A176+A177+A177+A178+A178+ESC+"40m"+A219+A219+A219+A219+A219+A219+A219+A219+A223+ESC+"0m        "+ESC+"1m"+A220+ESC+"0m        "+ESC+"1m"+A220+ESC+"0m       "+ESC+"31m"+A220+A220+ESC+"1;41m"+A176+A178+"  "+A176+" "+ESC+"0;31m"+A220+A220+ESC+"37m        "+ESC+"0m\n"
		thismsg += ESC+"31m  Seth Robinson "+ESC+"37m"+A222+"       "+A223+A223+ESC+"1;47m"+A178+ESC+"40m"+A219+A219+A219+A219+A223+A223+ESC+"0m        "+A220+ESC+"1;47m"+A220+ESC+"40m"+A223+"    "+ESC+"0m"+A220+A220+ESC+"1;47m"+A220+ESC+"40m"+A223+A223+"   "+ESC+"0m"+A223+A219+A220+ESC+"1m"+A220+"  "+ESC+"0;31m"+A223+ESC+"1;41m"+A176+A177+A178+"  "+ESC+"0;31m"+A223+ESC+"41m  "+ESC+"1m"+A176+" "+ESC+"0;31m"+A220+ESC+"37m     "+ESC+"0m\n"
		thismsg += ESC+"31m  by"+ESC+"0m            "+A219+"                      "+A220+ESC+"1;47m"+A220+ESC+"40m"+A223+"   "+ESC+"0m"+A220+ESC+"1;47m"+A220+A220+A219+ESC+"40m"+A223+ESC+"0m        "+A223+ESC+"1;47m"+A176+A219+ESC+"40m"+A220+"  "+ESC+"0;31m"+A223+ESC+"1;41m"+A177+A178+"  "+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+" "+A176+" "+A176+ESC+"0;31m"+A220+ESC+"37m   "+ESC+"0m\n"
		thismsg += ESC+"1;34m  J"+ESC+"0;34m."+ESC+"1mT"+ESC+"0;34m."+ESC+"1mS"+ESC+"0;34mage"+ESC+"0m     "+A219+ESC+"1;30;47m"+A176+ESC+"0;37;40m"+A221+"                   "+A220+ESC+"1;47m"+A177+A176+ESC+"40m"+A223+" "+ESC+"0m"+A220+ESC+"1;47m"+A220+A220+A219+ESC+"40m"+A223+ESC+"0m            "+A223+ESC+"1;47m"+A177+A219+A219+ESC+"40m"+A220+" "+ESC+"0;31m"+A223+ESC+"1;41m"+A177+A176+A178+" "+ESC+"0;31m"+A220+A223+ESC+"1;41m"+A176+A178+A176+A176+A177+A177+ESC+"0;37;40m "+ESC+"0m\n"
		thismsg += "               "+A219+A219+"                   "+ESC+"1;47m"+A176+A177+A219+ESC+"40m"+A223+" "+ESC+"0m"+A223+ESC+"1m"+A223+ESC+"41m"+A223+ESC+"0;31m"+A220+A220+A220+A220+ESC+"41m "+ESC+"40m"+A178+A177+A176+"   "+A220+A220+A220+A220+A223+A220+ESC+"1;41m"+A176+ESC+"0;31m"+A220+ESC+"1;41m"+A177+ESC+"0;31m"+A220+ESC+"41m "+ESC+"37;40m "+ESC+"31m"+A223+ESC+"1;41m"+A177+A178+" "+A219+ESC+"0;37;40m "+ESC+"1;31;41m"+A178+A178+A176+A177+A177+A219+ESC+"0m\n"
		thismsg += ESC+"37m              "+A219+ESC+"1;30;47m"+A176+ESC+"0;37;40m                   "+A219+A223+ESC+"1m"+A223+ESC+"0;31m"+A220+A220+ESC+"41m "+ESC+"40m"+A223+A223+A223+"   "+A220+A220+ESC+"41m "+ESC+"40m"+A223+A220+ESC+"41m "+ESC+"40m"+A223+A223+A223+"  "+A176+A176+" "+ESC+"1;41m"+A176+" "+A178+A178+A219+ESC+"0;31m"+A220+" "+A223+ESC+"1;41m"+A177+A176+" "+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+A178+A176+A177+A177+A219+ESC+"0m\n"
		thismsg += ESC+"37m              "+A219+ESC+"1;30;47m"+A176+ESC+"0;37;40m                  "+A219+" "+ESC+"31m"+A220+ESC+"41m "+ESC+"40m"+A223+"   "+A220+A220+A220+ESC+"41m "+ESC+"40m"+A178+A177+A176+ESC+"37m      "+ESC+"31m"+A178+A177+A177+A223+"   "+ESC+"1;41m"+A176+" "+A177+A178+A219+" "+ESC+"0;31m"+A220+" "+A223+ESC+"1;41m"+A177+A219+ESC+"0;31m"+A220+A223+ESC+"1;41m"+A178+" "+A177+A178+ESC+"0m\n"
		thismsg += ESC+"37m               "+ESC+"1;30;47m"+A176+ESC+"0;37;40m"+A219+"                "+A219+" "+ESC+"31m"+A220+ESC+"41m "+ESC+"37;40m "+ESC+"31m"+A220+ESC+"41m      "+ESC+"40m"+A178+A177+A176+"    "+A220+ESC+"41m "+ESC+"40m"+A223+A223+ESC+"37m        "+ESC+"1;31;41m"+A176+" "+A178+A177+A219+A219+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+A177+A178+ESC+"0;37;40m "+ESC+"31m"+A220+A220+A223+ESC+"1;41m"+A178+ESC+"0m\n"
		thismsg += ESC+"37m               "+ESC+"1;30;47m"+A176+ESC+"0;37;40m"+A219+ESC+"1;30;47m"+A176+ESC+"0;37;40m              "+ESC+"31m"+A220+A220+ESC+"41m   "+ESC+"40m"+A220+ESC+"41m   "+ESC+"40m"+A219+A178+A178+A177+A176+A223+" "+A220+A220+"  "+A223+ESC+"37m            "+ESC+"1;31;41m"+A176+" "+A177+A178+A219+ESC+"0;37;40m  "+ESC+"1;31;41m"+A177+A178+A219+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+A178+A178+ESC+"0m\n"
		thismsg += ESC+"37m                "+A219+A219+A219+"         "+ESC+"31m"+A220+ESC+"41m     "+ESC+"40m"+A221+ESC+"41m     "+ESC+"40m"+A178+A223+A223+A223+" "+A220+A220+ESC+"41m "+ESC+"40m"+A223+A223+ESC+"41m   "+ESC+"40m"+A220+" "+A220+A220+ESC+"41m  "+ESC+"40m"+A178+A178+A177+A223+"   "+ESC+"1;41m"+A176+" "+A177+A219+A219+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+A177+" "+ESC+"0;31m"+A220+ESC+"1;41m"+A176+A178+A178+ESC+"0m\n"
		thismsg += ESC+"37m                "+A222+ESC+"1;30;47m"+A176+A177+ESC+"0;37;40m"+A221+"       "+ESC+"31m"+A220+ESC+"41m "+ESC+"1m"+A176+"  "+ESC+"0;31m"+A223+"  "+ESC+"41m    "+ESC+"40m"+A220+A220+A220+ESC+"41m       "+ESC+"40m"+A220+A220+" "+A223+A223+A220+" "+A223+ESC+"41m "+ESC+"40m"+A178+A178+A178+ESC+"37m      "+ESC+"1;31;41m"+A176+" "+A178+A219+ESC+"0;37;40m "+ESC+"31m"+A223+ESC+"1;41m"+A176+A177+A178+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+A178+ESC+"0m\n"
		thismsg += ESC+"37m               "+A222+ESC+"1;30;47m"+A176+A177+ESC+"0;37;40m"+A219+"       "+ESC+"31m"+A220+ESC+"41m "+ESC+"1m"+A176+ESC+"0;31m"+A223+A223+"    "+ESC+"41m                  "+ESC+"40m"+A220+A222+ESC+"41m "+ESC+"40m"+A220+A220+" "+A223+A178+ESC+"37m       "+ESC+"1;31;41m"+A176+A177+A178+A219+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+A177+" "+A178+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+ESC+"0m\n"
		thismsg += "               "+A219+ESC+"1;30;47m"+A177+ESC+"0;37;40m"+A219+"      "+ESC+"31m"+A222+A219+ESC+"1;41m"+A176+A176+ESC+"0;31m"+A221+" "+ESC+"1;5;32m"+A220+A220+A223+"  "+ESC+"0;31;41m     "+ESC+"40m"+A178+ESC+"41m        "+ESC+"40m"+A223+A223+ESC+"41m   "+ESC+"40m"+A220+A222+ESC+"41m   "+ESC+"40m"+A220+"    "+A220+A220+A220+A220+A223+ESC+"1;41m"+A176+A177+A178+ESC+"0;31m"+A220+" "+ESC+"1;41m"+A176+A177+" "+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+ESC+"0m\n"
		thismsg += ESC+"37m              "+A219+ESC+"1;30;47m"+A176+ESC+"0;37;40m"+A219+"      "+ESC+"31m"+A222+ESC+"41m "+ESC+"1m"+A176+" "+ESC+"0;37;40m  "+ESC+"1;5;32m"+A219+A219+A223+"  "+ESC+"0;31m"+A222+ESC+"41m               "+ESC+"40m"+A178+A220+A222+ESC+"41m  "+ESC+"40m"+A220+A222+A219+ESC+"41m  "+ESC+"37;40m "+ESC+"31;41m    "+ESC+"40m"+A178+A223+"  "+A223+ESC+"1;41m"+A176+A177+A219+ESC+"0;37;40m "+ESC+"1;31;41m"+A176+A177+A219+A178+ESC+"0;37;40m "+ESC+"0m\n"
		thismsg += "             "+A222+ESC+"1;30;47m"+A176+A177+ESC+"0;37;40m"+A219+"     "+ESC+"31m"+A222+ESC+"41m "+ESC+"1m"+A178+A176+ESC+"0;37;40m  "+ESC+"1;5;32m"+A223+"  "+ESC+"0;31m"+A220+A220+A220+ESC+"41m     "+ESC+"40m"+A178+ESC+"41m          "+ESC+"40m"+A223+"  "+ESC+"41m   "+ESC+"40m"+A220+A222+A219+ESC+"41m "+ESC+"40m"+A220+" "+A223+ESC+"41m "+ESC+"40m"+A178+A223+"    "+A223+ESC+"1;41m"+A176+A219+ESC+"0;37;40m "+ESC+"31;41m "+A177+A219+A178+ESC+"37;40m "+ESC+"0m\n"
		thismsg += "              "+A219+ESC+"1;30;47m"+A176+ESC+"0;37;40m"+A221+"    "+ESC+"31m"+A222+ESC+"41m "+ESC+"1m"+A177+A176+ESC+"0;31m"+A221+A220+ESC+"41m                   "+ESC+"1m"+A176+ESC+"0;31m"+A223+A223+"   "+A222+ESC+"41m    "+ESC+"40m"+A220+A222+ESC+"41m "+ESC+"1m"+A176+A176+ESC+"0;31m"+A220+A220+ESC+"37m       "+ESC+"1;31;41m"+A176+A177+ESC+"0;37;40m "+ESC+"31;41m "+A176+A177+A219+A178+ESC+"0m\n"
		thismsg += ESC+"37m               "+A219+ESC+"1;30;47m"+A177+ESC+"0;37;40m   "+ESC+"31m"+A220+A220+A223+ESC+"41m         "+ESC+"40m"+A176+A222+ESC+"41m          "+ESC+"40m"+A223+ESC+"37m      "+ESC+"31m"+A220+ESC+"1;41m"+A176+"     "+ESC+"0;31m"+A220+A222+ESC+"41m "+ESC+"1m"+A177+A177+A176+" "+ESC+"0;37;40m "+ESC+"31m"+A220+"    "+ESC+"1;41m"+A176+A219+ESC+"0;37;40m "+ESC+"31;41m  "+A177+" "+A219+ESC+"0m\n"
		thismsg += ESC+"37m                "+A219+A221+" "+ESC+"31;41m    "+ESC+"37;40m "+ESC+"31;41m      "+ESC+"40m"+A177+A177+A176+A178+ESC+"41m         "+ESC+"1m"+A176+ESC+"0;37;40m   "+ESC+"31m"+A220+ESC+"41m   "+ESC+"1m"+A177+A176+A176+"     "+ESC+"0;31m"+A222+ESC+"41m  "+ESC+"1m"+A178+A177+A176+ESC+"0;31m"+A220+" "+ESC+"41m "+ESC+"40m"+A178+A220+A220+" "+ESC+"1;41m"+A178+ESC+"0;31m"+A220+" "+ESC+"41m  "+ESC+"1m"+A177+A219+ESC+"0m\n"
		thismsg += ESC+"37m           "+ESC+"1m"+A220+"    "+ESC+"0m"+A223+" "+ESC+"31;41m "+ESC+"40m"+A223+" "+ESC+"41m      "+ESC+"40m"+A219+A178+A178+A177+A176+A176+A177+ESC+"41m        "+ESC+"1m"+A176+ESC+"0;37;40m   "+ESC+"31;41m    "+A178+A177+A177+A176+"     "+ESC+"40m"+A220+A222+ESC+"41m  "+ESC+"1m"+A178+A177+A176+ESC+"0;37;40m "+ESC+"31m"+A223+A178+"   "+ESC+"1;41m"+A177+A219+ESC+"0;37;40m "+ESC+"31;41m "+A176+A176+A178+ESC+"0m\n"
		thismsg += ESC+"37m           "+A223+ESC+"1m"+A219+A220+"   "+ESC+"0;31;41m "+A177+A178+A176+A176+"  "+ESC+"40m"+A223+A223+A223+A223+A223+A223+ESC+"41m "+ESC+"40m"+A219+A176+A178+ESC+"41m        "+ESC+"1m"+A176+ESC+"0;37;40m  "+ESC+"31m"+A222+ESC+"41m   "+ESC+"1m"+A219+A178+A178+A177+A176+"      "+ESC+"0;37;40m "+ESC+"31;41m  "+A219+A178+A177+A176+ESC+"37;40m "+ESC+"31m"+A223+"   "+ESC+"1;41m"+A176+ESC+"0;31m"+A223+" "+ESC+"41m "+ESC+"1m"+A176+A177+A219+ESC+"0m\n"
		thismsg += "            "+A223+ESC+"1;47m"+A223+ESC+"40m"+A219+A223+ESC+"0;31m"+A220+ESC+"1;41m"+A178+A176+A176+" "+ESC+"0;31m"+A223+"  "+ESC+"1;37;47m"+A222+ESC+"40m"+A221+A223+A220+" "+ESC+"0;31m"+A177+" "+A223+ESC+"41m "+ESC+"40m"+A221+ESC+"41m       "+ESC+"1m"+A176+ESC+"0;31m"+A223+" "+A220+ESC+"41m    "+ESC+"1m"+A219+A178+A178+A177+A176+"       "+ESC+"0;31m"+A220+A223+ESC+"41m "+ESC+"1m"+A219+A178+A177+A176+" "+ESC+"0;31m"+A223+"  "+ESC+"1;41m"+A176+ESC+"0;37;40m "+ESC+"31;41m "+A176+" "+A177+A219+ESC+"0m\n"
		thismsg += ESC+"37m              "+A223+ESC+"31m"+A222+ESC+"1;41m"+A177+A176+"  "+ESC+"0;31m"+A223+" "+ESC+"1;37;47m"+A222+ESC+"40m"+A221+" "+ESC+"47m"+A222+ESC+"40m"+A221+"  "+ESC+"0;31m"+A178+A177+" "+A223+ESC+"41m        "+ESC+"1m"+A176+ESC+"0;37;40m "+ESC+"33m"+A220+" "+ESC+"31m"+A223+ESC+"41m    "+ESC+"1m"+A219+A178+A177+A176+A176+"       "+ESC+"0;31m"+A220+A223+ESC+"41m "+ESC+"1m"+A178+A177+A176+" "+ESC+"0;37;40m "+ESC+"31;41m "+ESC+"40m"+A220+A223+" "+ESC+"41m "+ESC+"1m"+A176+A176+" "+A178+ESC+"0m\n"
		thismsg += ESC+"37m                "+ESC+"31;41m "+A176+A176+ESC+"37;40m "+A220+ESC+"1m"+A219+ESC+"0m"+A223+ESC+"1m"+A219+A221+" "+A223+"    "+A223+A220+" "+ESC+"0;31;41m   "+ESC+"40m"+A223+A220+ESC+"41m  "+ESC+"40m"+A223+" "+ESC+"33m"+A219+A219+" "+ESC+"31m"+A223+ESC+"41m    "+ESC+"1m"+A219+A178+A177+A176+"         "+ESC+"0;37;40m "+ESC+"31;41m "+A178+A177+A176+ESC+"40m"+A220+" "+ESC+"1;41m"+A176+ESC+"0;37;40m  "+ESC+"31;41m "+A176+A177+" "+A219+ESC+"0m\n"
		thismsg += "                  "+A220+ESC+"1m"+A219+" "+A219+A221+" "+A223+"   "+A220+" "+A223+A220+" "+ESC+"0;31m"+A220+ESC+"41m  "+ESC+"40m"+A223+A220+ESC+"41m  "+ESC+"40m"+A223+" "+ESC+"1;33;43m"+A177+A176+ESC+"0;33m"+A219+A219+" "+ESC+"31m"+A223+ESC+"41m    "+ESC+"1m"+A219+A178+A177+A176+"        "+ESC+"0;31m"+A219+A220+A222+ESC+"1;41m"+A219+A177+A176+ESC+"0;31m"+A220+ESC+"1;41m"+A176+ESC+"0;37;40m "+ESC+"31m"+A220+ESC+"41m "+ESC+"1m"+A176+" "+A178+A219+ESC+"0m\n"
		thismsg += "                   "+A223+ESC+"1m"+A220+" "+A223+"  "+A220+A223+A220+" "+A223+" "+A223+ESC+"0;31m"+A220+ESC+"41m "+ESC+"40m"+A223+A223+A220+ESC+"41m  "+ESC+"40m"+A223+" "+ESC+"1;33m"+A223+ESC+"43m"+A219+A219+ESC+"40m"+A223+ESC+"0;33m"+A220+A219+" "+ESC+"31;41m    "+ESC+"1m"+A219+A178+A177+A176+"          "+ESC+"0;31m"+A222+ESC+"41m "+ESC+"1m"+A177+A177+A176+ESC+"0;31m"+A223+" "+ESC+"41m "+ESC+"1m"+A176+A177+A178+"  "+ESC+"0m\n"
		thismsg += ESC+"37m                       "+ESC+"1m"+A220+" "+ESC+"0;31m"+A220+A220+A220+A220+A220+ESC+"41m   "+ESC+"40m"+A220+A220+ESC+"41m  "+ESC+"40m"+A223+ESC+"37m     "+ESC+"1;33;43m"+A177+A176+ESC+"0;33m"+A219+A219+A220+" "+ESC+"31;41m    "+ESC+"1m"+A219+A178+A177+A176+"         "+ESC+"0;31m"+A220+A222+ESC+"41m "+ESC+"1m"+A176+A176+ESC+"0;37;40m "+ESC+"31;41m  "+A176+A177+A178+" "+A219+ESC+"0m\n"
		thismsg += ESC+"37m                       "+ESC+"30mÙ"+ESC+"31m"+A222+ESC+"41m  "+ESC+"1m"+A177+A177+A176+A176+"  "+ESC+"0;31m"+A223+A223+ESC+"37m        "+ESC+"1;33m"+A223+ESC+"43m"+A219+ESC+"0;33m"+A223+A223+A223+A220+" "+ESC+"31;41m    "+ESC+"1m"+A219+A178+A177+A176+"         "+ESC+"0;31m"+A220+A222+A223+" "+A220+ESC+"41m "+ESC+"1m"+A177+A176+"  "+A219+" "+ESC+"0m\n"
		thismsg += ESC+"37m                         "+ESC+"31m"+A223+A223+A223+A223+A223+A223+A223+ESC+"37m            "+ESC+"1;33m"+A220+A220+ESC+"43m"+A176+ESC+"0;33m"+A219+A219+" "+ESC+"31;41m    "+ESC+"1m"+A219+A178+A177+A176+"         "+ESC+"0;37;40m "+ESC+"31m"+A220+ESC+"1;41m"+A176+A177+A178+A176+A176+"  "+A219+ESC+"0;37;40m  "+ESC+"0m\n"
		thismsg += "                                            "+ESC+"1;33;43m"+A219+A178+A177+A176+ESC+"0;33m"+A219+" "+ESC+"31m"+A223+ESC+"41m    "+ESC+"1m"+A219+A178+A177+A176+"        "+ESC+"0;31m"+A220+" "+A223+ESC+"1;41m"+A176+A177+A177+"  "+ESC+"0;31m"+A223+ESC+"37m   "+ESC+"0m\n"
		thismsg += "                                            "+ESC+"1;33;43m"+A219+A178+ESC+"40m"+A223+ESC+"0;33m"+A223+A223+A220+A220+" "+ESC+"31;41m   "+ESC+"1m"+A219+A178+A177+A177+A176+"         "+ESC+"0;31m"+A220+" "+A223+ESC+"1;41m"+A177+A177+ESC+"0;37;40m  "+ESC+"31;41m   "+ESC+"0m\n"
		thismsg += ESC+"37m                                            "+ESC+"1;33m"+A220+A220+ESC+"43m"+A219+A178+A177+A176+ESC+"0;33m"+A219+A220+" "+ESC+"31;41m   "+ESC+"1m"+A219+A178+A177+A177+A176+"          "+ESC+"0;37;40m "+ESC+"31m"+A223+ESC+"41m  "+ESC+"37;40m "+ESC+"31;41m   "+ESC+"0m\n"
		thismsg += ESC+"37m                                           "+ESC+"1;33m"+A220+ESC+"43m"+A219+ESC+"40m"+A223+A223+A223+ESC+"0;33m"+A223+A220+A220+A220+" "+ESC+"31;41m     "+ESC+"1m"+A178+A177+A176+ESC+"0;31m"+A223+A223+A223+A223+ESC+"41m       "+ESC+"40m"+A220+" "+ESC+"41m "+ESC+"40m"+A220+" "+A223+ESC+"41m "+ESC+"0m\n"
		thismsg += ESC+"37m                                           "+ESC+"1;33m"+A220+A220+ESC+"43m"+A219+A219+A178+A177+A176+ESC+"0;33m"+A219+A219+" "+ESC+"31m"+A223+A223+" "+A220+A220+A220+A220+A220+ESC+"41m   "+ESC+"40m"+A220+" "+ESC+"41m       "+ESC+"40m"+A220+" "+ESC+"41m  "+ESC+"40m"+A220+A220+ESC+"0m\n"
		thismsg += ESC+"37m                                           "+ESC+"1;33;43m"+A219+A219+ESC+"40m"+A223+A223+A223+ESC+"0;33m"+A223+A223+ESC+"31m"+A220+A220+ESC+"41m   "+ESC+"1m"+A176+A178+A177+" "+A176+"     "+ESC+"0;31m"+A220+" "+ESC+"41m       "+ESC+"37;40m "+ESC+"31m"+A223+ESC+"41m   "+ESC+"0m\n"
		thismsg += ESC+"37m                                           "+ESC+"1;33m"+A220+ESC+"43m"+A178+ESC+"0;33m"+A220+A219+A223+" "+ESC+"31;41m     "+ESC+"1m"+A176+A178+A177+A177+A176+A176+A176+"     "+ESC+"0;31m"+A220+" "+A223+ESC+"41m      "+ESC+"37;40m "+ESC+"31;41m   "+ESC+"0m\n"
		thismsg += ESC+"37m                                          "+ESC+"1;33;43m"+A178+A177+A176+ESC+"0;33m"+A223+A223+" "+ESC+"31;41m     "+ESC+"1m"+A176+A178+A178+" "+A177+" "+A176+A176+"       "+ESC+"0;37;40m "+ESC+"31;41m      "+ESC+"37;40m "+ESC+"31m"+A223+ESC+"41m  "+ESC+"0m\n"
		thismsg += ESC+"37m                                         "+ESC+"1;33m"+A220+A220+ESC+"0;33m"+A220+A220+A223+" "+ESC+"31;41m    "+ESC+"1m"+A176+A219+A178+A178+A177+A177+A176+" "+A176+" "+A176+A176+"     "+ESC+"0;31m"+A220+" "+ESC+"41m      "+ESC+"37;40m "+ESC+"31;41m  "+ESC+"0m\n"
		thismsg += ESC+"37m                         "+ESC+"0;37m               "+ESC+"1;33m"+A223+A223+A223+ESC+"0;33m"+A223+"  "+ESC+"30;41m  "+ESC+"1;31mShatterstar [W/X]     "+ESC+"0;37;40m "+ESC+"30;41m      "+ESC+"37;40m "+ESC+"30;41m "+ESC+"0m\n"
		thismsg += ESC+"37m                                                                               "+ESC+"0m\n"
		return thismsg

	""" Abdul's Armoury, Opening Screen """
	def abdul(self):
		thismsg  = ESC+"1;33m"+A220+A220+A220+A220+ESC+"0;33m"+A220+A220+ESC+"1m"+A220+A220+ESC+"0;33m"+A220+ESC+"1m"+A220+A220+A220+ESC+"0;33m"+A220+ESC+"1m"+A220+A220+ESC+"0;33m"+A220+ESC+"1m"+A220+ESC+"0;33m"+A220+A220+ESC+"1m"+A220+ESC+"0;33m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"1;30m"+A220+ESC+"C"+ESC+"0;33m"+A220+A220+A220+A220+"\n"
		thismsg += ESC+"A"+ESC+"79C"+A220+ESC+"1;43m"+A219+A178+ESC+"0;33m"+A219+A219+A219+A223+A219+A219+A223+ESC+"32m"+A220+ESC+"33m"+A223+ESC+"32m"+A220+ESC+"C"+A254+ESC+"33m"+A219+A219+A219+A219+A219+A219+A219+A219+A219+ESC+"1;30;43m"+A176+ESC+"C"+ESC+"0;33m"+A219+ESC+"1;43m"+A177+A176+ESC+"C"+A176+ESC+"C"+ESC+"37;40mSaga"+ESC+"Cof"+ESC+"Cthe"+ESC+"CRed"+ESC+"CDragon"+ESC+"C-"+ESC+"C"+ESC+"33mAbduls"+ESC+"CArmour    "+ESC+"C"+ESC+"0;33m"+A223+"\n"
		thismsg += ESC+"1;43m"+A219+ESC+"0;33m"+A219+A219+A223+ESC+"32m"+A220+ESC+"1;42m"+A177+ESC+"0;32m"+A220+ESC+"C"+A223+ESC+"1m"+A223+ESC+"2C"+ESC+"0;33m"+A223+A223+A223+ESC+"30;43m"+A177+A176+ESC+"33;40m"+A219+A219+A219+A219+A219+A219+ESC+"1;30;43m"+A176+ESC+"2C"+ESC+"0;33m"+A223+A219+ESC+"C"+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+"\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"1;30;43m"+A176+ESC+"33m"+A219+ESC+"0;33m"+A219+A219+A219+A220+ESC+"32m"+A223+ESC+"33m"+A220+A219+A223+ESC+"37m"+A220+ESC+"1;47m"+A176+ESC+"0m"+A219+A223+ESC+"1;30;47m"+A176+A176+ESC+"40m"+A220+A220+ESC+"0;33m"+A223+ESC+"30;43m"+A177+A176+ESC+"33;40m"+A219+A219+A219+ESC+"1;30;43m"+A177+ESC+"C"+ESC+"0;33m"+A220+ESC+"1;30m"+A223+ESC+"4C"+ESC+"0;33mBehind"+ESC+"Cthe"+ESC+"Cdesk"+ESC+"Cof"+ESC+"Cthe"+ESC+"Carmour"+ESC+"Cshop"+ESC+"Cis"+ESC+"Can\n"
		thismsg += ESC+"1;43m"+A219+ESC+"0;33m"+A219+A219+A219+A219+ESC+"30;43m"+A176+A177+ESC+"C"+ESC+"37;40m"+A223+ESC+"1;47m"+A177+A176+ESC+"C"+ESC+"0m"+A219+A219+A219+ESC+"1;30;47m"+A176+A177+A178+ESC+"C"+ESC+"0;30;43m"+A177+A176+ESC+"33;40m"+A219+A219+ESC+"1;30;43m"+A178+ESC+"C"+ESC+"40m"+A223+A220+ESC+"4C"+ESC+"0;33mamazingly"+ESC+"Cattractive"+ESC+"Clooking"+ESC+"Cfemale - she seems\n"
		thismsg += ESC+"1;43m"+A219+ESC+"0;33m"+A219+A219+ESC+"30;43m"+A176+A177+ESC+"33;40m"+A223+ESC+"1;37m"+A220+ESC+"47m"+A177+A176+ESC+"0m"+A220+A220+A220+A220+A220+ESC+"1;30m"+A220+A220+A223+ESC+"47m"+A177+A178+ESC+"C"+ESC+"0;30;43m"+A177+A176+ESC+"33;40m"+A219+ESC+"1;30;43m"+A219+ESC+"2C"+ESC+"0;32m"+A220+A254+ESC+"3C"+ESC+"33mbusy, doing her mails but she"+ESC+"Casks"+ESC+"C\""+ESC+"1mHow\n"
		thismsg += ESC+"43m"+A219+ESC+"0;33m"+A223+A219+ESC+"30;43m"+A176+A177+ESC+"C"+ESC+"1;37;47m"+A178+ESC+"40m"+A222+A222+ESC+"47m"+A176+ESC+"C"+ESC+"30m"+A176+ESC+"C"+A177+ESC+"40m"+A220+ESC+"47m"+A178+ESC+"40m"+A223+A220+ESC+"47m"+A219+ESC+"C"+ESC+"0;30;43m"+A177+A176+ESC+"33;40m"+A223+ESC+"32m"+A220+A178+ESC+"6C"+ESC+"1;33mmay"+ESC+"CI"+ESC+"Cbe"+ESC+"Cof"+ESC+"Cservice?"+ESC+"0;33m\"\n"
		thismsg += ESC+"1m"+A220+ESC+"0;33m"+A223+ESC+"C"+A220+A220+ESC+"C"+ESC+"1;37m"+A223+ESC+"47m"+A178+ESC+"0m"+A220+ESC+"1;47m"+A177+ESC+"0m"+A220+ESC+"1;30;47m"+A176+ESC+"0m"+A220+ESC+"1;30m"+A223+A223+A220+ESC+"47m"+A177+A178+ESC+"C"+ESC+"0;30;43m"+A177+ESC+"33;40m"+A223+ESC+"32m"+A220+ESC+"1;42m"+A176+ESC+"0;32m"+A220+"\n"
		thismsg += ESC+"1;33;43m"+A219+ESC+"0;33m"+A219+A220+A223+ESC+"C"+A220+ESC+"1;43m"+A176+ESC+"0;33m"+A220+ESC+"1;37m"+A223+ESC+"0m"+A220+ESC+"2C"+A220+A219+ESC+"1;30;47m"+A176+A176+ESC+"40m"+A223+ESC+"47m"+A219+ESC+"C"+ESC+"0;30;43m"+A177+A176+ESC+"33;40m"+A220+ESC+"32m"+A223+ESC+"1;30m"+A220+ESC+"7C"+ESC+"0;33m["+ESC+"1mB"+ESC+"0;33m]"+ESC+"1muy"+ESC+"CArmour\n"
		thismsg += ESC+"43m"+A219+ESC+"0;33m"+A219+A219+A219+A220+A223+ESC+"1;37m"+A220+A220+ESC+"0m"+A223+ESC+"C"+ESC+"1;47m"+A223+ESC+"0m"+A219+A220+A220+A220+A220+ESC+"1;30;47m"+A176+A177+ESC+"40m"+A220+ESC+"0;33m"+A223+A223+ESC+"30;43m"+A177+A176+ESC+"1;40m"+A219+ESC+"7C"+ESC+"0;33m["+ESC+"1mS"+ESC+"0;33m]"+ESC+"1mell"+ESC+"CArmour\n"
		thismsg += ESC+"43m"+A219+ESC+"0;33m"+A219+ESC+"30;43m"+A176+A177+ESC+"C"+ESC+"1;37;47m"+A219+A178+ESC+"40m"+A220+ESC+"47m"+A177+A176+ESC+"0m"+A220+A220+A220+A220+A219+A220+A223+ESC+"1;30m"+A220+A220+A219+A219+A220+ESC+"0;33m"+A223+ESC+"1;30m"+A219+ESC+"7C"+ESC+"0;33m["+ESC+"1mY"+ESC+"0;33m]"+ESC+"1mour"+ESC+"CStats\n"
		thismsg += ESC+"43m"+A178+ESC+"0;33m"+A223+A220+A223+ESC+"30;43m"+A176+A223+ESC+"1;37;40m"+A223+A223+ESC+"47m"+A178+A177+A176+A176+ESC+"0m"+A219+A219+A223+ESC+"1;30m"+A220+A176+A177+A178+A223+A223+ESC+"0;33m"+A220+A219+ESC+"1;30m"+A219+ESC+"7C"+ESC+"0;33m["+ESC+"1mR"+ESC+"0;33m]"+ESC+"1meturn"+ESC+"Cto"+ESC+"CTown\n"
		thismsg += ESC+"43m"+A177+ESC+"0;33m"+A219+A220+A219+A219+A223+ESC+"32m"+A220+ESC+"1;42m"+A176+ESC+"0;32m"+A220+ESC+"C"+ESC+"33m"+A220+A220+A220+A220+A220+A220+ESC+"C"+A220+A220+A219+ESC+"30;43m"+A176+ESC+"33;40m"+A219+A219+ESC+"1;30m"+A223+ESC+"0;33m"+A220+A254+ESC+"C"+ESC+"1;30m"+A220+A223+"\n"
		thismsg += ESC+"33;43m"+A176+ESC+"0;33m"+A219+A219+A219+A219+A219+A220+ESC+"32m"+A223+ESC+"C"+A178+A254+ESC+"33m"+A219+ESC+"30;43m"+A177+A176+ESC+"33;40m"+A223+A220+ESC+"1;43m"+A176+ESC+"0;33m"+A220+A223+A220+A223+A223+A220+ESC+"3C"+ESC+"1;30m"+A177+A220+ESC+"2C"+ESC+"33m"+A220+A220+ESC+"0;33m"+A220+A220+ESC+"1m"+A220+ESC+"0;33m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+"\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"1;30;43m"+A176+ESC+"33m"+A176+ESC+"0;33m"+A219+A219+A219+A219+A219+A219+A219+A219+A220+A220+ESC+"32m"+A254+ESC+"33m"+A223+A219+A219+A220+A223+A220+A220+A223+A223+ESC+"1;30m"+A220+A220+A219+ESC+"2C"+A220+A178+A220+ESC+"C"+ESC+"33;43m"+A177+ESC+"2C"+ESC+"0m                      "+ESC+"3C"+ESC+"33m"+A220+"\n"
		thismsg += A223+A223+A223+ESC+"1;30m"+A223+ESC+"0;33m"+A223+A223+ESC+"1;30m"+A223+ESC+"0;33m"+A223+ESC+"1;30m"+A223+A223+ESC+"0;33m"+A223+ESC+"1;30m"+A223+A223+A223+ESC+"0;33m"+A223+ESC+"1;30m"+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+ESC+"C"+ESC+"0;33m"+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+ESC+"1;30m"+A223+ESC+"C"+ESC+"0;33m"+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+"\n"
		thismsg += ESC+"A"+ESC+"79C"+A223+ESC+"0m\n"
		return thismsg

	"""Abdul's Armoury, Buy Screen"""
	def armbuy(self):
		thismsg  = ESC+"12C"+ESC+"1;33m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"0;33m"+A220+ESC+"1m"+A220+A220+A220+ESC+"0;33m"+A220+ESC+"1m"+A220+ESC+"0;33m"+A220+A220+ESC+"1m"+A220+ESC+"0;33m"+A220+ESC+"1m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+"\n"
		thismsg += ESC+"12C"+ESC+"47m"+A178+ESC+"40m"+A223+ESC+"2C"+ESC+"37m The"+ESC+"CSaga"+ESC+"Cof"+ESC+"Cthe"+ESC+"CRed"+ESC+"CDragon"+ESC+"C-"+ESC+"C"+ESC+"33mArmour"+ESC+"CList "+ESC+"2C"+A220+ESC+"47m"+A178+ESC+"40m\n"
		thismsg += ESC+"12C"+ESC+"47m"+A178+A219+ESC+"40m"+A223+A223+A223+A223+A223+A223+A223+ESC+"0;33m"+A223+ESC+"1m"+A223+A223+A223+A223+ESC+"0;33m"+A223+ESC+"1m"+A223+A223+A223+ESC+"0;33m"+A223+ESC+"1m"+A223+A223+ESC+"0;33m"+A223+ESC+"1m"+A223+ESC+"0;33m"+A223+A223+ESC+"1m"+A223+ESC+"0;33m"+A223+ESC+"1m"+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+ESC+"47m"+A178+A178+ESC+"40m\n"
		thismsg += ESC+"12C"+ESC+"43m"+A219+ESC+"4C"+ESC+"40mArmour"+ESC+"25CPrice"+ESC+"8C"+A219+"\n"
		thismsg += ESC+"12C"+ESC+"43m"+A219+ESC+"2C"+ESC+"0;33m1."+ESC+"CCoat"+ESC+"1;30m..................................."+ESC+"33m200"+ESC+"C"+A219+"\n"
		thismsg += ESC+"12C"+ESC+"43m"+A219+ESC+"2C"+ESC+"0;33m2."+ESC+"CHeavy"+ESC+"CCoat"+ESC+"1;30m..........................."+ESC+"33m1,000"+ESC+"C"+A219+"\n"
		thismsg += ESC+"12C"+ESC+"43m"+A219+ESC+"2C"+ESC+"0;33m3."+ESC+"CLeather"+ESC+"CVest"+ESC+"1;30m........................."+ESC+"33m3,000"+ESC+"C"+ESC+"43m"+A178+ESC+"40m\n"
		thismsg += ESC+"12C"+ESC+"43m"+A178+ESC+"2C"+ESC+"0;33m4."+ESC+"CBronze"+ESC+"CArmour"+ESC+"1;30m......................."+ESC+"33m10,000"+ESC+"C"+ESC+"43m"+A177+ESC+"40m\n"
		thismsg += ESC+"12C"+ESC+"43m"+A177+ESC+"2C"+ESC+"0;33m5."+ESC+"CIron"+ESC+"CArmour"+ESC+"1;30m........................."+ESC+"33m30,000"+ESC+"C"+ESC+"43m"+A176+ESC+"40m\n"
		thismsg += ESC+"12C"+ESC+"0;33m"+A223+ESC+"2C6."+ESC+"CGraphite"+ESC+"CArmour"+ESC+"1;30m...................."+ESC+"33m100,000"+ESC+"C"+ESC+"0;33m"+A223+"\n"
		thismsg += ESC+"12C"+A176+ESC+"2C7."+ESC+"CErdrick's"+ESC+"CArmour"+ESC+"1;30m..................."+ESC+"33m150,000"+ESC+"C"+ESC+"0;33m"+A176+"\n"
		thismsg += ESC+"12C"+A177+ESC+"2C8."+ESC+"CArmour"+ESC+"Cof"+ESC+"CDeath"+ESC+"1;30m...................."+ESC+"33m200,000"+ESC+"C"+ESC+"0;33m"+A177+"\n"
		thismsg += ESC+"12C"+A178+ESC+"2C9."+ESC+"CAble's"+ESC+"CArmour"+ESC+"1;30m......................"+ESC+"33m400,000"+ESC+"C"+ESC+"0;33m"+A178+"\n"
		thismsg += ESC+"12C"+A219+ESC+"C10."+ESC+"CFull"+ESC+"CBody"+ESC+"CArmour"+ESC+"1;30m................."+ESC+"33m1,000,000"+ESC+"C"+ESC+"0;33m"+A219+"\n"
		thismsg += ESC+"12C"+A223+ESC+"C11."+ESC+"CBlood"+ESC+"CArmour"+ESC+"1;30m....................."+ESC+"33m4,000,000"+ESC+"C"+ESC+"0;33m"+A219+"\n"
		thismsg += ESC+"12C"+A219+ESC+"C12."+ESC+"CMagic"+ESC+"CProtection"+ESC+"1;30m................"+ESC+"33m10,000,000"+ESC+"C"+ESC+"0;33m"+A220+"\n"
		thismsg += ESC+"12C"+A219+ESC+"C13."+ESC+"CBelar's"+ESC+"CMail"+ESC+"1;30m...................."+ESC+"33m40,000,000"+ESC+"C"+ESC+"0;33m"+A219+"\n"
		thismsg += ESC+"12C"+A219+ESC+"C14."+ESC+"CGolden"+ESC+"CArmour"+ESC+"1;30m.................."+ESC+"33m100,000,000"+ESC+"C"+ESC+"0;33m"+A219+"\n"
		thismsg += ESC+"12C"+A219+ESC+"C15."+ESC+"CArmour"+ESC+"COf"+ESC+"CLore"+ESC+"1;30m................."+ESC+"33m400,000,000"+ESC+"C"+ESC+"43m"+A176+ESC+"40m\n"
		thismsg += ESC+"12C"+ESC+"43m"+A176+ESC+"0;33m"+A219+A220+A220+A220+A220+A220+A220+A178+A220+A220+A220+A176+A220+A220+A178+A220+ESC+"C"+A220+A220+A220+A220+A178+A220+A220+A220+ESC+"C"+A220+A220+A221+A220+A220+A220+A220+A178+A220+A220+A176+ESC+"C"+A220+A220+A220+A220+A178+A220+A220+A220+A220+A219+ESC+"1;43m"+A176+ESC+"40m"+ESC+"0m\n"
		return thismsg


	""" King Arthur's Weapons, Opening Screen """
	def arthur(self):
		thismsg = ESC+"34m"+A220+ESC+"1;44m"+A176+ESC+"0;34m"+A220+A223+A176+ESC+"C"+A178+A176+A254+ESC+"2C"+A220+A254+ESC+"6C"+A220+A178+ESC+"C"+A220+A178+ESC+"C"+ESC+"1;44m"+A177+ESC+"40m"+A223+ESC+"0;34m"+A223+ESC+"1m"+A223+A223+ESC+"0;34m"+A223+ESC+"1m"+A223+ESC+"0;34m"+A223+A223+A223+A223+ESC+"1m"+A223+ESC+"0;34m"+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+ESC+"C"+A223+"\n"
		thismsg += ESC+"C"+A223+ESC+"2C"+A176+A223+A223+ESC+"1;37m"+A220+A220+A220+A220+ESC+"0m"+A220+ESC+"1m"+A223+A223+ESC+"0m"+A223+ESC+"1m"+A223+A223+ESC+"0m"+A223+ESC+"1m"+A223+A220+ESC+"0m"+A220+A220+A220+A220+ESC+"C"+ESC+"34m"+A223+ESC+"3C"+ESC+"1;37mSaga"+ESC+"Cof"+ESC+"Cthe"+ESC+"CRed"+ESC+"CDragon"+ESC+"C-"+ESC+"C"+ESC+"34mKing"+ESC+"CArthurs"+ESC+"CWeapons    "+ESC+"C"+ESC+"0;34m"+A219+"\n"
		thismsg += A223+ESC+"1;37m"+A220+A223+A223+A223+A223+A223+ESC+"C"+ESC+"0m"+A220+A220+A220+A220+A220+A219+A219+A219+ESC+"30;47m"+A223+ESC+"37;40m"+A219+A220+A220+A220+A220+A220+ESC+"C"+A223+ESC+"1;30m"+A223+ESC+"0m"+A223+ESC+"1;30m"+A223+A223+A220+ESC+"4C"+ESC+"0;34m"+A220+A220+A220+A220+ESC+"C"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"C"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A178+A220+A220+A220+A220+ESC+"C"+A220+A220+"\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"1m"+A219+ESC+"C"+A220+ESC+"47m"+A219+A219+A223+A178+A177+A176+ESC+"0m"+A219+A223+ESC+"1m"+A220+ESC+"0m"+A223+A219+A219+ESC+"30;47m"+A223+A176+ESC+"37;40m"+A219+A219+A223+A220+A223+A219+A219+A219+A219+A219+A219+A220+ESC+"C"+ESC+"1;30;47m"+A178+ESC+"C"+ESC+"0;34m"+A176+ESC+"3C"+A178+ESC+"20C"+A223+ESC+"17C"+ESC+"1m"+A220+A220+A220+A220+"\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"0m "+ESC+"1m"+A219+ESC+"C"+ESC+"47m"+A219+A219+A178+ESC+"0m"+A219+ESC+"30;47m"+A176+ESC+"37;40m"+A219+A219+A219+ESC+"C"+ESC+"1m"+A219+ESC+"47m"+A178+ESC+"40m"+A220+ESC+"0m"+A223+A219+A219+A223+A220+ESC+"1;47m"+A176+ESC+"0m"+A219+ESC+"C"+A219+A219+ESC+"1;47m"+A176+A176+A176+A176+ESC+"30m"+A176+ESC+"C"+ESC+"40m"+A219+ESC+"3C"+ESC+"0;34mYou"+ESC+"Cwalk"+ESC+"Cinto"+ESC+"Cthe"+ESC+"Cwell"+ESC+"Cknown"+ESC+"Cweapons"+ESC+"6C"+ESC+"1m"+A219+ESC+"44m"+A178+ESC+"0;34m"+A219+"\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"1m"+A219+ESC+"C"+ESC+"47m"+A178+A178+A178+" "+ESC+"0;30;47m"+A223+A177+ESC+"37;40m"+A219+A219+A219+ESC+"C"+ESC+"1m"+A219+ESC+"C"+ESC+"47m"+A178+ESC+"40m"+A220+ESC+"C"+ESC+"47m"+A177+A176+" "+ESC+"C"+ESC+"0m"+A219+ESC+"1;47m"+A176+A176+A177+A177+A177+A176+ESC+"30m"+A176+ESC+"C"+ESC+"40m"+A219+ESC+"3C"+ESC+"0;34mshop,"+ESC+"Cyou"+ESC+"Cpause"+ESC+"Cto"+ESC+"Clook"+ESC+"Caround"+ESC+"Cat"+ESC+"Call"+ESC+"Cof"+ESC+"2C"+A222+ESC+"1;44m"+A177+ESC+"0;34m"+A219+"\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"1m"+A219+ESC+"C"+A223+ESC+"47m"+A178+A177+ESC+"0m"+A219+A219+A219+A219+A219+A219+A219+ESC+"C"+ESC+"1m"+A219+ESC+"C"+ESC+"47m"+A178+A177+ESC+"0m"+A220+A223+A220+ESC+"1;47m"+A176+A176+A177+A177+A176+A176+A176+ESC+"30m"+A176+ESC+"0m"+A223+ESC+"C"+ESC+"1;30m"+A219+ESC+"3C"+ESC+"0;34mthe"+ESC+"Cmany"+ESC+"Cimplements"+ESC+"Cof"+ESC+"Cdestruction."+ESC+"2CA"+ESC+"37m "+ESC+"4C"+ESC+"1;34;44m"+A176+ESC+"0;34m"+A219+"\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"C "+ESC+"1m"+A219+ESC+"C"+ESC+"47m"+A177+A176+ESC+"0m"+A219+A219+A219+A219+A219+A219+A223+ESC+"1m"+A220+ESC+"C"+ESC+"47m"+A178+ESC+"40m"+A220+A223+ESC+"47m"+A177+A176+ESC+"0m"+A220+A223+ESC+"1;47m"+A177+A176+A176+ESC+"0m"+A219+ESC+"30;47m"+A220+A176+ESC+"1m"+A177+ESC+"C"+ESC+"40m"+A178+ESC+"4C"+ESC+"0;34mfat"+ESC+"Cman"+ESC+"Cwoddles"+ESC+"Cinto"+ESC+"Cthe"+ESC+"Croom,"+ESC+"Cand"+ESC+"2C  "+ESC+"37m   "+ESC+"2C"+ESC+"1;34;44m"+A176+ESC+"0;30;44m"+A176+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"C "+ESC+"1m"+A219+ESC+"C"+ESC+"47m"+A176+" "+ESC+"0m"+A219+A219+A223+ESC+"33m"+A220+ESC+"37m"+A223+ESC+"1m"+A220+ESC+"47m"+A178+A178+A177+ESC+"0m"+A220+ESC+"1m"+A223+ESC+"47m"+A177+A176+ESC+"0;30;47m"+A176+A223+ESC+"1m"+A176+ESC+"0m"+A220+A223+ESC+"33m"+A220+ESC+"37m"+A223+A219+A219+ESC+"1;30;47m"+A178+ESC+"C"+ESC+"40m"+A178+ESC+"4C"+ESC+"0;34masks"+ESC+"C\""+ESC+"1mWadaya"+ESC+"Cwant"+ESC+"Ckid?"+ESC+"0;34m\""+ESC+"17C"+ESC+"37m "+ESC+"2C"+ESC+"1;34;44m"+A176+ESC+"0;30;44m"+A176+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"C "+ESC+"1m"+A219+ESC+"C"+ESC+"47m"+A176+ESC+"0m"+A219+ESC+"30;47m"+A254+A176+ESC+"37;40m"+A223+ESC+"1;33m"+A220+ESC+"43m"+A177+ESC+"0;33m"+A220+ESC+"1;37m"+A223+ESC+"47m"+A177+A176+ESC+"0m"+A223+A220+A220+A223+A223+ESC+"1;47m "+ESC+"0m"+A223+ESC+"33m"+A220+ESC+"1;43m"+A177+ESC+"C"+ESC+"0m"+A219+A219+ESC+"1;30m"+A219+A223+ESC+"C"+A178+ESC+"47C"+ESC+"0;34m"+A219+ESC+"30;44m"+A177+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"34m"+A176+ESC+"C "+ESC+"1;37;47m"+A178+ESC+"C"+A176+ESC+"0m"+A223+ESC+"1;33m"+A220+ESC+"43m"+A178+ESC+"40m"+A223+ESC+"C"+ESC+"43m"+A176+ESC+"0;33m"+A223+A220+ESC+"C"+ESC+"1;37;47m"+A177+A177+A176+ESC+"0m"+A219+A223+ESC+"1;33m"+A220+ESC+"43m"+A178+ESC+"C"+ESC+"0;33m"+A223+ESC+"1;43m"+A176+ESC+"0;33m"+A220+ESC+"37m"+A223+ESC+"1;30m"+A219+ESC+"C"+A178+ESC+"6C"+ESC+"0;34m["+ESC+"1mB"+ESC+"0;34m]"+ESC+"1muy"+ESC+"CWeapon"+ESC+"30C"+ESC+"0;34m"+A219+ESC+"30;44m"+A177+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"34m"+A178+ESC+"C "+ESC+"1;37;47m"+A177+ESC+"2C"+ESC+"40m"+A223+ESC+"33m"+A219+A220+ESC+"0;33m"+A178+A223+ESC+"37m"+A220+A219+A220+ESC+"1;47m"+A177+A176+A176+ESC+"0m"+A219+A220+ESC+"1m"+A223+ESC+"0m"+A220+A220+ESC+"1;33m"+A223+A220+A220+ESC+"43m"+A177+ESC+"0;33m"+A223+ESC+"2C"+ESC+"1;30m"+A219+ESC+"6C"+ESC+"0;34m["+ESC+"1mS"+ESC+"0;34m]"+ESC+"1mell"+ESC+"CWeapon"+ESC+"29C"+ESC+"0;34m"+A219+ESC+"30;44m"+A177+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"34m"+A176+A176+ESC+"C "+ESC+"1;37;47m"+A176+ESC+"C"+ESC+"0m"+A223+A220+A220+A220+A219+ESC+"1;47m"+A176+A176+A176+A176+ESC+"0;30;47m"+A176+ESC+"37;40m"+A219+A219+A219+A219+ESC+"1;30;47m"+A176+ESC+"0m"+A219+A219+A220+A220+ESC+"1;30m"+A220+A223+ESC+"C"+A219+ESC+"7C"+ESC+"0;34m["+ESC+"1mY"+ESC+"0;34m]"+ESC+"1mour"+ESC+"CStats"+ESC+"30C"+ESC+"0;34m"+A219+ESC+"30;44m"+A178+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"C"+ESC+"34m"+A176+ESC+"C   "+ESC+"37m"+A223+A220+ESC+"C"+A223+A223+A219+A219+A219+A219+A219+ESC+"30;47m"+A220+A177+ESC+"37;40m"+A219+A219+A219+ESC+"1;30;47m"+A220+A220+A178+ESC+"40m"+A223+A223+ESC+"C"+A220+A223+ESC+"0;34m"+A176+ESC+"7C["+ESC+"1mR"+ESC+"0;34m]"+ESC+"1meturn"+ESC+"Cto"+ESC+"CTown"+ESC+"25C"+ESC+"0;34m"+A222+ESC+"1;44m"+A177+ESC+"0;30;44m"+A178+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"34m"+A220+ESC+"1;44m"+A176+ESC+"0;34m"+A220+ESC+"C"+A178+A220+ESC+"37m"+A223+A223+A220+A220+ESC+"C"+A223+A223+A223+ESC+"1;30;47m"+A176+A177+A219+ESC+"40m"+A223+A223+A223+ESC+"C"+A220+A220+A223+A223+ESC+"C"+ESC+"0;34m"+A220+A219+A176+ESC+"47C"+A219+ESC+"1;44m"+A176+ESC+"0;30;44m"+A178+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"C"+ESC+"34m"+A223+ESC+"C"+A220+A254+A178+A219+A219+A220+A220+ESC+"37m"+A223+A223+A223+A220+ESC+"C"+ESC+"1;30m"+A223+ESC+"C"+A220+A223+A223+A223+ESC+"C"+ESC+"0;34m"+A176+A176+A223+A178+A178+A176+ESC+"2C"+ESC+"1;44m"+A176+ESC+"0;34m"+A223+A223+A223+A178+A223+A223+ESC+"C"+A223+A178+A223+ESC+"C"+A223+A223+ESC+"C"+A223+A176+ESC+"C"+A223+ESC+"C"+A223+A223+ESC+"C"+A223+A223+ESC+"30;44m"+A177+ESC+"19C"+ESC+"34;40m"+A223+A223+A223+A223+"\n"
		thismsg += ESC+"A"+ESC+"79C"+ESC+"37m "+ESC+"34m"+A177+A178+A219+A220+ESC+"C"+A176+A223+A178+A178+A178+A178+A223+A176+ESC+"C"+ESC+"37m"+A223+ESC+"1;30m"+A220+A223+ESC+"C"+ESC+"0;34m"+A223+A178+A176+ESC+"4C"+A176+ESC+"C"+A220+A219+ESC+"30;44m"+A176+" "+ESC+"34;40m"+A254+ESC+"37m                      "+ESC+"34m"+A220+ESC+"30;44m"+A176+A178+ESC+"34;40m"+A219+A219+A219+ESC+"30;44m"+A176+ESC+"34;40m"+A219+A220+A219+A219+A219+A219+A219+A222+A219+A219+"\n"
		return thismsg
		
	""" King Arthur's Weapons, Buy Screen """
	def wepbuy(self):
		thismsg  = ESC+"14C"+ESC+"1;34m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"0;34m"+A220+ESC+"1m"+A220+A220+A220+A220+ESC+"0;34m"+A220+ESC+"1m"+A220+ESC+"0;34m"+A220+A220+ESC+"1m"+A220+ESC+"0;34m"+A220+ESC+"1m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+"\n"
		thismsg += ESC+"14C"+ESC+"46m"+A178+ESC+"40m"+A223+ESC+"2C"+ESC+"37m The"+ESC+"CSaga"+ESC+"Cof"+ESC+"Cthe"+ESC+"CRed"+ESC+"CDragon"+ESC+"C-"+ESC+"C"+ESC+"34mWeapons"+ESC+"CList "+ESC+"C"+A220+ESC+"46m"+A178+ESC+"40m\n"
		thismsg += ESC+"14C"+ESC+"46m"+A178+ESC+"44m"+A219+ESC+"40m"+A223+A223+A223+A223+ESC+"0;34m"+A223+ESC+"1m"+A223+A223+A223+ESC+"0;34m"+A223+ESC+"1m"+A223+A223+ESC+"0;34m"+A223+ESC+"1m"+A223+ESC+"0;34m"+A223+A223+ESC+"1m"+A223+ESC+"0;34m"+A223+ESC+"1m"+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+ESC+"46m"+A178+A178+ESC+"40m\n"
		thismsg += ESC+"14C"+ESC+"46m"+A219+ESC+"2C"+ESC+"0;36mWeapons"+ESC+"27CPrice"+ESC+"7C"+ESC+"1;34;44m"+A219+ESC+"40m\n"
		thismsg += ESC+"14C"+ESC+"44m"+A219+ESC+"2C"+ESC+"40m1."+ESC+"CStick"+ESC+"0;34m.................................."+ESC+"36m200"+ESC+"C"+ESC+"1;34;44m"+A219+ESC+"40m\n"
		thismsg += ESC+"14C"+ESC+"44m"+A219+ESC+"2C"+ESC+"40m2."+ESC+"CDagger"+ESC+"0;34m..............................."+ESC+"36m1,000"+ESC+"C"+ESC+"1;34;44m"+A219+ESC+"40m\n"
		thismsg += ESC+"14C"+ESC+"44m"+A178+ESC+"2C"+ESC+"40m3."+ESC+"CShort"+ESC+"CSword"+ESC+"0;34m.........................."+ESC+"36m3,000"+ESC+"C"+ESC+"1;34;44m"+A178+ESC+"40m\n"
		thismsg += ESC+"14C"+ESC+"44m"+A177+ESC+"2C"+ESC+"40m4."+ESC+"CLong"+ESC+"CSword"+ESC+"0;34m.........................."+ESC+"36m10,000"+ESC+"C"+ESC+"1;34;44m"+A177+ESC+"40m\n"
		thismsg += ESC+"14C"+ESC+"44m"+A176+ESC+"2C"+ESC+"40m5."+ESC+"CHuge"+ESC+"CAxe"+ESC+"0;34m............................"+ESC+"36m30,000"+ESC+"C"+ESC+"1;34;44m"+A176+ESC+"40m\n"
		thismsg += ESC+"14C"+ESC+"0;34m"+A223+ESC+"2C"+ESC+"1m6."+ESC+"CBone"+ESC+"CCruncher"+ESC+"0;34m......................"+ESC+"36m100,000"+ESC+"C"+ESC+"34m"+A223+"\n"
		thismsg += ESC+"14C"+A176+ESC+"2C"+ESC+"1m7."+ESC+"CTwin"+ESC+"CSwords"+ESC+"0;34m........................"+ESC+"36m150,000"+ESC+"C"+ESC+"34m"+A176+"\n"
		thismsg += ESC+"14C"+A177+ESC+"2C"+ESC+"1m8."+ESC+"CPower"+ESC+"CAxe"+ESC+"0;34m.........................."+ESC+"36m200,000"+ESC+"C"+ESC+"34m"+A177+"\n"
		thismsg += ESC+"14C"+A178+ESC+"2C"+ESC+"1m9."+ESC+"CAble's"+ESC+"CSword"+ESC+"0;34m......................."+ESC+"36m400,000"+ESC+"C"+ESC+"34m"+A178+"\n"
		thismsg += ESC+"14C"+A219+ESC+"C"+ESC+"1m10."+ESC+"CWan's"+ESC+"CWeapon"+ESC+"0;34m....................."+ESC+"36m1,000,000"+ESC+"C"+ESC+"34m"+A219+"\n"
		thismsg += ESC+"14C"+A223+ESC+"C"+ESC+"1m11."+ESC+"CSpear"+ESC+"COf"+ESC+"CGold"+ESC+"0;34m...................."+ESC+"36m4,000,000"+ESC+"C"+ESC+"34m"+A219+"\n"
		thismsg += ESC+"14C"+A219+ESC+"C"+ESC+"1m12."+ESC+"CCrystal"+ESC+"CShard"+ESC+"0;34m..................."+ESC+"36m10,000,000"+ESC+"C"+ESC+"34m"+A220+"\n"
		thismsg += ESC+"14C"+A219+ESC+"C"+ESC+"1m13."+ESC+"CNiras's"+ESC+"CTeeth"+ESC+"0;34m..................."+ESC+"36m40,000,000"+ESC+"C"+ESC+"34m"+A219+"\n"
		thismsg += ESC+"14C"+A219+ESC+"C"+ESC+"1m14."+ESC+"CBlood"+ESC+"CSword"+ESC+"0;34m...................."+ESC+"36m100,000,000"+ESC+"C"+ESC+"34m"+A219+"\n"
		thismsg += ESC+"14C"+A219+ESC+"C"+ESC+"1m15."+ESC+"CDeath"+ESC+"CSword"+ESC+"0;34m...................."+ESC+"36m400,000,000"+ESC+"C"+ESC+"1;34;44m"+A176+ESC+"40m\n"
		thismsg += ESC+"14C"+ESC+"44m"+A176+ESC+"0;34m"+A219+A220+A220+A220+A220+A220+A178+ESC+"C"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A178+ESC+"C"+A220+A220+A220+ESC+"C"+A220+A220+ESC+"C"+A220+A176+ESC+"C"+A220+ESC+"C"+A220+A220+A220+A220+A178+A220+A220+A220+A220+A176+A220+A220+A219+ESC+"1;44m"+A176+ESC+"40m\n"
		thismsg += ESC+"0m\n";
		return thismsg

	""" Forest Fight Screen """
	def forest(self):
		thismsg  = ESC+"C"+ESC+"30m"+A220+ESC+"C"+A220+A220+ESC+"C"+A220+A220+A220+ESC+"C"+A220+A220+A220+A220+A220+A220+A178+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A178+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"C"+ESC+"37m"+A220+A220+ESC+"C"+ESC+"30m"+A220+A220+ESC+"C"+ESC+"32m"+A220+ESC+"2C"+A220+ESC+"1;42m"+A177+ESC+"0;32m"+A223+ESC+"C"+A219+ESC+"30;42m"+A176+ESC+"32;40m"+A220+ESC+"C"+ESC+"1;30m"+A220+A220+A220+"\n"
		thismsg += ESC+"2C"+ESC+"0;30;47m"+A219+ESC+"37;40m"+A220+A220+A178+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"30;47m"+A223+A223+A223+A223+A223+A223+A223+ESC+"37;40m"+A220+A220+ESC+"C"+ESC+"1;47m"+A222+ESC+"40m"+A219+ESC+"47m"+A178+ESC+"40m"+A178+ESC+"2C"+ESC+"32;42m"+A177+ESC+"0;32m"+A223+A219+ESC+"C"+ESC+"1;42m"+A176+ESC+"0;32m"+A220+A219+ESC+"1;42m"+A176+ESC+"0;32m"+A219+A223+ESC+"30;42m"+A177+ESC+"C"+ESC+"37;40m"+A220+ESC+"C"+ESC+"1;30m"+A223+A178+"\n"
		thismsg += ESC+"2C"+ESC+"0;30;47m"+A178+A177+A176+ESC+"37;40m"+A219+ESC+"1;47m  Saga of the Red Dragon"+ESC+"0m"+A219+ESC+"30;47m- Forest   "+A176+A177+ESC+"37;40m"+A220+ESC+"1m"+A223+ESC+"0m"+A223+A220+ESC+"C"+ESC+"1;32;42m"+A176+ESC+"0;32m"+A223+A220+ESC+"30;42m"+A176+A177+ESC+"32;40m"+A254+ESC+"33m"+A222+ESC+"32m"+A223+ESC+"33m"+A220+A223+ESC+"32m"+A223+ESC+"37m"+A220+A219+A219+A178+"\n"
		thismsg += ESC+"C"+A176+ESC+"C"+ESC+"30;47m"+A178+A177+A176+ESC+"37;40m"+A219+A219+ESC+"30;47m   "+ESC+"37;40m"+A223+ESC+"30;47m"+A176+"       "+ESC+"37;40m"+A178+ESC+"30;47m"+A220+A220+A220+A220+ESC+"37;40m"+A223+A223+A223+A223+A223+ESC+"30;47m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"37;40m"+A223+ESC+"30;47m"+A220+ESC+"C"+ESC+"32;40m"+A254+A223+A223+A223+A223+A223+ESC+"1;30m"+A223+A223+ESC+"C"+ESC+"0;30;43m"+A176+ESC+"33;40m"+A222+ESC+"C"+ESC+"37m"+A177+A178+A219+A219+A178+ESC+"C"+ESC+"1;30m"+A178+"\n"
		thismsg += ESC+"4C"+ESC+"0;30;47m"+A178+A177+A176+ESC+"37;40m"+A219+A219+A219+A220+ESC+"C"+A220+ESC+"30;47m"+A177+ESC+"37;40m"+A219+A219+ESC+"30;47m"+A223+A176+ESC+"37;40m"+A219+A223+A223+ESC+"30;47m"+A219+ESC+"42m"+A176+"                     "+A177+ESC+"47m"+A219+ESC+"37;40m"+A219+ESC+"30;47m"+A176+ESC+"37;40m"+A223+ESC+"30;47m"+A177+ESC+"C"+ESC+"1;33;43m "+ESC+"30;40m"+A221+ESC+"0m"+A222+A178+ESC+"C"+ESC+"30;43m"+A176+A177+ESC+"C"+ESC+"37;40m"+A178+A223+ESC+"32m"+A220+A220+ESC+"37m"+A223+ESC+"C"+ESC+"1;30m"+A219+"\n"
		thismsg += ESC+"4C"+A220+ESC+"2C"+A220+ESC+"C"+A220+A220+ESC+"C"+A220+A220+A220+ESC+"C"+A220+A220+A220+A220+ESC+"47m"+A223+ESC+"40m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"C"+A220+A178+ESC+"C"+ESC+"0;33m"+A220+ESC+"1;43m"+A176+ESC+"30m"+A222+ESC+"C"+ESC+"0;33m"+A220+ESC+"30;43m"+A176+ESC+"1;40m"+A220+ESC+"0;33m"+A223+A221+A220+ESC+"32m"+A223+ESC+"1;42m"+A176+ESC+"0;32m"+A223+A223+ESC+"1;30m"+A220+ESC+"47m"+A178+ESC+"40m\n"
		thismsg += ESC+"34C"+A223+"\n"
		thismsg += ESC+"2C"+ESC+"0;32mThe murky forest stands before you - a giant maw of gloomy darkness\n"
		thismsg += ESC+"2Cever beckoning."+ESC+"37m              \n\n"
		thismsg += func_normmenu("(L)ook for something to kill")
		thismsg += func_normmenu("(H)ealer's Hut")
		thismsg += func_normmenu("(R)eturn to town")
		return thismsg 

	""" Rescue maiden intermediate screen """
	def tower(self):
		thismsg  = ESC+"255D"+ESC+"0;1;44m                                                          "+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"58C"+ESC+"44m                  "+ESC+"40m\n"
		thismsg += ESC+"44m                                                                    "+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"68C"+ESC+"44m        "+ESC+"40m\n"
		thismsg += ESC+"44m                     "+ESC+"30m"+A219+" "+A219+" "+A219+" "+A219+" "+A219+" "+ESC+"0;44m"+A219+" "+A219+" "+A219+" "+ESC+"1m"+A219+" "+A219+"            "+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"52C"+ESC+"44m                        "+ESC+"40m\n"
		thismsg += ESC+"44m                     "+ESC+"30m"+A219+A219+A219+A219+A219+A219+A219+ESC+"43m"+A223+A223+ESC+"0;43m"+A223+A223+A223+A223+ESC+"1m"+A223+A223+A223+A223+A223+A223+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"40C"+ESC+"43m"+ESC+"0;34;43m"+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+ESC+"30m"+A223+A223+ESC+"40m\n"
		thismsg += ESC+"44m                      "+ESC+"1m"+A219+A219+A219+A219+A219+A219+ESC+"0;33;43m"+A219+ESC+"C"+ESC+"1;36;40mYou reach th\n"
		thismsg += ESC+"A"+ESC+"42Ce castle and fight your way up the"+ESC+"C"+ESC+"0;33;43m"+A219+ESC+"40m\n"
		thismsg += ESC+"44m         "+ESC+"32;40m"+A178+A219+ESC+"44m            "+ESC+"1;30m"+A219+A219+A219+A219+A219+ESC+"0;33;43m"+A219+ESC+"C"+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"30C"+ESC+"43m"+ESC+"1;36;40mtower!"+ESC+"41C"+ESC+"0;33;43m"+A219+ESC+"40m\n"
		thismsg += ESC+"44m "+ESC+"32;40m"+A176+A219+ESC+"44m     "+ESC+"40m"+A176+A177+A219+A219+ESC+"44m "+ESC+"40m"+A219+ESC+"44m         "+ESC+"1;30m"+A219+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"24C"+ESC+"44m"+ESC+"40m"+A221+ESC+"44m"+A219+A219+A219+ESC+"0;33;43m"+A219+ESC+"48C"+A219+ESC+"40m\n"
		thismsg += ESC+"32m"+A178+A177+A177+A219+ESC+"44m  "+ESC+"40m"+A176+A177+A177+A177+A177+ESC+"44m "+ESC+"40m"+A176+A177+A219+ESC+"44m        "+ESC+"1;30m"+A219+A219+A219+A219+A219+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"28C"+ESC+"44m"+ESC+"0;33;43m"+A219+ESC+"C"+ESC+"1;36;40mYou blindly slash at any and all who\n"
		thismsg += ESC+"A"+ESC+"66C stand in  "+ESC+"0;33;43m"+A219+ESC+"40m\n"
		thismsg += ESC+"32m"+A177+A176+A177+A176+A178+A219+ESC+"44m "+ESC+"40m"+A176+A177+A176+A177+A177+A219+A178+ESC+"44m         "+ESC+"1;30m"+A219+A219+A219+A219+A219+ESC+"0;33;43m"+A219+ESC+"C"+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"30C"+ESC+"43m"+ESC+"1;36;40myour path - screaming to find the prisoner "+ESC+"4C\n"
		thismsg += ESC+"A"+ESC+"77C"+ESC+"0;33;43m"+A219+ESC+"40m\n"
		thismsg += ESC+"32m"+A176+A177+A177+A178+A178+ESC+"44m "+ESC+"40m"+A176+A177+A177+A178+A178+ESC+"44m "+ESC+"40m"+A176+A178+A178+ESC+"44m        "+ESC+"1;30m"+A219+A219+A219+A219+A219+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"28C"+ESC+"44m"+ESC+"0;33;43m"+A219+ESC+"C"+ESC+"1;36;40myou seek - and the jailer of your he\n"
		thismsg += ESC+"A"+ESC+"66Cart."+ESC+"7C"+ESC+"0;33;43m"+A219+ESC+"40m\n"
		thismsg += ESC+"44m "+ESC+"32;40m"+A176+A176+A177+ESC+"33m"+A176+ESC+"32m"+A177+A176+A177+ESC+"33m"+A178+ESC+"44m  "+ESC+"32;40m"+A178+A176+A177+A176+A178+ESC+"44m       "+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"23C"+ESC+"44m"+ESC+"1;30m"+A219+A219+A219+A219+A219+ESC+"0;33;43m"+A219+ESC+"48C"+A219+ESC+"40m\n"
		thismsg += ESC+"32m"+A176+A177+A177+A177+A176+A178+A177+ESC+"33m"+A176+A177+A178+ESC+"32m"+A177+A177+A178+A176+A178+A176+A178+ESC+"44m      "+ESC+"1;30m"+A219+A219+A219+A219+A219+ESC+"43m"+A220+A220+ESC+"0;43m"+A220+A220+A220+A220+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"34C"+ESC+"43m"+A220+ESC+"1m"+A220+A220+A220+ESC+"0;34;43m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"76C"+ESC+"43m"+ESC+"30m"+A220+A220+ESC+"40m\n"
		thismsg += ESC+"44m  "+ESC+"32;40m"+A177+A176+A177+A176+A176+ESC+"33m"+A176+A177+A178+A177+A177+ESC+"32m"+A177+A178+A177+A177+ESC+"44m       "+ESC+"1;30m"+A219+A219+ESC+"40m"+A222+ESC+"44m"+A219+A219+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"28C"+ESC+"44m"+A219+A219+ESC+"0;44m"+A219+A219+ESC+"40m"+A221+A219+ESC+"1;44m"+A219+ESC+"40m"+A221+ESC+"44m"+A219+A219+"   "+ESC+"0;33;43m"+A219+ESC+"40m"+A223+A223+"\n"
		thismsg += ESC+"A"+ESC+"44C"+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+A223+ESC+"43m"+A219+ESC+"34m"+A219+ESC+"40m\n"
		thismsg += ESC+"44m        "+ESC+"33;40m"+A176+A177+A178+ESC+"44m            "+ESC+"1;30m"+A219+A219+A219+A219+A219+ESC+"0;44m"+A219+A219+A219+ESC+"1m"+A219+A219+A219+A219+A219+A219+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"37C"+ESC+"44m"+A219+"   "+ESC+"0;33;43m"+A219+ESC+"2C"+ESC+"1;37;40mYou make it to the top and    \n"
		thismsg += ESC+"A"+ESC+"74C"+ESC+"0;33;43m"+A219+ESC+"44m "+ESC+"40m\n"
		thismsg += ESC+"44m        "+ESC+"40m"+A176+A177+A176+A178+ESC+"44m           "+ESC+"1;30m"+A219+A219+A219+A219+A219+A219+A219+ESC+"0;44m"+A219+A219+ESC+"1m"+A219+A219+A219+A219+A219+A219+"  "+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"40C"+ESC+"44m "+ESC+"0;33;43m"+A219+ESC+"4C"+ESC+"1;37;40mthrow open the door..."+ESC+"6C\n"
		thismsg += ESC+"A"+ESC+"74C"+ESC+"0;33;43m"+A219+ESC+"44m "+ESC+"40m\n"
		thismsg += ESC+"44m        "+ESC+"40m"+A176+A178+A177+A178+ESC+"44m         "+ESC+"32;40m"+A177+ESC+"1;42m"+A178+A219+ESC+"30;44m"+A219+A219+A219+A219+A219+A219+A219+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"31C"+ESC+"44m"+ESC+"0;44m"+A219+A219+ESC+"1m"+A219+A219+A219+A219+A219+"   "+ESC+"0;33;43m"+A219+ESC+"1;32;42m"+A177+A178+A178+ESC+"0;33m"+A220+A220+A220+A220+A220+A220+A220+A220+"\n"
		thismsg += ESC+"A"+ESC+"53C"+ESC+"32m"+A178+ESC+"1;42m"+A219+A219+ESC+"0;33m"+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+A220+ESC+"43m"+A219+ESC+"44m "+ESC+"40m\n"
		thismsg += ESC+"44m    "+ESC+"32;40m"+A176+ESC+"1;42m"+A176+ESC+"0;32m"+A177+ESC+"1;42m"+A219+A219+ESC+"0;33m"+A176+A177+A178+ESC+"44m        "+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"20C"+ESC+"44m"+ESC+"1;32;42m"+A178+A219+ESC+"0;32m"+A176+A178+ESC+"1;42m"+A219+ESC+"0;32m"+A178+ESC+"1;30;44m"+A219+A219+A219+ESC+"0;44m"+A219+A219+A219+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"32C"+ESC+"44m"+ESC+"1m"+A219+A219+A219+A219+A219+A219+"  "+ESC+"0;32m"+A177+ESC+"1;42m"+A176+ESC+"0;32m"+A178+ESC+"1;42m"+A178+ESC+"0;32m"+A177+ESC+"1;42m"+A178+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"46C"+ESC+"42m"+ESC+"44m    "+ESC+"0;32m"+A177+A178+A176+ESC+"1;42m"+A178+ESC+"0;32m"+A176+A178+ESC+"1;42m"+A219+A178+A178+ESC+"44m  "+ESC+"42m"+A176+A177+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"63C"+ESC+"42m"+A178+ESC+"44m            "+ESC+"40m\n"
		thismsg += ESC+"42m   "+ESC+"0;32m"+A177+A176+ESC+"1;42m"+A178+A176+ESC+"0;32m"+A176+ESC+"1;42m"+A178+A219+ESC+"0;32m"+A178+A219+ESC+"42m    "+ESC+"40m"+A177+A177+A176+A176+A177+"\n"
		thismsg += ESC+"A"+ESC+"21C"+ESC+"1;42m"+A178+A176+ESC+"30;40m"+A219+ESC+"0;32m"+A177+A177+A178+ESC+"1;42m"+A219+ESC+"30;40m"+A219+A219+ESC+"0m"+A219+A219+A219+ESC+"1m"+A219+A219+A219+"\n"
		thismsg += ESC+"A"+ESC+"36C"+ESC+"0;32m"+A177+A178+A176+ESC+"1;42m"+A176+ESC+"0;32m"+A176+ESC+"1;42m"+A219+A178+ESC+"0;32m"+A176+ESC+"1;42m"+A219+A219+" "+A178+" "+ESC+"0;32m"+A177+A176+A176+"\n"
		thismsg += ESC+"A"+ESC+"52C"+ESC+"1;42m"+A176+ESC+"0;32m"+A177+A176+ESC+"1;42m"+A176+ESC+"0;32m"+A177+ESC+"1;42m"+A176+A178+A176+ESC+"0;32m"+A178+ESC+"1;42m"+A176+ESC+"44m "+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"63C"+ESC+"44m             "+ESC+"40m\n"
		thismsg += ESC+"42m"+A176+A176+ESC+"0;32m"+A177+A176+ESC+"1;42m"+A176+A176+A178+A219+A219+A178+A178+A176+A176+"  "+A176+A176+ESC+"0;32m"+A177+A176+A177+A178+A176+A177+ESC+"1;42m"+A176+ESC+"0;32m"+A176+ESC+"1;42m"+A219+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"26C"+ESC+"42m"+ESC+"0;32m"+A178+ESC+"1;42m"+A219+ESC+"0;32m"+A177+A178+ESC+"1;42m"+A176+ESC+"0;32m"+A177+ESC+"1;42m"+A176+A176+ESC+"0;32m"+A177+A177+"\n"
		thismsg += ESC+"A"+ESC+"36C"+ESC+"1;42m"+A176+ESC+"0;32m"+A177+ESC+"1;42m"+A176+ESC+"0;32m"+A176+A177+A177+A177+ESC+"1;42m"+A219+A176+ESC+"0;32m"+A178+A178+A177+A176+A178+ESC+"1;42m"+A176+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"51C"+ESC+"42m"+ESC+"0;32m"+A177+A176+A177+A178+A178+ESC+"1;42m"+A178+ESC+"0;32m"+A177+A178+ESC+"1;42m"+A177+A178+ESC+"0;32m"+A177+ESC+"1;42m"+A176+ESC+"44m "+ESC+"40m\n"
		thismsg += ESC+"A"+ESC+"64C"+ESC+"44m   "+ESC+"37m<MORE>   "+ESC+"40m\n"
		return thismsg
