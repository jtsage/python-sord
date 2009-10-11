<?php
/**
 * General Base Functions.
 * 
 * Contains all low level input/output functions.
 * 
 * @package phpsord
 * @subpackage phpsord-general
 * @author J.T.Sage
 */

/**
 * Color by character case.
 * 
 * Capitals returns in boldcolor, lowercase in normcolor
 * 
 * @param string $text Input text to color
 * @param int $boldcolor Color for capital letters
 * @param int $normcolor Color for lowercase letters
 * @return string Colored text.
 */
function func_caseclr($text, $boldcolor, $normcolor) {
	$bclrstr = "\033[1m\033[3" . $boldcolor . "m";
	$nclrstr = "\033[0m\033[3" . $normcolor . "m";
	$replacement = $bclrstr . '${1}' . $nclrstr;
	$retval = preg_replace("/([A-Z:<>])/", $replacement, $text);
	return $retval . "\033[0m";
}

/**
 * Color by character case.
 * 
 * Capitals returns in bold of suplied color, lowercase in suplied color.
 * 
 * @param string $text Input text to color
 * @param int $boldcolor Color for lowercase letters
 * @return string Colored text.
 */
function func_casebold($text, $boldcolor) {
	$bclrstr = "\033[1m\033[3" . $boldcolor . "m";
	$nclrstr = "\033[0m\033[3" . $boldcolor . "m";
	$replacement = $bclrstr . '${1}' . $nclrstr;
	$retval = preg_replace("/([A-Z:<>])/", $replacement, $text);
	return $retval . "\033[0m";
}

/**
 * Process user entered color codes.
 * 
 * Uses color codes contained in curly braces.  Standard ANSI codes work.
 * 
 * @todo Add error correction and checking.  Could be used to hose other players.
 * @param string $text Text to convert to escape string
 * @return string Fully escaped string
 */
function func_colorcode($text) {
	$replacement = "\033[" . '${1}' . "m";
	return preg_replace("/\{(\d+)\}/", $replacement, $text);
}

/**
 * Return a standard colored menu entry.
 * 
 * @param string $text Text to convert to menu entry
 * @return string Fully escaped string
 */
function func_normmenu($text) {
	$bclrstr = "  \033[0m\033[32m(\033[1;35m";
	$nclrstr = "\033[0m\033[32m)";
	$replacement = $bclrstr . '${1}' . $nclrstr;
	$retval = preg_replace("/\(([A-Z:<>])\)/", $replacement, $text);
	return $retval . "\033[0m\n";
}

/**
 * Pad a selection of text to be a specied number of columns wide.
 * 
 * @param string $text Text to pad
 * @param int $col Number of columns to fill
 * @return string String of spaces to finish column
 */
function padnumcol($text, $col) {
	$col = $col - strlen($text);
	$ittr = 0; $retval = "";
	while ( $ittr < $col ) { $retval .= " "; $ittr++; }
	return $retval;
}

/**
 * Pad a selection of text to be a specied number of columns wide, right justified.
 * 
 * @param string $text Text to pad
 * @param int $col Number of columns to fill
 * @return string Fully padded text
 */
function padright($text, $col) {
	$col = $col - strlen($text);
	$ittr = 0; $retval = "";
	while ( $ittr < $col ) { $retval .= " "; $ittr++; }
	$retval .= $text;
	return $retval;
}

/**
 * Pause for user confirmation
 */
function pauser() {
	slowecho(func_casebold("\n    :-: Press Any Key :-:", 2));
	$dumper = fgets(STDIN);
}

/**
 * Echo text to user, with delay between each printed character to mimic slow modem speed opertaion.
 * 
 * @param string $text Text to display to user
 */
function slowecho($text) {
	global $SORDDELAY;
	$text = preg_replace("/\\n/", "\r\n", $text);
	foreach( mb_str_split($text) as $char ) { echo $char; usleep($SORDDELAY); }
}

/** Split a multi-byte string - which our data likely is.
 * 
 * @param string $str Text to split
 * @param int $length Length to split to [optional]
 * @return array split text.
 */
function mb_str_split($str, $length = 1) {
	if ($length < 1) return FALSE;
	$result = array();
	for ($i = 0; $i < mb_strlen($str); $i += $length) {
		$result[] = mb_substr($str, $i, $length);
	}
	return $result;
}

/** 
 * Signal handler to catch signals from the operating system.
 * 
 * @param string $signal Signal type to process
 */
function signal_handler($signal) {
	switch($signal) {
		case SIGTERM:
			echo "Quitting: Caught SIGTERM\n"; exit;
		case SIGQUIT:
			echo "Quitting: Caught SIGQUIT\n"; exit;
		case SIGINT:
			echo "Quitting: Caught SIGINT\n"; exit;
		case SIGALRM:
			die("Connection Timed out, Disconnecting.\n");
	}
}

?>
