<?php

function art_banner() {
    $thismsg  = "\033[32m                           Saga Of The Red Dragon\n\n";
    $thismsg .= "\033[32m                    Compiled June 25, 2009: Version \033[1;37m1.00\n";
    $thismsg .= "\033[32m                        (c) pre-2009 by Someone Else\n\n";
    $thismsg .= "\033[32m                        \033[1;37mREGISTERED \033[0m\033[32m(AND INCOMPLETE!)\n\n";
    $thismsg .= "\033[32m                The current game has been running for a while.\n";
    $thismsg .= "\033[32m               Players are deleted after \033[1m30\033[22m days of inactivity.\n\n";
    $thismsg .= "\033[32m                         (\033[1mE\033[22m)nter the realm of the Dragon\n";
    $thismsg .= "\033[32m                         (\033[1mL\033[22m)ist Warriors\n";
    $thismsg .= "\033[32m                         (\033[1mQ\033[22m)uit the game server\n\n";
    $thismsg .= "\033[32m                         Your choice, warrior? [\033[1mE\033[22m]: \033[0m";
    return $thismsg;
}

function art_line() {
    return "\033[32m-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n";
}
    
function art_header() {
    $thismsg  = "\033[0m\033[37;40m \033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°\033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°±²²²²²²²±°±²²²²²²²±°±²²²²²²²±°±²²²²²²±°°°\033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°±²±±±±±±±°±²±°°°°²±°±²±°°°°²±°±²±°°°²²±°°\033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°±²°°°°°°°°±²±°°°°²±°±²±°°°°²±°±²±°°°°²²±°\033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°±²²²²²²²±°±²±°°°°²±°±²²²²²²²±°±²±°°°°°²±°\033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°°±±±±±²²±°±²±°°°°²±°±²±²²±±±±°±²±°°°°°²±°\033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°°°°°°°²²±°±²±°°°°²±°±²±°°²²±°°±²±°°°°²²±°\033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°±²²²²²²²±°±²²²²²²²±°±²±°°°²²±°±²²²²²²±±°°\033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°°±±±±±±±±°°±±±±±±±±°±±±°°°±±±°±±±±±±±±°°°\033[0m\n";
    $thismsg .= "\033[37;40m \033[1m\033[31;40m°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°\033[0m\n";
    $thismsg .= func_caseclr("  >> Saga Of the Red Dragon", 1, 7) . "\n";
    $thismsg .= func_caseclr("   >> A Shameless Ripoff of Seth Ables's Masterpiece\n", 7, 7);
    return $thismsg . "\n";
}

?>
