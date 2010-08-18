#!/usr/bin/python
"""
 * SORD Database class
 * 
 * Contains specialized sord database routines
 * 
"""
import sqlite3, time, random
from os.path import isfile
from os import unlink
from shutil import copy

def getDB(config):
	sqc = sqlite3.connect(config.sqlitefile)
	return sqc

def dayRollover(config, sqc, log):
	""" Daily Update routine """
	
	randdaily = [ 
			'More children are missing today.',
			'A small girl was missing today.',
			'The town is in grief.  Several children didnt come home today.',
			'Dragon sighting reported today by a drunken old man.',
			'Despair covers the land - more bloody remains have been found today.',
			'A group of children did not return from a nature walk today.',
			'The land is in chaos today.  Will the abductions ever stop?',
			'Dragon scales have been found in the forest today..Old or new?',
			'Several farmers report missing cattle today.',
			'A Child was found today!  But scared deaf and dumb.']
			
	checklast = 0
	timestr = '%Y%j00'
	if ( config.daylength > 24 ) :
		days = config.daylength // 24
		checklast = time.strftime('%Y%j00', time.localtime(time.mktime(time.localtime()) - (days*24*60*60)))
	elif ( config.daylength == 6 ) :
		if ( int(time.strftime('%H', time.localtime())) < 6 ): end = '00' 
		elif ( int(time.strftime('%H', time.localtime())) < 12 ): end = '06' 
		elif ( int(time.strftime('%H', time.localtime())) < 18 ): end = '12' 
		else: end = '18' 
		timestr = '%Y%j' + end
		checklast = time.strftime('%Y%j'+end, time.localtime())
	elif ( config.daylength == 8 ) :
		if ( int(time.strftime('%H', time.localtime())) < 8 ): end = '00' 
		elif ( int(time.strftime('%H', time.localtime())) < 16 ): end = '08' 
		else: end = '16' 
		timestr = '%Y%j' + end
		checklast = time.strftime('%Y%j'+end, time.localtime())
	elif ( config.daylength == 12 ) :
		if ( int(time.strftime('%H', time.localtime())) < 12 ): end = '00' 
		else: end = '12' 
		timestr = '%Y%j' + end
		checklast = time.strftime('%Y%j'+end, time.localtime())
	else:
		checklast = time.strftime('%Y%j00', time.localtime())
	
	sqr = sqc.cursor()
	
	for row in sqr.execute("select value from sord where name=?", ('lastday',)):
		lday, = row
		if ( int(lday) < int(checklast) ):
			log.add(" === DAY ROLLOVER")
			rsaying = randdaily[random.randint(0, 9)]
			laster = time.strftime('%Y%j', time.localtime(time.mktime(time.localtime()) - (config.delinactive*24*60*60)))
			sqc.execute("UPDATE users set ffight = ?, pfight = ? WHERE 1", (config.ffight, config.pfight))
			sqc.execute("UPDATE users set flirt = 0, sung = 0, master = 0, alive = 1, usem = spclm, hp = hpmax WHERE 1")			
			sqc.execute("UPDATE users set used = (spcld / 5 ) + 1 WHERE spcld > 0")
			sqc.execute("UPDATE users set uset = (spclt / 5 ) + 1 WHERE spclt > 0")
			sqc.execute("UPDATE users set bank = bank + ( bank * ("+str(config.bankinterest)+"/100) ) WHERE bank > 0")
			sqc.execute("INSERT INTO daily ( 'data' ) VALUES ( ? )", ( "{31}"+rsaying, ))
			sqc.execute("DELETE from users WHERE last < ?", (laster,))
			sqc.execute("UPDATE sord set value = value + 1 WHERE 'name' = 'gdays'")
			sqc.execute("UPDATE sord set value = ? WHERE name = 'lastday'", (time.strftime(timestr, time.localtime()),))
			sqc.commit()
	
def initialTest(config, log):
	""" Check for db existence and check version """
	if ( isfile(config.sqlitefile) ):
		sqc = sqlite3.connect(config.sqlitefile)
		sqr = sqc.cursor()
		
		sqc.execute("vacuum")
		sqc.commit()
		
		for row in sqr.execute("select value from sord where name=?", ('version',)):
			version, = row
			if ( version > 1 ):
				log.add(" === SQLite Database is up to date")
			else:
				log.add(" === SQLite Database is out of date (corrupt), rebuilding...")
				updateDB(config, log)
		sqc.close()
	else:
		createDB(config, log)
		
def updateDB(config, log):
	""" Update sord datebase - for now, nuke and start over """
	copy(config.sqlitefile, config.sqlitefile+".bak")
	unlink(config.sqlitefile)
	createDB(config, log)
		
def createDB(config, log):
	""" Create new sord database """
	log.add(" === Creating New Database - First Run!")
	sqc = sqlite3.connect(config.sqlitefile)
	
	statstable = [ # (name, default value)
		('cls' , 1) , ('sex', 1), ('flirt', 0), ('sung', 0), ('master', 0),
		('atinn', 0), ('horse', 0), ('fairy', 0), ('ffight', config.ffight), ('pfight', config.pfight),
		('gems', 0), ('gold', 500), ('bank', 0), ('level', 1), ('charm', 0),
		('spclm', 0), ('spclt', 0), ('spcld', 0), ('used', 0), ('dragon', 0),
		('uset', 0), ('usem', 0), ('str', 10), ('defence', 1), ('exp', 1),
		('hp', 20), ('hpmax', 20), ('weapon', 1), ('armor', 1), ('pkill', 0),
		('dkill', 0), ('fuck', 0), ('alive', 1) ]
	statssql = "create table users ( userid INTEGER PRIMARY KEY, username TEXT, password TEXT, fullname TEXT, last TEXT"
	for stat in statstable:
		name, defu = stat
		statssql = statssql + ", " + name + " INTEGER DEFAULT " + str(defu)
	statssql = statssql + " )"
	with sqc:
		sqc.execute("create table sord ( name TEXT, value integer)")
		sqc.execute("insert into sord values (?,?)", ('version', '2'))
		sqc.execute("insert into sord values (?,?)", ('gdays', '0'))
		sqc.execute("insert into sord values (?,?)", ('lastday', '201000101'))
		
		sqc.execute("create table daily ( id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT )")
		sqc.execute("insert into daily (data) values (?)", ('{31}Welcome to {1}{37}S{0}{32}.{1}{37}O{0}{32}.{1}{37}R{0}{32}.{1}{37}D{0}{32}.', ))
		sqc.execute("insert into daily (data) values (?)", ('{31}Despair covers the land - more bloody remains have been found today.',))
		
		sqc.execute("create table dhtpatrons (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, nombre TEXT)")
		sqc.execute("insert into dhtpatrons (data, nombre) values (?, ?)", ('{34}Welcome to the {31}Dark Horse Tavern', 'Chance'))
		
		sqc.execute("create table dirt (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, nombre TEXT)")
		sqc.execute("insert into dirt (data, nombre) values (?, ?)", ('{32}Mighty quiet around here...', 'Jack the Ripper'))
		
		sqc.execute("create table flowers ( id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT, nombre TEXT )")
		sqc.execute("insert into flowers (data, nombre) values (?, ?)", ('{34}Does this kimono make me look {31}fat?', 'Fairy #1'))
		sqc.execute("insert into flowers (data, nombre) values (?, ?)", ('{36}No, just {1}ugly', 'Fairy #2'))
		
		sqc.execute("create table mail ( id INTEGER PRIMARY KEY AUTOINCREMENT, 'from' INTEGER, 'to' integer, message text, sent text)")
		sqc.execute("create table online ( userid integer, whence text )")
		
		sqc.execute("create table patrons ( id INTEGER PRIMARY KEY, data text, nombre TEXT)" )
		sqc.execute("insert into patrons (data, nombre) values (?, ?)", ('{34}Welcome to the {31}Red Dragon {34}Inn', 'The Bartender'))
		
		sqc.execute(statssql)
		sqc.execute("insert into users ( userid, username, password, fullname, used, spcld ) values (?, ?, ?, ?, ?, ?)", (1, config.gameadmin, config.gameadminpass, config.admin,1,1))

