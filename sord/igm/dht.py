"""
 IGM:  The Dark Horse Tavern
 
 This is pretty close to the original dark horse tavern, found
 in the L.O.R.D forest - it has however been converted to a IGM
 cabable format for documentation purposes.  
 
 A few notes:
 
   __init__() is called during server startup - in other words, 
              far to early to be of much use.
   run() is called from the main sord code when the user invokes
         the IGM.  A sord user object is passed as the sole 
         argument.  See ../base/user.py for details on the 
         standard API.
         
   The two imports listed allow for standard display functions,
   plus use of things like daily happenings and user stats view
   
 Best practice note:
 
   It's a good idea to throw a tracking log entry in the top of
   your run() method.  Ex:
   
      user.log.add("   ** "+user.thisFullname+" entered IGM: IGM Name") 
      
   Also, see the example to have the module print it's own
   installation options below:
      
"""
if ( __name__ == '__main__' ) :
	print "The Dark Horse Tavern IGM"
	print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
	print "  To install, add this tuple to igmlist in"
	print "  <sorddir>/sord/igm/__init__.py :"
	print "      ('D', dht.dht(), 'The Dark Horse Tavern')"
else:
	from ..base import func
	from ..game import util
	from ..base import user

class dht():
	def __init__(self):
		pass
	
	def main_menu(self):
		"""Dark Cloak Menu"""
		user = self.user
		thismsg  = "\r\n\r\n\x1b[32m                          Dark Cloak Tavern\r\n"
		thismsg += user.art.line()
		thismsg += "  \x1b[32mA blazing fire warms your heart as well as your body in this fragrant.\x1b[0m\r\n"
		thismsg += "  \x1b[32mroadhouse.  Many a wary traveler has had the good fortune to find this\x1b[0m\r\n"
		thismsg += "  \x1b[32mcozy hostel, to escape the harsh reality of the dense forest for a few\x1b[0m\r\n"
		thismsg += "  \x1b[32mmoments.  You notice someone has etched something in the table you are\x1b[0m\r\n"
		thismsg += "  \x1b[32msitting at.\x1b[0m\r\n\r\n"
		thismsg += func.menu_2col("(C)onverse With The Patrons", "(D)aily News", 5, 5)
		thismsg += func.menu_2col("(E)xamine Etchings In Table", "(Y)our Stats", 5, 5)
		thismsg += func.menu_2col("(T)alk with Bartender", "(R)eturn to Forest", 5, 5)
		return thismsg
	
	def prompt(self):
		""" User Prompt"""
		user = self.user
		ptime = func.maketime(user)
		thismenu  = "\r\n  \x1b[1;35mThe Dark Cloak Tavern\x1b[0m\x1b[1;30m (? for menu)\x1b[0m\r\n"
		thismenu += "  \x1b[1;30m(C,D,E,Y,T,R)\x1b[0m\r\n\r\n"
		thismenu += "  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
		return thismenu

	def run(self, user):
		""" Dark Horse Tavern Logic"""
		self.user = user
		user.log.add("   ** "+user.thisFullname+" entered IGM: Dark Horse Tavern") 
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				if (  not user.expert ):
					user.write(self.main_menu())
				user.write(self.prompt())
			skipDisp = False
			data = user.ntcon.recv(2)
			if not data: break
			elif ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
				user.write('R')
				thisQuit = True
			elif ( data[0] == '?' ):
				user.write('?')
				user.write(self.main_menu(user))
				skipDisp = True
			elif ( data[0] == 'y' or data[0] == 'Y' ):
				user.write('Y')
				user.write(util.viewstats(user))
				user.pause()
			elif ( data[0] == 'd' or data[0] == 'D' ):
				user.write('D')
				user.write(util.dailyhappen(True, user))
				user.pause()
			elif ( data[0] == 'c' or data[0] == 'C' ):
				user.write('C')
				self.converse()
			elif ( data[0] == 'e' or data[0] == 'E' ):
				user.write('E')
				db = user.dbcon.cursor()
				db.execute("SELECT fullname, fuck FROM users u, stats s WHERE s.userid = u.userid AND s.fuck > 0 ORDER by s.fuck DESC")
				user.write("\r\n\r\n  \x1b[32mUsers who have gotten lucky:\x1b[0m\r\n")
				
				for row in db.fetchall():
					if not row:
						user.write("\r\n\r\n  \x1b[32mWhat a sad thing - there are no carvings here after all.\x1b[0m\r\n")
					else:
						for (nombre, data) in row:
							user.write("  \x1b[32m"+nombre+padnumcol(nombre, 25)+"\x1b[1m"+str(data)+"\x1b[0m\r\n")
				user.write("\r\n")
				db.close()
				user.pause()
			elif ( data[0] == 't' or data[0] == 'T' ):
				user.write('T')
				self.chance(user)
			else:
				skipDisp = True

	def converse(self):
		""" Converse with patrons (dht)"""
		user = self.user
		output  = "\r\n\r\n  \x1b[1;37mConverse with the Patrons\x1b[22;32m....\x1b[0m\r\n"
		output += "\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
		db = user.dbcon.cursor()
		db.execute("SELECT data, nombre FROM (SELECT * FROM dhtpatrons ORDER BY id ASC LIMIT 10) AS tbl ORDER by tbl.id")
		for (data, nombre) in db.fetchall():
			output += "    \x1b[32m"+nombre+" \x1b[1;37msays... \x1b[0m\x1b[32m" + func.colorcode(data)
			output += "\x1b[0m\r\n\x1b[32m                                      -=-=-=-=-=-\x1b[0m\r\n"
		output += "\r\n  \x1b[32mAdd to the conversation? \x1b[1m: \x1b[0m"
		user.write(output)
		db.close()
		yesno = user.ntcon.recv(2)
		if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
			user.write(func.casebold("\r\n  What say you? :-: ", 2))
			ann = func.getLine(user.ntcon, True)
			user.dbcon.execute("INSERT INTO dhtpatrons ( `data`, `nombre` ) VALUES ( ?, ? )", (ann, user.thisFullname))
			user.dbcon.commit()
			user.write(func.casebold("\r\n  Wisdom added!\r\n", 2))
			user.pause()
			
	def chance_menu(self):
		""" Chance's Menu """
		user = self.user
		ptime = func_maketime(user)
		thismenu = func.normmenu("(C)hange Profession")
		thismenu += func.normmenu("(L)earn About Your Enemies")
		thismenu += func.normmenu("(T)alk About Colors")
		thismenu += func.normmenu("(R)eturn to Tavern")
		thismenu += "\r\n  \x1b[32mYour command, \x1b[1m" + user.thisFullname + "\x1b[22m? \x1b[1;37m[\x1b[22m"+ptime+"\x1b[1m] \x1b[0m\x1b[32m:-: \x1b[0m"
		return thismenu
	
	def chance(self):
		""" Chance, the bartender """
		user = self.user
		header = "\r\n\r\n  \x1b[32m              Talking To Chance\x1b[0m\r\n"
		header += "\x1b[32m-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\x1b[0m\r\n"
		header += "  \x1b[32mYou seat yourself next to the bartender,\x1b[0m\r\n"
		header += "  \x1b[32mfor some reason you like him.          \x1b[0m\r\n\r\n"
		thisQuit = False
		skipDisp = False
		while ( not thisQuit ):
			if ( not skipDisp ):
				user.write(header)
				user.write(self.chance_menu())
			skipDisp = False
			data = user.ntcon.recv(2)
			if not data: break
			elif ( data[0] == 'q' or data[0] == 'Q' or data[0] == 'r' or data[0] == 'R' ):
				user.write('R')
				thisQuit = True
			elif ( data[0] == 't' or data[0] == 'T' ):
				user.write('T')
				user.write("\r\n\r\n  \x1b[32mColors are easy my friend!  Just enclose single ANSI codes in braces\r\n  like this {32} - that would turn the text green you can learn\r\n  more at:\r\n    http://en.wikipedia.org/wiki/ANSI_escape_code\x1b[0m\r\n")
				user.pause()
			elif ( data[0] == 'l' or data[0] == 'L' ):
				user.write('L')
				whoid = util.finduser(user, "\r\n  \x1b[32mGet information on who?")
				if ( whoid > 0 ):
					whoName = user.userGetLogin(whoid)
					whoCost = user.level * 100
					user.write("\r\n  \x1b[32mThat will be \x1b[1m"+str(whoCost)+"\x1b[0;32m gold.  Ok? ")
					yesno = user.ntcon.recv(2)
					if ( yesno[0] == 'y' or yesno[0] == 'Y' ):
						user.write('Y')
						if ( user.gold < whoCost ):
							user.write("\r\n  \x1b[32mYou don't have enough gold jackass!\x1b[0m\r\n")
						else:
							usertoSee = user.sorduser(whoName, user.dbcon, user.ntcon, user.art)
							user.gold -= whoCost
							user.write(util.viewstats(usertoSee))
							del usertoSee
							user.pause()
					else:
						user.write('N')
						user.write("\r\n  \x1b[32mOk.  You got it.\x1b[0m\r\n")
				else: 
					user.write("\r\n  \x1b[32mOk.  Nevermind.\x1b[0m\r\n")
			elif ( data[0] == 'c' or data[0] == 'C' ):
				user.write('C')
				user.write(func.casebold("\r\n  Pick that which best describes your childhood.\r\n  From an early age, you remember:\r\n\r\n", 2))
				user.write(func.normmenu("(D)abbling in the mystical forces"))
				user.write(func.normmenu("(K)illing a lot of woodland creatures"))
				user.write(func.normmenu("(L)ying, cheating, and stealing from the blind"))
				thisLooper = False
				while ( not thisLooper ):
					user.write(func.casebold("\r\n  Your Choice (D/K/L) :-: ", 2))
					data = user.ntcon.recv(2)
					if not data: break
					if ( data[0] == 'k' or data[0] == 'K' ):
						user.write('K')
						user.cls = 1
						thisLooper = True
						user.write(func.casebold("\r\n  Welcome warrior to the ranks of the Death Knights!\r\n", 2))
					if ( data[0] == 'd' or data[0] == 'D' ):
						user.write('D')
						user.cls = 2
						thisLooper = True
						user.write(func.casebold("\r\n  Feel the force young jedi.!\r\n", 2))
					if ( data[0] == 'l' or data[0] == 'L' ):
						user.write('L')
						user.cls = 3
						thisLooper = True
						user.write(func.casebold("\r\n  You're a real shitheel, you know that?\r\n", 2))
			else:
				skipDisp = True
	
