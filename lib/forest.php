<?php
function forest_special() {
	GLOBAL $userid;
	$happening = rand(1, 12);
	slowecho(func_casebold("Happening # {$happening}", 1)); pauser();
	switch ( $happening ) {
			
	}
}

function forest_fight() {
	GLOBAL $userid, $enemies;
	user_takeffight($userid, 1);
	$userlevel = user_getlevel($userid);
	$topenemy = (count($enemies[$userlevel])) - 1;
	$thisenemy = rand(0, $topenemy);
	$firsthit = rand(0, 10); 
	$thisunderdog = ( $firsthit == 8 ) ? 1 : 0;
	$userstr = user_getstr($userid);
	$userdef = user_getdef($userid);
	$userhstr = ($userstr - ($userstr % 2)) / 2;
	$userhp = user_gethp($userid);
	$dead = 0; $ran = 0; $win = 0;

	$enemystr = $enemies[$userlevel][$thisenemy][2];
	$enemyhstr = ($enemystr - ($enemystr % 2)) / 2;
	$enemyhp = $enemies[$userlevel][$thisenemy][3];
	$enemyname = $enemies[$userlevel][$thisenemy][0];
	$enemywep = $enemies[$userlevel][$thisenemy][1];
	
	slowecho("\n\n  \033[32m**\033[1;37mFIGHT\033[0m\033[32m**\n");
	slowecho("\n  \033[32mYou have encountered {$enemyname}!!\033[0m\n");

	if ( $thisunderdog ) {
		$eattack =  (( $enemyhstr ) + rand(0, $enemyhstr) ) - $userdef;
		if ( $eattack > 0 ) {
			if ( $eattack > $userhp ) { $eattack = $userhp; $dead = 1;}
			slowecho("\n  \033[32m{$enemyname} executes a sneak attach for \033[1;31m{$eattack}\033[0m\033[32m damage!\033[0m\n");
			user_takehp($userid, $eattack);
		} else { slowecho("\n  \033[32m{$enemyname} misses you completely!\033[0m\n"); }
	} else { slowecho("\n  \033[32mYour skill allows you to get the first strike.\033[0m\n"); }
	
	while( $userhp > 0 && $enemyhp > 0 && !$dead && !$ran) {  ## FIGHT LOOP ##
		$userhp = user_gethp($userid);
		slowecho(forest_menu($userhp, $enemyhp, $enemyname));
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                switch ($choice) {
			case 'S':
				module_viewstats($userid);
				break;
			case 'A':
				$eattack =  (( $enemyhstr ) + rand(0, $enemyhstr) ) - $userdef;
				$uattack =  (( $userhstr ) + rand(0, $userhstr));
				if ( !$thisunderdog ) { if ( $uattack > $enemyhp ) { $eattack = 0; } }
                                if ( $eattack > $userhp ) { $eattack = $userhp; $dead = 1;}
				if ( $eattack > 0 ) {
					slowecho("\n  \033[32m{$enemyname} hits you with {$enemywep} for \033[1;31m{$eattack}\033[0m\033[32m damage\033[0m\n"); 
					user_takehp($userid, $eattack);
				}
				if ( $uattack > 0 && !$dead) { 
					slowecho("\n  \033[32mYou hit {$enemyname} for \033[1;31m{$uattack}\033[0m\033[32m damage\n"); 
					$enemyhp = $enemyhp - $uattack;
					if ( $enemyhp < 1 ) { 
						slowecho("  \033[31m{$enemies[$userlevel][$thisenemy][6]}\n"); 
						$win = 1; }
				}
				break;
			case 'R':
				$madeit = rand(1, 9);
				if ( $madeit == 4 ) {
					$eattack =  (( $enemyhstr ) + rand(0, $enemyhstr) ) - $userdef;
					if ( $eattack > $userhp ) { $eattack = $userhp; }
					if ( $eattack > 0 ) {
						slowecho("\n  \033[32m{$enemyname} hits you in the back with it's {$enemywep} for \033[1;31m{$eattack}\033[0m\033[32m damage\n"); 
						user_takehp($userid, $eattack); }
				} else {
					slowecho("\n  \033[32mYou narrowly escape harm.\033[0m\n"); 
					$ran = 1; }
				break;
		}
	}
	if ( $win ) {
		user_giveexp($userid, $enemies[$userlevel][$thisenemy][5]);
		user_givegold($userid, $enemies[$userlevel][$thisenemy][4]);
		slowecho("\n  \033[32mYou have recieved \033[1m{$enemies[$userlevel][$thisenemy][4]}\033[22m gold and \033[1m{$enemies[$userlevel][$thisenemy][5]}\033[22m experience\033[0m\n");
		pauser();
	}
	if ( $dead ) {
		user_setdead($userid);
		die(func_casebold("  Tragically, you died.  Returning to the mundane world for the day...\n"));
	}
}

function forest_menu($uhp, $ehp, $ename) {
	GLOBAL $userid;
	$thismenu .= "\n  \033[32mYour Hitpoints : \033[1m{$uhp}\033[0m\n";
	$thismenu .= "  \033[32m{$ename}'s Hitpoints : \033[1m{$ehp}\033[0m\n\n";
	$thismenu .= func_normmenu("(A)ttack");
	$thismenu .= func_normmenu("(S)tats");
	$thismenu .= func_normmenu("(R)un");
	/* SPECIAL SKILLS SECTION - ADD THIS*/
	$thismenu .= "\n  \033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? [\033[1;35mA\033[0m\033[32m] : \033[0m";
	return $thismenu;
}



function master_fight() {
	GLOBAL $userid, $masters, $masterwin, $db, $MYSQL_PREFIX;
	$userlevel = user_getlevel($userid);
	$thisunderdog = 0;
	$userstr = user_getstr($userid);
	$userdef = user_getdef($userid);
	$userhstr = ($userstr - ($userstr % 2)) / 2;
	$userhp = user_gethp($userid);
	$dead = 0; $ran = 0; $win = 0;

	$enemystr = $masters[$userlevel][7];
	$enemydef = $masters[$userlevel][8];
	$enemyhstr = ($enemystr - ($enemystr % 2)) / 2;
	$enemyhp = $masters[$userlevel][6];
	$enemyname = $masters[$userlevel][0];
	$enemywep = $masters[$userlevel][1];
	
	slowecho("\n\n  \033[32m**\033[1;37mFIGHT\033[0m\033[32m**\n");
	slowecho("\n  \033[32mYour skill allows you to get the first strike.\033[0m\n"); 
	
	while( $userhp > 0 && $enemyhp > 0 && !$dead && !$ran) {  ## FIGHT LOOP ##
		$userhp = user_gethp($userid);
		slowecho(forest_menu($userhp, $enemyhp, $enemyname));
		$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
                switch ($choice) {
			case 'S':
				module_viewstats($userid);
				break;
			case 'A':
				$eattack =  (( $enemyhstr ) + rand(0, $enemyhstr) ) - $userdef;
				$uattack =  (( $userhstr ) + rand(0, $userhstr)) - $enemydef;
				if ( !$thisunderdog ) { if ( $uattack > $enemyhp ) { $eattack = 0; } }
                                if ( $eattack > $userhp ) { $eattack = $userhp; $dead = 1;}
				if ( $eattack > 0 ) {
					slowecho("\n  \033[32m{$enemyname} hits you with {$enemywep} for \033[1;31m{$eattack}\033[0m\033[32m damage\033[0m\n"); 
					user_takehp($userid, $eattack);
				}
				if ( $uattack > 0 && !$dead) { 
					slowecho("\n  \033[32mYou hit {$enemyname} for \033[1;31m{$uattack}\033[0m\033[32m damage\n"); 
					$enemyhp = $enemyhp - $uattack;
					if ( $enemyhp < 1 ) { 
						slowecho("  \033[31m{$masters[$userlevel][5]}\n"); 
						$win = 1; }
				}
				break;
			case 'R':
				slowecho("\n  \033[32mYou retire from the field before getting yourself killed.\033[0m\n"); 
				$resethp = "UPDATE {$MYSQL_PREFIX}stats set hp = hpmax WHERE userid = {$userid}";
				$result = mysql_query($resethp, $db);
				$ran = 1; 
				break;
		}
	}
	if ( $win ) {
		$addexp = $masters[$userlevel][2] * .1;
		user_giveexp($userid, $addexp);
		user_givedef($userid, $masterwin[$userlevel][2]);
		user_givestr($userid, $masterwin[$userlevel][1]);
		user_givehpmax($userid, $masterwin[$userlevel][0]);
		slowecho("\n  \033[32mYou have receieved \033[1m+{$masterwin[$userlevel][2]}\033[22m vitality, \033[1m+{$masterwin[$userlevel][1]}\033[22m strength, and \033[1m+{$masterwin[$userlevel][0]}\033[22m hitpoints.\033[0m\n");
		$newlevel = user_getlevel($userid) + 1;
		slowecho("  \033[32mYou have gained \033[1m{$addexp}\033[22m experience, and are now level \033[1m{$newlevel}\033[22m.\033[0m\n");
		user_setlevel($userid, $newlevel);
		$resethp = "UPDATE {$MYSQL_PREFIX}stats set hp = hpmax WHERE userid = {$userid}";
		$result = mysql_query($resethp, $db);
		pauser();
	}
	if ( $dead ) {
		slowecho("\n  \033[31mTragically, you are horribly disfigured....  oh wait...\033[0m\n");
		slowecho("  \033[31mYou always looked like that you say?...  That's unfortunate...\033[0m\n");
		slowecho("  \033[32mAnyway, you lost.  Being the gracious master {$enemyname} is, he heals you and sends you away for the day.\033[0m\n");
		$resethp = "UPDATE {$MYSQL_PREFIX}stats set hp = hpmax WHERE userid = {$userid}";
		$masterql = "UPDATE {$MYSQL_PREFIX}stats SET master = 1 WHERE userid = {$userid}"; 
		$result = mysql_query($resethp, $db);
		pauser();
	}
}
?>