#!/usr/bin/python
"""
 * Configuration file.
 * 
 * Contains all configuration data for the game
 * 
 * @package phpsord
 * @subpackage phpsord-system
 * @author J.T.Sage
 * @staticvar string $MYSQL_SERVER Hostname of mysql server.
 * @staticvar string $MYSQL_USER User for mysql server.
 * @staticvar string $MYSQL_PASS Password for mysql server.
 * @staticvar string $MYSQL_DATABASE Database to use on mysql server.
 * @staticvar string $MYSQL_PREFIX Prefix for all mysql table names.
 * @staticvar string $SORD_HOST Name of the game host.  FQDN.
 * @staticvar string $SORD_ADMIN Name of the game admin.
 * @staticvar int $SORD_DELINACT Number of game days to delete inactive users after.
 * @staticvar int $SORD_DAYLENGTH Length of the game days, in hours.
 * @staticvar int $SORD_BANKINT Interest to be paid on bank acounts per game day.
 * @staticvar int $SORD_FFIGHT Number of forest fights to start each game day, per player.
 * @staticvar int $SORD_PFIGHT Number of player fights to start each game day, per player.
"""

class sord():

	def sqlServer(self):
		return "localhost"
		
	def sqlDatabase(self):
		return "sord"
		
	def sqlUser(self):
		return "sord"
		
	def sqlPass(self):
		return "dr0s"
		
	def sqlPrefix(self):
		return "gameone_"
		
	def host(self):
		return "sord.jtsage.com"
		
	def admin(self):
		return "JTSage"
		
	def dayLength(self):
		return 24
		
	def bankInterest(self):
		return 2
		
	def deleteInactive(self):
		return 256
		
	def forestFights(self):
		return 30
		
	def playerFights(self):
		return 5
		
	def version(self):
		return "py1.0.1"
