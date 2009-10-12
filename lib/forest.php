<?php
/**
 * Fighting Subsystem.
 * 
 * Contains forest fights, events, player fights, leveling up
 * 
 * @package phpsord
 * @subpackage phpsord-ui
 * @author J.T.Sage
 * @todo Player fight subsystem, horses.
 */

/**
 * Forest Special Events
 * 
 * Special forest event happenings
 * 
 * @todo Add all elements as needed.
 * 	- gems (done)
 * 	- gold (done)
 * 	- old man (done)
 * 	- ugly / pretty stick (done)
 * 	- old hag (done)
 * 	- fairies
 * 	- dark horse tavern
 * 	- lessons
 * 	- merry men (done)
 * 	- rescue man/maiden
 * 	- flowers (done)
 * 	- hammerstone (done)
 */
function forest_special() {
	GLOBAL $userid, $db, $MYSQL_PREFIX;
	$happening = rand(1, 12);
	switch ( $happening ) {
		case 1: // Find Gems
			$thisfind = rand(1, 4);
			slowecho(art_line());
			slowecho("  \033[32mFortune Smiles Upon You.  You find \033[1;37m{$thisfind}\033[0m\033[32m gems!\033[0m\n");
			slowecho(art_line());
			pauser();
			user_givegems($userid, $thisfind);
			break;
		case 2: // Find Gold
			$thisfind = rand(1, 4) * 200 * user_getlevel($userid);
			slowecho(art_line());
			slowecho("  \033[32mFortune Smiles Upon You.  You find a sack full of \033[1;37m");
			slowecho(number_format($thisfind, 0));
			slowecho("\033[0m\033[32m gold!\033[0m\n");
			slowecho(art_line());
			pauser();
			user_givegold($userid, $thisfind);
			break;
		case 3: // Hammerstone (attack str++)
			slowecho(art_line());
			slowecho("  \033[32mYou find a hammer stone.  You quickly hit it as hard as possible.\n \033[1mYour attack strength is raised by 1!\033[0m\n");
			slowecho(art_line());
			pauser();
			user_givestr($userid, 1);
			break;
		case 4: // Merry Men (hp = hpmax)
			slowecho(art_line());
			slowecho("  \033[32mYou stumble across a group of merry men.  They offer you ale you can't resist.\n \033[1mYou feel refreshed!\033[0m\n");
			slowecho(art_line());
			pauser();
			$sql = "UPDATE {$MYSQL_PREFIX}stats SET hp = hpmax WHERE userid = {$USERID}";
			$result = mysql_query($sql, $db);
			break;
		case 5: // Old Man (gold + (lvl * 500) && charm +1 on help)
			slowecho(art_line());
			slowecho("  \033[32mYou come upon an old man wandering around.\n  He asks you for help back to town.\033[0m\n");
			slowecho(func_normmenu("(H)elp the old man"));
			slowecho(func_normmenu("(I)gnore him"));
			slowecho("  \033[0m\033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[0m\033[32m:-: \033[0m");
			$miniquit = 0;
			while ( !$miniquit ) {
				$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
				switch ($choice) {
					case "H":
						$goldgotten = user_getlevel($userid) * 500;
						slowecho("\n  \033[32mYou help the old gentleman home.\033[1mHe gives you ");
						slowecho(number_format($goldgotten,0));
						slowecho(" gold and 1 charm!.\033[0m\n");
						user_givegold($userid, $goldgotten);
						user_givecharm($userid, 1);
						$miniquit = 1;
						break;
					case "I":
						slowecho("\n  \033[31mYou just really \033[1mSUCK\033[0;31m, don't you?\033[0m\n");
						$miniquit = 1;
						break;
				}
			}
			pauser();
			break;
		case 6: // Ugly (33%) and Pretty (66%) stick
			slowecho(art_line());
			slowecho("  \033[32mA demented penguin jumps from the bushes and whacks you with a");
			$sticktype = rand(1, 3);
			if ( $sticktype == 2 ) { slowecho("\033[1,31mugly\033[0,32m"); } else { slowecho("\033[1mpretty\033[0,32m"); }
			slowecho("stick!  Your charm is ");
			if ( $sticktype == 2 ) { slowecho("lowered"); } else { slowecho("raised"); }
			slowecho("by 1!!\033[0m\n");
			if ( $sticktype == 2 ) {
				$currentcharm = user_getcharm($userid);
				if ( $currentcharm > 0 ) { user_takecharm($userid, 1); }
			} else {
				user_givecharm($userid, 1);
			}
			pauser();
			break;
		case 7: // old hag
			slowecho(art_line());
			slowecho("  \033[32mYou come across an old hag.\n  \033[1m\"Give me a gem my pretty, and I will completely heal you!\"\033[0,32m\n  She screeches!\033[0m\n");
			slowecho(func_normmenu("(G)ive her a gem"));
			slowecho(func_normmenu("(K)ick her and run"));
			slowecho(func_normmenu("(L)eave polietly"));
			slowecho("  \033[0m\033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[0m\033[32m:-: \033[0m");
			$miniquit = 0;
			while ( !$miniquit ) {
				$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
				switch ($choice) {
					case "L":
						slowecho("\n  \033[32mThe old hag begins following you like a lost puppy.\033[0m\n");
						break;
					case "K":
						slowecho("\n  \033[32mYou hate to be rude to your elders, but sometimes deperate times call for\n  deperate measures.  You which the old hag in the shin and run for it.\033[0m\n");
						$miniquit = 1;
						break;
					case "G":
						if ( user_getgems($userid) > 0 ) {
							slowecho("\n  \033[1,32m\"Thank you\"\033[0,32m she cackles.\n  \033[1mYou feel refreshed and renewed\033[0m\n");
							user_givehpmax($userid, 1);
							$this_maxhp = user_gethpmax($userid);
							$hptoheal = user_gethpmax($userid) - user_gethp($userid);
							user_givehp($userid, $hptoheal);
							$miniquit = 1;
							user_takegems($userid, 1);
						} else {
							slowecho("\n  \033[1,32m\"You don't have any gems you stinky cow-pox pustule!\"\[33[0,32m she yells.\n  \033[1mCome to think of it, you feel rather like a cow-pie.\033[0m\n");
							$this_hp = $user_gethp($userid);
							user_takehp($userid, ($this_hp - 1));
							$miniquit = 1;
						}
						break;
				}
			}
			pauser();
			break;
		case 8: // Flowers in the forest.
			slowecho(art_line());
			slowecho("  \033[32mYou come across a grove of flowers, and decide to inspect them closer...\n  \033[1mThere is something written here!\033[0m\n");
			pauser();
			module_flowers();
			break;
		case 9: // rescue man/maiden
			slowecho(art_line());
			slowecho("  \033[32mYou come upon a dead bird.  While gross, you begin to put it out of your\n  mind when you notice a scroll attached to it's leg\n\n");
			slowecho("  \033[1mTo Whome It May Concern:\n    I have been locked in this terrible tower for many cycles.\n    Please save me soon!\n        ~ Elora\n\n");
			slowecho(func_normmenu("(S)eek the maiden"));
			slowecho(func_normmenu("(I)gnore her plight"));
			slowecho("\n  \033[0m\033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[0m\033[32m:-: \033[0m");
			$miniquit = 0;
			while ( !$miniquit ) {
				$choice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
				switch($choice) {
					case "I":
						$miniquit = 1;
						break;
					case "S":
						$miniquit2 = 0; $towerselection = 0;
						slowecho("\n  \033[32mWhere do you wish to seek the maiden?\033[0m\n");
						slowecho(func_normmenu("(K)eep of Hielwain"));
						slowecho(func_normmenu("(S)tarbucks Seattle Spaceneedle"));
						slowecho(func_normmenu("(C)astle Morbidia"));
						slowecho(func_normmenu("(S)ty of Pigashia"));
						slowecho(func_normmenu("(B)logshares Brutal Belfry"));
						slowecho("\n  \033[0m\033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[0m\033[32m:-: \033[0m");
						while ( !$miniquit2 ) {
							$minichoice = preg_replace("/\r\n/", "", strtoupper(substr(fgets(STDIN), 0, 1)));
							switch($minichoice) {
								case "K":
									$towerselection = 1; $miniquit2 = 1; break;
								case "S":
									$towerselection = 2; $miniquit2 = 1; break;
								case "C":
									$towerselection = 3; $miniquit2 = 1; break;
								case "S":
									$towerselection = 4; $miniquit2 = 1; break;
								case "B":
									$towerselection = 5; $miniquit2 = 1; break;
							}
						}
						slowecho(art_tower()); pauser();
						$correctselection = rand(1, 5);
						if ( $towerselection == $correctselection ) { // GOT IT RIGHT!
							slowecho("\n  \033[32mYou have choosen \033[1mwisely.\033[0m\n");
							slowecho("  \033[32mElora gasps in suprise, saunters over, and thanks you 'properly'\n  \033[1mYou feel smarter, more gem laden, and -erm- 'satisfied'\033[0m\n");
							user_givegems($userid, 5);
							$this_gold = user_getlevel($userid) * 500;
							user_givegold($userid, $this_gold);
						} else { // GOT IT WRONG
							if ( rand(0, 1) == 1 ) { //REALLY WRONG.
								slowecho("\n  \033[32mYou have choosen \033[1mpoorly.  really poorly.\033[0m\n");
								slowecho("  \033[32mYou hear a strange groan and out pops Ken Adams, the disfigured midger (er, 'little person').\n  Sadly, 'little person' doesn't refer to all of him.\n  \033[1mYou feel terrible, both physically and mentally\033[0m\n");
								$this_hp = user_gethp($userid) - 1;
								user_takehp($userid, $this_hp);
							} else { // WRONG, NOT TOO BAD
								slowecho("\n  \033[32mYou have choosen \033[1mpoorly.\033[0m\n");
								slowecho("  \033[32mYou run like hell before anything bad happens.\033[0m\n");
							}
						}
						$miniquit = 1;
						break;
				}
			}
			pauser();
			break;


		default: // Not yet implemented options
			slowecho(func_casebold("Happening # {$happening}", 1)); pauser();
	}
}

/**
 * Forest Fights
 * 
 * Player vs. Monster system
 * 
 */
function forest_fight() {
	GLOBAL $userid, $enemies, $forestdie;
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
			case 'Q':
				slowecho("\n  \033[31mYou are in Combat!  Try Running!\033[0m\n");
				break;
			case 'H':
				slowecho("\n  \033[32mYou are in combat, and they don't make house calls!\033[0m\n");
				break;
			case 'L':
				slowecho("\n  \033[32mWhat?!  You want to fight two at once?\033[0m\n");
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
		user_logout($userid);
		$lamenttop = (count($forestdie)) - 1;
		$thislament = $forestdie[rand(0, $lamenttop)];
		$thislament = preg_replace("/`n/", "\n", $thislament);
		$thislament = preg_replace("/`g/", user_gethandle($userid), $thislament);
		$thislament = preg_replace("/`e/", $enemyname, $thislament);
		$thislament = mysql_escape_string($thislament);
		$sql = "INSERT INTO {$MYSQL_PREFIX}daily ( `data` ) VALUES ('{$thislament}')";
		$result = mysql_query($sql, $db);
		die(func_casebold("  Tragically, you died.  Returning to the mundane world for the day...\n"));
	}
}

/**
 * Forest Fight Menu
 * 
 * Menu used during a fight
 * 
 * @param int $uhp User's HitPoints
 * @param int $ehp Enemy's HitPoints
 * @param string $ename Enemy's Name
 * @todo Special Skills section
 */
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

/**
 * Master Fight Subsystem
 * 
 * System for leveling up
 */
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
				$masterql = "UPDATE {$MYSQL_PREFIX}stats SET master = 1 WHERE userid = {$userid}"; 
				$result = mysql_query($resethp, $db);
				$result = mysql_query($masterql, $db);
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
		$result = mysql_query($masterql, $db);
		pauser();
	}
}
?>
