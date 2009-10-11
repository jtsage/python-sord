#!/usr/bin/php
<?
/**
 * Saga of the Red Dragon - Main Program Loop
 * 
 * A blatent rip off of Seth Able Robinson's BBS Door Masterpiece.  
 * All attempts were made to be as close to the original as possible, 
 * including some original artwork, the original fight equations, and 
 * most especially the original spelling and punctuation mistakes.  Enjoy.
 * 
 * 
 * @package phpsord
 * @author J.T.Sage
 * @copyright 2009-2011
 * @license http://sord.jtsage.com/LICENSE Disclaimer's License
 * @version 0.9.9
 * @todo IGM framework, main menu '1' for image.
 */
/* Set ANSI characters per user input. */
echo "PRESS ENTER TO CONNECT (UNICODE TERMINAL)\nPRESS 'A', THEN ENTER FOR IBM950 CODEPAGE\n"; 
$a176 = html_entity_decode('&#9617;',ENT_QUOTES,'UTF-8');
$a177 = html_entity_decode('&#9618;',ENT_QUOTES,'UTF-8');
$a178 = html_entity_decode('&#9619;',ENT_QUOTES,'UTF-8');
$a219 = html_entity_decode('&#9608;',ENT_QUOTES,'UTF-8');
$a220 = html_entity_decode('&#9604;',ENT_QUOTES,'UTF-8');
$a221 = html_entity_decode('&#9612;',ENT_QUOTES,'UTF-8');
$a222 = html_entity_decode('&#9616;',ENT_QUOTES,'UTF-8');
$a223 = html_entity_decode('&#9600;',ENT_QUOTES,'UTF-8');
$a254 = html_entity_decode('&#9642;',ENT_QUOTES,'UTF-8');

$dumper = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
if ( $dumper == "A" ) { 
	$a176 = "\260"; $a177 = "\261"; $a178 = "\262"; $a219 = "\333"; $a220 = "\334"; $a221 = "\335"; $a222 = "\336"; $a223 = "\337"; $a254 = "\376"; }

$SORDDEBUG = 0;
#$SORDDEBUG = 1;
$SORDVERSION = "0.9.9";
$SORDDELAY = ( $SORDDEBUG ) ? 0 : 700;
/** Server and Game configuration */
require_once("config.php");
/** Load all needed functions */
require_once("lib/functions-load.php");

echo chr(255) . chr(253) . chr(3);
# This enables bidirectional communication

declare(ticks=1);
$logontime = time();

if ( !$SORDDEBUG ) { slowecho(art_header()); pauser(); }

$next = ( $SORDDEBUG ) ? 1 : 0;
while ( !$next ) {
	slowecho(art_banner());
	$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	if ( $choice == "Q" ) { die(func_casebold("\nQuitting to the fields...\n\n", 1)); }
	if ( $choice == "L" ) { slowecho(module_list()); pauser(); } else { $next = 1; }
}

echo "\n\n"; $userid = ( $SORDDEBUG ) ? 1 :control_getlogin();
if ( user_isdead($userid) ) { die(func_casebold("\nSorry!  You're dead right now!\n\n", 1)); }
user_logintime($userid);

$logonsql = "INSERT INTO {$MYSQL_PREFIX}online ( `userid` ) VALUES ( {$userid} )";
$results = mysql_query($logonsql, $db);

if ( user_atinn($userid) ) { slowecho(func_casebold("\nYou awake from your warm bed, and wander out into the main road...", 2)); pauser(); user_leaveinn($userid); }

$ctrl = ( $SORDDEBUG ) ? 1 : 0;
while ( !$ctrl ) {
	slowecho(module_dailyhappen(0));
	$choice =  preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	if ( !($choice == "T") ) { $ctrl = 1; }
}

if ( !$SORDDEBUG ) { slowecho(module_who()); pauser(); }
if ( !$SORDDEBUG ) { slowecho(module_viewstats($userid)); pauser(); }

$mainexit = 0; $xprt = 0;
while ( !$mainexit ) {
	control_readmail($userid);
	if ( !$xprt ) { slowecho(menu_mainlong(0)); } else { slowecho(menu_mainshort()); }
	$key = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	switch ($key) {
		case 'Q': // QUIT
			$mainexit = 1; break;
		case 'X': // EXPERT VIEW
			$xprt = ( $xprt ) ? 0 : 1; break;
		case "V": // VIEW STATS
			slowecho(module_viewstats($userid)); pauser(); break;
		case "D": // DAILY HAPPENINGS
			slowecho(module_dailyhappen(1)); pauser(); break;
		case "?": // SHOW MENU
			slowecho(menu_mainlong(1)); break;
		case 'P': // PLAYERS ONLINE
			slowecho(module_who()); pauser(); break;
		case 'L': // LIST PLAYERS
			slowecho(module_list()); pauser(); break;
		case 'A': // ABDULS ARMOR
			module_abduls(); break;
		case 'K': // KING ARTHURS WEAPONS
			module_arthurs(); break;
		case 'Y': // THE BANK
			module_bank(); break;
		case 'H': // HEALERS HUT
			module_heal(); break;
		case 'F': // THE FOREST
			module_forest(); break;
		case 'M': // MAKE ANNOUNCMENT
			module_announce(); break;
		case 'W': // SEND MAIL MESSAGE
			control_sendmail($userid); break;
		case 'I': // RED DRAGON INN
			inn_logic(); break;
		case 'T': // WARRIOR TRAINING
			module_turgon(); break;
	}
}

slowecho(func_casebold("\n\n   Quitting to the Fields... GoodBye!\n", 7));
$logoutsql = "DELETE FROM {$MYSQL_PREFIX}online WHERE userid = {$userid}";
$results = mysql_query($logoutsql, $db);

?>
