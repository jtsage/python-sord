<?php
function menu_2col($text1, $text2, $col1, $col2) {
  $bclrstr1 = "\033[0m\033[32m(\033[1;3{$col1}m";
  $nclrstr1 = "\033[0m\033[32m)";
  $replacement = $bclrstr1 . '${1}' . $nclrstr1;
  $text1col = preg_replace("/\(([A-Z:<>])\)/", $replacement, $text1);
  $bclrstr2 = "\033[0m\033[32m(\033[1;3{$col2}m";
  $nclrstr2 = "\033[0m\033[32m)";
  $replacement = $bclrstr2 . '${1}' . $nclrstr2;
  $text2col = preg_replace("/\(([A-Z:<>])\)/", $replacement, $text2);
  return "  " . $text1col . padnumcol($text1, 36) . $text2col . "\033[0m\n";
}

function menu_bank() {
  GLOBAL $userid, $logontime;
  $currenttime = time(); $ontime = $currenttime - $logontime;
  $sec = $ontime % 60;
  $min = ( $ontime - $sec ) / 60;
  $psec = ( $sec < 10 ) ? "0{$sec}" : $sec;

  $thismenu  = "\n\n  \033[1;37mSaga of the Red Dragon - \033[0m\033[32mBank\033[0m\n";
  $thismenu .= art_line();
  $thismenu .= "  \033[32mA polite clerk approaches. \033[1;35m\"Can I help you sir?\"\033[0m\n\n";
  $thismenu .= func_normmenu("(D)eposit Gold");
  $thismenu .= func_normmenu("(W)ithdraw Gold");
  $thismenu .= func_normmenu("(T)ransfer Gold");
  $thismenu .= func_normmenu("(R)eturn to Town");
  $thismenu .= "\n\n\033[32m  Gold In Hand: \033[1m" . user_getgold($userid);
  $thismenu .= "\033[0m\033[32m Gold In Bank: \033[1m" . user_getbank($userid). "\n";
  $thismenu .= "\033[35m  The Bank \033[1;30m(W,D,R,T,Q) (? for menu)\033[0m\n\n";
  $thismenu .= "  \033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[1;37m[\033[22m{$min}:{$psec}\033[1m] \033[0m\033[32m:-: \033[0m";
  return $thismenu;
}

function menu_mainlong($noprmpt) {
  $thismenu  = "\n\n\033[1;37m  Saga of the Red Dragon - \033[0m\033[32mTown Square\033[0m\n";
  $thismenu .= art_line();
  $thismenu .= "\033[32m  The streets are crowded, it is difficult to\n  push your way through the mob....\n\n";
  $thismenu .= menu_2col("(F)orest", "(S)laughter other players", 5, 5);
  $thismenu .= menu_2col("(K)ing Arthurs Weapons", "(A)bduls Armour", 5, 5);
  $thismenu .= menu_2col("(H)ealers Hut", "(V)iew your stats", 5, 5);
  $thismenu .= menu_2col("(I)nn", "(T)urgons Warrior Training", 5, 5);
  $thismenu .= menu_2col("(Y)e Old Bank", "(L)ist Warriors", 5, 5);
  $thismenu .= menu_2col("(W)rite Mail", "(D)aily News", 5, 5);
  $thismenu .= menu_2col("(C)onjugality List", "(O)ther Places", 5, 5);
  $thismenu .= menu_2col("(X)pert Mode", "(M)ake Announcement", 7, 5);
  $thismenu .= menu_2col("(P)eople Online", "(Q)uit to Fields", 5, 2);
  $thismenu .= ( $noprmpt ) ? "" : menu_mainshort();
  return $thismenu;
}

function menu_mainshort() {
  GLOBAL $userid, $logontime;
  $currenttime = time(); $ontime = $currenttime - $logontime;
  $sec = $ontime % 60;
  $min = ( $ontime - $sec ) / 60;
  $psec = ( $sec < 10 ) ? "0{$sec}" : $sec;

  $thismenu  = "\n  \033[1;35mThe Town Square\033[0m\033[1;30m (? for menu)\033[0m\n";
  $thismenu .= "  \033[1;30m(F,S,K,A,H,V,I,T,Y,L,W,D,C,O,X,M,P,Q)\033[0m\n\n";
  $thismenu .= "  \033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[1;37m[\033[22m{$min}:{$psec}\033[1m] \033[0m\033[32m:-: \033[0m";
  return $thismenu;
}

function menu_abdul() {
  GLOBAL $userid, $armor, $logontime;
  $currenttime = time(); $ontime = $currenttime - $logontime;
  $sec = $ontime % 60;
  $min = ( $ontime - $sec ) / 60;
  $psec = ( $sec < 10 ) ? "0{$sec}" : $sec;

  $thisarmour = user_getarmor($userid);
  $thismenu  = "\n  \033[32mCurrent armour: \033[1m{$armor[$thisarmour]}\033[0m\n";
  $thismenu .= "  \033[1;35mAbduls Armour \033[1;30m(B,S,Y,R) (? for menu)\n\n";
  $thismenu .= "  \033[0m\033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[1;37m[\033[22m{$min}:{$psec}\033[1m] \033[0m\033[32m:-: \033[0m";

  return $thismenu;
}


function menu_arthur() {
  GLOBAL $userid, $weapon, $logontime;
  $currenttime = time(); $ontime = $currenttime - $logontime;
  $sec = $ontime % 60;
  $min = ( $ontime - $sec ) / 60;
  $psec = ( $sec < 10 ) ? "0{$sec}" : $sec;

  $thisweapon = user_getweapon($userid);
  $thismenu  = "\n  \033[32mCurrent weapon: \033[1m{$weapon[$thisweapon]}\033[0m\n";
  $thismenu .= "  \033[1;35mKing Arthur's Weapons \033[1;30m(B,S,Y,R) (? for menu)\n\n";
  $thismenu .= "  \033[0m\033[32mYour command, \033[1m" . user_gethandle($userid) . "\033[22m? \033[1;37m[\033[22m{$min}:{$psec}\033[1m] \033[0m\033[32m:-: \033[0m";

  return $thismenu;
}




?>
