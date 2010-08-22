#!/usr/bin/python

import sordfunc, sqlite3

print "Content-type: text/html\n"
print "<html><head><title>S.O.R.D. Stats</title></head><body style=\"background-color: #000; color: #fff\">"

print "<center><font size=\"+1\"><pre>"
print "<b><span style=\"color: #F77\">S</span><span style=\"color: #F00\">aga</span> <span style=\"color: #F77\">O</span><span style=\"color: #F00\">f</span> <span style=\"color: #F77\">T</span><span style=\"color: #F00\">he</span> <span style=\"color: #F77\">R</span><span style=\"color: #F00\">ed</span> <span style=\"color: #F77\">D</span><span style=\"color: #F00\">ragon</span></b>"
print "<span style=\"color: #6F6\">Player Standings</span>\n\n"


dbc = sqlite3.connect("../sord.db")

db = dbc.cursor()
db.execute("SELECT userid, fullname, exp, level, cls, spclm, spcld, spclt, sex, alive FROM users WHERE 1 ORDER BY exp DESC")
print "\n<span style=\"color: green\">     Name                    Experience    Level    Mastered    Status       </span>"
print sordfunc.line()
output = ""
for line in db.fetchall():
	if ( line[8] == 2 ):
		lineSex = "<span style=\"color: magenta\">F</span> "
	else:
		lineSex = "  "
		
	lineClass = "<span style=\"color:#F77\">"
	if ( line[4] == 1 ):
		lineClass += "D "
	elif ( line[4] == 2 ):
		lineClass += "M "
	else:
		lineClass += "T "
	lineClass += "</span>"
	
	lineMaster = ""
	if ( line[6] > 19 ):
		if ( line[6] > 39 ):
			lineMaster += "<span style=\"color:#fff\">D </span>"
		else:
			lineMaster += "<span style=\"color:#ccc\">D </span>"
	else:
		lineMaster += "  "
		
	if ( line[5] > 19 ):
		if ( line[5] > 39 ):
			lineMaster += "<span style=\"color:#fff\">M </span>"
		else:
			lineMaster += "<span style=\"color:#ccc\">M </span>"
	else:
		lineMaster += "  "
					
	if ( line[7] > 19 ):
		if ( line[7] > 39 ):
			lineMaster += "<span style=\"color:#fff\">T </span>"
		else:
			lineMaster += "<span style=\"color:#ccc\">T </span>"
	else:
		lineMaster += "  "
								
	
	if ( line[9] == 1 ):
		lineStatus = "<span class=\"color: #6F6\">Alive</span>"
	else:
		lineStatus = "<span class=\"color: #F00\"> Dead</span>"
		
	output += lineSex + lineClass + "<span style=\"color: green\"> " + line[1] + sordfunc.padnumcol(str(line[1]), 24) + sordfunc.padright(str(line[2]), 10)
	output += sordfunc.padright(str(line[3]), 9) + "       " + lineMaster + '    ' + lineStatus + "       \n"
db.close()
dbc.close()
print output
print sordfunc.line()
print "</pre></font></center>"

print "</body></html>"

