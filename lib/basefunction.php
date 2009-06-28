<?php

function func_caseclr($text, $boldcolor, $normcolor) {
	$bclrstr = "\033[1m\033[3" . $boldcolor . "m";
	$nclrstr = "\033[0m\033[3" . $normcolor . "m";
	$replacement = $bclrstr . '${1}' . $nclrstr;
	$retval = preg_replace("/([A-Z:<>])/", $replacement, $text);
	return $retval . "\033[0m";
}

function func_casebold($text, $boldcolor) {
        $bclrstr = "\033[1m\033[3" . $boldcolor . "m";
        $nclrstr = "\033[0m\033[3" . $boldcolor . "m";
        $replacement = $bclrstr . '${1}' . $nclrstr;
        $retval = preg_replace("/([A-Z:<>])/", $replacement, $text);
        return $retval . "\033[0m";
}

function func_colorcode($text) {
	$replacement = "\033[" . '${1}' . "m";
	return preg_replace("/\{(\d+)\}/", $replacement, $text);
}

function func_normmenu($text) {
        $bclrstr = "  \033[0m\033[32m(\033[1;35m";
        $nclrstr = "\033[0m\033[32m)";
        $replacement = $bclrstr . '${1}' . $nclrstr;
        $retval = preg_replace("/\(([A-Z:<>])\)/", $replacement, $text);
        return $retval . "\033[0m\n";
}

function padnumcol($text, $col) {
	$col = $col - strlen($text);
	$ittr = 0; $retval = "";
	while ( $ittr < $col ) { $retval .= " "; $ittr++; }
	return $retval;
}

function padright($text, $col) {
	$col = $col - strlen($text);
	$ittr = 0; $retval = "";
        while ( $ittr < $col ) { $retval .= " "; $ittr++; }
	$retval .= $text;
	return $retval;
}

function pauser() {
	slowecho(func_casebold(":-: Press Any Key :-:", 2));
	$dumper = fgets(STDIN);
}

function slowecho($text) {
	global $SORDDELAY;
	$text = preg_replace("/\\n/", "\r\n", $text);
	foreach( str_split($text) as $char ) { echo $char; usleep($SORDDELAY); }
}

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
