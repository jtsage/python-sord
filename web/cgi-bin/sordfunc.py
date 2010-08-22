#!/usr/bin/python
""" Saga of the Red Dragon

 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.

 * Contains all web cgi-bin functions.

 * (c) 2009 - 2011 J.T.Sage
 * No Rights Reserved - but don't sell it please."""
__author__ = "Jonathan T. Sage <jtsage@gmail.com>"
__date__ = "18 August 2010"
__version__ = "2.0-pysqlite"
__credits__ = "Seth Able Robinson, original game concept"

def line():
		""" Dark Green Horizontal Rule """
		return "<span style=\"color: darkgreen\">-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-</span>"


def padnumcol(text, col):
	"""Pad a selection of text to be a specied number of columns wide.
	
	@param string $text Text to pad
	@param int $col Number of columns to fill """
	col = col - len(text)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
	return retval

def padright(text, col):
	""" Pad a selection of text to be a specied number of columns wide, right justified.
	 
	@param string $text Text to pad
	@param int $col Number of columns to fill """
	col = col - len(text)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
	return retval + text
