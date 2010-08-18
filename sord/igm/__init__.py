from . import dht

""" Notes on IGM's:

* All IGM module files should be listed in the above import.
* To install a new IGM, add another tuple to the list of tuples in igmlist

  ex:  igmlist = list( ( 'KEY COMMAND', igm_module.igm_main_class() , 'DISPLAY NAME' ) )
  
* IGM Module files *may* include more than one IGM class, list them seperatly.
* IGM Module classes *must* have a run(<sordUser object>) method, used to initiate the IGM
* IGM Module classes *may* have an __init__() method
  !! but it is called too early in processing to do anything other that basic setup !!

NOTE: See dht.py for an example of a working IGM (has access to basic display functions, 
      basic user info display functions, and the full user object.
      
WARNING: The IGMs are loaded with the server, and do nothing (unavoidable in order to enumerate them)
         However, they are also loaded for each connected user again.  As you might imagine, if an
         IGM uses a lot of memory, or you have a ton of IGMS, this can be a performance hit.  Natrually,
         with modern systems, this isn't quite the problem it was in the days of LORD and a BBS running 
         on a 386, but it is certainly something to be aware of.
"""
igmlist = [('D', dht.dht(), "Dark Horse Tavern")]

