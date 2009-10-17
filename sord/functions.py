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
import re

""" Color by character case.
 * Capitals returns in boldcolor, lowercase in normcolor
 * 
 * @param string $text Input text to color
 * @param int $boldcolor Color for capital letters
 * @param int $normcolor Color for lowercase letters
 * @return string Colored text. """
def func_caseclr(text, boldcolor, normcolor):
	bclrstr = "\x1b[1m\x1b[3" + str(boldcolor) + "m"
	nclrstr = "\x1b[0m\x1b[3" + str(normcolor) + "m"
	return re.sub("([A-Z:<>])", bclrstr + r"\1" + nclrstr, text) + "\x1b[0m"


""" Color by character case.
 * Capitals returns in bold of suplied color, lowercase in suplied color.
 * 
 * @param string $text Input text to color
 * @param int $boldcolor Color for lowercase letters
 * @return string Colored text."""
def func_casebold(text, boldcolor):
	bclrstr = "\x1b[1m\x1b[3" + str(boldcolor) + "m"
	nclrstr = "\x1b[0m\x1b[3" + str(boldcolor) + "m"
	return re.sub("([A-Z:<>])", bclrstr + r"\1" + nclrstr, text) + "\x1b[0m"

""" Process user entered color codes.
 * Uses color codes contained in curly braces.  Standard ANSI codes work.
 * 
 * @todo Add error correction and checking.  Could be used to hose other players.
 * @param string $text Text to convert to escape string
 * @return string Fully escaped string """
def func_colorcode(text):
	return re.sub("\{(\d+)\}", "\x1b[" + r"\1" + "m" , text) + "\x1b[0m"

"""Return a standard colored menu entry.
 * 
 * @param string $text Text to convert to menu entry
 * @return string Fully escaped string"""
def func_normmenu(text):
	bclrstr = "  \x1b[0m\x1b[32m(\x1b[1;35m"
	nclrstr = "\x1b[0m\x1b[32m)"
	return re.sub("\(([A-Z:<>])\)", bclrstr + r"\1" + nclrstr, text) + "\x1b[0m"
	
"""Pad a selection of text to be a specied number of columns wide.
 * 
 * @param string $text Text to pad
 * @param int $col Number of columns to fill
 * @return string String of spaces to finish column"""
def padnumcol(text, col):
	col = col - len(text)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
	return retval

""" Pad a selection of text to be a specied number of columns wide, right justified.
 * 
 * @param string $text Text to pad
 * @param int $col Number of columns to fill
 * @return string Fully padded text"""
def padright(text, col):
	col = col - len(text)
	ittr = 0
	retval = ""
	while ( ittr < col ):
		retval += " "
		ittr += 1
	return retval + text
