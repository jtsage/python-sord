#!/usr/bin/php
<?
echo "PRESS ENTER TO CONNECT"; $dumper = fgets(STDIN);
$SORDDEBUG = 0;
#$SORDDEBUG = 1;
$SORDVERSION = "0.0.1";
$SORDDELAY = ( $SORDDEBUG ) ? 0 : 700;
require_once("config.php");
require_once("lib/functions-load.php");

echo chr(255) . chr(253) . chr(3);
# This enables bidirectional communication
# NO LOCAL ECHO.
#echo chr(255) . chr(251) . chr(1);

declare(ticks=1);
$logontime = time();
pcntl_signal(SIGTERM, "signal_handler");
pcntl_signal(SIGQUIT, "signal_handler");
pcntl_signal(SIGINT, "signal_handler");
pcntl_signal(SIGALRM, "signal_handler");

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

$ctrl = ( $SORDDEBUG ) ? 1 : 0;
while ( !$ctrl ) {
	slowecho(module_dailyhappen(0));
	$choice =  preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
	if ( !($choice == "T") ) { $ctrl = 1; }
}

if ( !$SORDDEBUG ) { slowecho(module_viewstats($userid)); pauser(); }

$mainexit = 0; $xprt = 0;
while ( !$mainexit ) {
  if ( !$xprt ) { slowecho(menu_mainlong(0)); } else { slowecho(menu_mainshort()); }
  $key = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
  switch ($key) {
    case 'Q':
      $mainexit = 1;
      break;
    case 'X':
      $xprt = ( $xprt ) ? 0 : 1;
      break;
    case "V":
      slowecho(module_viewstats($userid));
      pauser();
      break;
    case "D":
      slowecho(module_dailyhappen(1));
      pauser();
      break;
    case "?":
      slowecho(menu_mainlong(1));
      break;
    case 'P':
      slowecho(module_who());
      pauser();
      break;
    case 'L':
      slowecho(module_list());
      pauser();
      break;
    case 'A':
      module_abduls();
      break;
    case 'K':
      module_arthurs();
      break;
    case 'Y':
      module_bank();
      break;
    case 'H':
      module_heal();
      break;
    case 'F':
      module_forest();
      break;
  }

}
slowecho(func_casebold("\n\n .....Quitting to the Fields... GoodBye!\n", 3));
$logoutsql = "DELETE FROM {$MYSQL_PREFIX}online WHERE userid = {$userid}";
$results = mysql_query($logoutsql, $db);

?>
