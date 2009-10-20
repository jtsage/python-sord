#!/usr/bin/python
"""
 * General Base Functions.
 * 
 * Contains all low level input/output functions.
 * 
 * @package phpsord
 * @subpackage phpsord-general
 * @author J.T.Sage
"""
import re, time

def func_slowecho(connection, data):
	"""slowecho"""
	for thisData in list(data):
		time.sleep(0.001)
		connection.send(thisData)
		

def func_pauser(connection):
	"""Sreen pauser"""
	#data = connection.recv(1024) #clear buffer
	func_slowecho(connection, func_casebold("\r\n    :-: Press Any Key :-:", 2))
	pauser_quit = False
	while ( not pauser_quit ):
		data = connection.recv(5)
		if not data: break
		pauser_quit = True
		connection.send("\r\n")
		

def func_getLine(connection, echo):
	""" Get line from user"""
	getterquit = False
	retval = ""
	while ( not getterquit ):
		data = connection.recv(2)
		if not data: break
		if ( data[0] == "\n" or data[0] == "\r" ):
			getterquit = True
		else:
			if ( data[0] == chr(127) ):
				retval = retval[:-1]
				connection.send("\x1b[1D \x1b[1D")
			else:
				retval += data
				if ( echo ):
					connection.send(data)
				else:
					connection.send('*')
	return retval

def func_caseclr(text, boldcolor, normcolor):
	""" Color by character case.
	* Capitals returns in boldcolor, lowercase in normcolor
	* 
	* @param string $text Input text to color
	* @param int $boldcolor Color for capital letters
	* @param int $normcolor Color for lowercase letters
	* @return string Colored text. """
	bclrstr = "\x1b[1m\x1b[3" + str(boldcolor) + "m"
	nclrstr = "\x1b[0m\x1b[3" + str(normcolor) + "m"
	return re.sub("([A-Z:<>])", bclrstr + r"\1" + nclrstr, text) + "\x1b[0m"

def func_casebold(text, boldcolor):
	""" Color by character case.
	* Capitals returns in bold of suplied color, lowercase in suplied color.
	* 
	* @param string $text Input text to color
	* @param int $boldcolor Color for lowercase letters
	* @return string Colored text."""
	bclrstr = "\x1b[1m\x1b[3" + str(boldcolor) + "m"
	nclrstr = "\x1b[0m\x1b[3" + str(boldcolor) + "m"
	return re.sub("([A-Z:<>])", bclrstr + r"\1" + nclrstr, text) + "\x1b[0m"

def func_colorcode(text):
	""" Process user entered color codes.
	* Uses color codes contained in curly braces.  Standard ANSI codes work.
	* 
	* @todo Add error correction and checking.  Could be used to hose other players.
	* @param string $text Text to convert to escape string
	* @return string Fully escaped string """
	return re.sub("\{(\d+)\}", "\x1b[" + r"\1" + "m" , text) + "\x1b[0m"


def func_normmenu(text):
	"""Return a standard colored menu entry.
	* 
	* @param string $text Text to convert to menu entry
	* @return string Fully escaped string"""
	bclrstr = "  \x1b[0m\x1b[32m(\x1b[1;35m"
	nclrstr = "\x1b[0m\x1b[32m)"
	return re.sub("\(([A-Z:<>])\)", bclrstr + r"\1" + nclrstr, text) + "\x1b[0m\r\n"


def func_menu_2col(text1, text2, col1, col2):
	""" 2 Column Menu
	* Generate a 2 column menu entry
	* 
	* @param string $text1 Menu Option 1
	* @param string $text2 Menu Option 2
	* @param int $col1 Option color for menu option 1
	* @param int $col2 Option color for menu option 2
	* @return string Formatted menu string"""
	nclrstr = "\x1b[0m\x1b[32m)"
	bclrstr1 = "\x1b[0m\x1b[32m(\x1b[1;3"+str(col1)+"m"
	bclrstr2 = "\x1b[0m\x1b[32m(\x1b[1;3"+str(col2)+"m"
	text1col = re.sub("\(([A-Z:<>])\)", bclrstr1 + r"\1" + nclrstr, text1) + "\x1b[0m"
	text2col = re.sub("\(([A-Z:<>])\)", bclrstr2 + r"\1" + nclrstr, text2) + "\x1b[0m"
	return "  " + text1col + padnumcol(text1, 36) + text2col + "\x1b[0m\r\n"

def func_maketime(user):
	""" Make a time since login string"""
	currenttime = time.time()
	ontime = int(currenttime) - int(user.logontime)
	sec = ontime % 60
	min = ( ontime - sec ) / 60
	if ( sec < 10 ):
		ptime = str(min) + ':0' + str(sec)
	else: 
		ptime = str(min) + ':' + str(sec)
	return ptime

def padnumcol(text, col):
	"""Pad a selection of text to be a specied number of columns wide.
	* 
	* @param string $text Text to pad
	* @param int $col Number of columns to fill
	* @return string String of spaces to finish column"""
	col = col - len(text)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
	return retval

def padright(text, col):
	""" Pad a selection of text to be a specied number of columns wide, right justified.
	* 
	* @param string $text Text to pad
	* @param int $col Number of columns to fill
	* @return string Fully padded text"""
	col = col - len(text)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
	return retval + text
