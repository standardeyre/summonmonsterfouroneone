summonmonsterfouroneone
=======================

 
Directory assistance for Summon Monster spells in the PFRPG


Description
===========

This application "summonmonsterfouroneone" is a tool to assist players with finding the right monster to summon using the various Summon Monster spells available in the PFRPG.

This application "summonmonsterfouroneone" (or sm411) 
will help players of the PFRPG with "Directory Assistance" 
searching  all possible monsters
that might be called
with various Summon Monster spells.


Why is this needed?  Suppose you are playing a character with access to the spell *Summon Monster V*.   This lets you summon one single monster from the fifth level monster list, between one and three monsters from the fourth level monster list, or between two and five monsters from any lower level list.   One of the options on the fourth level list is "mephit," which is actually a choice of one mephit out of the eight different types of mephit that may be summoned.  A different option is to summon an elemental, which is actually a choice out of four different elements.  One of those mephits can cast *Glitterdust* as a Spell Like Ability.  Can you remember which one?  I cannot.   That's one reason I built this tool.  Put *Glitterdust* in the search field, and it will come back with 'mephit, salt'. 


A second reason I built this tool has to do with Feats and Templates.   A spell caster with a Good alignment summons creatures with the  Celestial template.  A spell caster with an Evil alignment summons creatures with the  Infernal template.  A Neutral spell caster has another choice between Celestial and Infernal.  Can you remember all the abilities the template provides?  I cannot.   The "Augment Summoning" feat adds still more benefits to summoned creatures, notably a +4 CON bonus, so +2hp/HD.   This tool can apply that bonus.  If you search first for 'eagle' you will get base stats.  Search for 'eagle "+augment summoning"  '  (or "eagle +a") and you will notice the Hit Points of the eagle have been modified by the Augment Summoning feat.


The reference to 4-1-1 is meant as a pun on Directory Assistance.



Description of use
------------------


1.  Edit the file ./bin/setup.sh 
     You want to set PROJECTDIR to the full path to summonmonsterfouroneone on your system
2.  cd $PROJECTDIR
3.  Source the file ./bin/setup.sh to set $PYTHONPATH environment variable.
4.  At a prompt, type
     python webserver.py
5.  You now have a web server running on port 8080 on your host.  Open a web client and point it at http://localhost:8080/    You will see a form that expects input, and a submit button.  Type the following word in the field:
     help
6.  Press submit.  You should see the help message, with more options to search.



Requirements
============


This application requires python 2.7 and two other libraries which are not standard on my python installation: web.py and lxml.   

web.py I installed from the web.py site.  sudo privileges to root were required to install it on my Linux system, but the installation was pretty simple.

    sudo -H pip install web.py
    
lxml was available through the Linux Ubuntu package installer synaptic. 

    sudo -H pip install lxml

Once I stop adding features, I intend to redo the application in python3.


I have tested this on UNIX (Ubuntu 12.04 and Ubuntu 16.04) hosts. If you are able to help improve this application for other operating systems, great, please do so.


Examples
========



Example of set up
-----------------

Source the file ./bin/setup.sh to set $PYTHONPATH environment variable.


    user@host: /path/to/summonmonsterfouroneone$ echo $PYTHONPATH
           
    user@host: /path/to/summonmonsterfouroneone$ . ./bin/setup.sh
    user@host: /path/to/summonmonsterfouroneone$ echo $PYTHONPATH
    :/path/to/summonmonsterfouroneone/sm411
    user@host: /path/to/summonmonsterfouroneone$ 
   


Example of use
--------------


In the following example I used a text mode web browser (lynx) to put 
     1 +x +a
into the search field, and hit submit.

The 1 is for the *Summon Monster I* spell.  The +a modifies the result with the "Augment Summoning" feat, increasing the hit points.  The +x shows the results in the extended display.




     Summon Monster Four One One TABLE OUTPUT
     
                   input: help, 0 to 9, 'dire wolf', blindSENSE, +a, +good
                   1 +x +a_______________________
                   (Submit a SumMon411 search!)
     _________________________________________________________________
     
     You submitted: [1 +x +a] You chose the extended display. 
     The Augment Summoning feat gives +4 to STR and +4 to CON for each summoned creature.
     
     Result set:

        Name        HD    hp SQ Size AL
     dog, riding    1d8+2 8     S    N
     eagle          1d8+1 7     S    N
     poisonous frog 1d8   6     T    N
     viper (snake)  1d8-1 5     T    N
     fire beetle    1d8   6     S    N
     rat, dire      1d8+1 7     S    N
     dolphin        2d8+2 15    M    N
     pony (horse)   2d8+4 17    M    N
     _________________________________________________________________


Example of testing
------------------

summonmonsterfouroneone makes use of Unit Tests.  All tests are in the  tests/ directory.

Calling tests/rt.py with python runs a regression test framework of all files in tests/ that start with test_ and in with .py

    user@host: /path/to/summonmonsterfouroneone$ python tests/rt.py 
    ..................................................
    ----------------------------------------------------------------------
    Ran 50 tests in 0.027s
    
    OK
    user@host: /path/to/summonmonsterfouroneone$
    


Design Notes
============

1.  XML is case sensitive.  Searching XML is case sensitive.  The monster names are in lower case to avoid using two xpath functions at once.   So are most other elements with text that would be searched.  The translate() xpath function is not used to convert XML content to lower case.  Instead, this application uses only the contains() xpath function to search partial term input provided by the user.   All input terms are converted to lower case to make searching easier.
2.  The online PRD differs from the PFRPG book.  The online PRD has been corrected (or so it seems to me), so where there are differences from the book, I go with the online PRD.
3.  Not all the monsters available to the Summon Monster spells are in the xml data file at present.  

Licence
=======


The files in the OGL directory provide Open Gaming Content that is licenced under the Open Gaming Licence.  See the file OGL/licence.txt for more information. 

The file /static/js/jquery-latest.js is Copyright 2010, John Resig and distributed under the GNU General Public Licence.

The file /static/js/jquery.tablesorter.js is Copyright (c) 2007 Christian Bach and distributed under the GNU General Public Licence.


This file is part of summonmonsterfouroneone.

summonmonsterfouroneone is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

summonmonsterfouroneone is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with summonmonsterfouroneone in the file COPYING.  
If not, see <http://www.gnu.org/licenses/>.



This application is not affiliated with Paizo.  


This application makes no claim to compatibility with the Pathfinder Role Playing Game made by Paizo.  




