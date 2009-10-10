<?php
/**
 * Function loader file.
 * 
 * Contains all linked library files.
 * 
 * @package phpsord
 * @subpackage phpsord-system
 * @author J.T.Sage
 */

/** Database configuration */
require_once("dbaseconfig.php");
/** Static variables, non monster data */
require_once("staticvar.php");
/** Static variables, monster data */
require_once("monsters.php");
/** User control functions */
require_once("user.php");
/** Special skill control functions */
require_once("skills.php");
/** ANSI Art headers */
require_once("art.php");
/** Low level I/O functions */
require_once("basefunction.php");
/** User account control functions */
require_once("control.php");
/** In game modules */
require_once("modules.php");
/** Game menus */
require_once("menus.php");
/** Forest, Master, and Player fight modules */
require_once("forest.php");
/** The Red Dragon Inn modules */
require_once("inn.php");
?>
