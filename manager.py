## addonsync ##
## syncronize wow addons from curse.com/wow based on URL ##

import os
import sqlite3 as db
from addon import Addon
import json
import shutil

## TODO:

## - Time-delay to prevent curse.com from detecting automation and blocking
## - cache for downloads (prevent too much downloading).
## - threading (help with net and file io bottlenecks).
## - automatic tmpfile locations
## - configfile/prompt for wow-addon folder?
## - INSTALL/DELET ADDON BY NAME OR OBJECT
## - BETTER FILE INDEXING (ONLY INDEX ROOT FOLDERS THAT END UP AT THE TOP OF ADDONS FOLDER

## TESTING:
## - version / updating
## - failure on invalid item name, bad url, no file, etc..
## - nested files (addon packs).

## Target directory
# addons_dir = "/home/curtis/.local/share/wineprefixes/wowtrial/drive_c/Program Files (x86)/World of Warcraft/Interface/AddOns"


## Temporary hard-coded list of addons
## this will be later read from a config-file/DB
addon_links = [
    "http://www.curse.com/addons/wow/omni-cc/download"
    "http://www.curse.com/addons/wow/tidy-plates/download"
    "http://www.curse.com/addons/wow/battlegroundtargets/download"
    "http://www.curse.com/addons/wow/quartz/download"
    "http://www.curse.com/addons/wow/reforgelite/download"
    "http://www.curse.com/addons/wow/gladius/download"
    "http://www.curse.com/addons/wow/tip-tac/download"
    "http://www.wowinterface.com/downloads/download21377-PlateBuff-Mop"]

class Manager(object):
    """
    Handles the updating and installation of Addons.
    """
    
    def __init__(self, ):
        """
        """

        ## file locations
        ## TODO: argument pass this?
        self.addons_dir = "/home/curtis/Desktop/Addons/"
        self.temp_dir = "/tmp/addonsync/"

        for i in [self.addons_dir, self.temp_dir]:
            if not os.path.isdir(i):
                os.mkdir(i)
                

        ## connect to DB
        self.db = "/home/curtis/Code/Python/addonsync/addon.db"
        self.conn = db.connect(self.db)

    def installAddon(self, addon):
        """
        Download, and extract an addon into the addons folder.
        
        Arguments:
        - `self`:
        - `addon`:
        """

        if addon.installed:
            #update... assume new version number only
            with self.conn:
                # print debugging
                print("Updating record for %s." % addon.name)
                print("Version -> %s" % addon.newest_file)
                print("Files extracted -> %s" % json.dumps(addon.files))
                self.conn.execute("UPDATE addons SET version=?,files=? WHERE name=?;",\
                                  (addon.newest_file, json.dumps(addon.files), addon.name, ))
            
        else:
            # add new
            # TODO: better naming of tmp/zipfile (should end with .zip)
            tmpfile = self.temp_dir + addon.name + ".zip"
            if addon.getFile(tmpfile) and addon.unzipFile(self.addons_dir):
                addon.newest_file = addon.updateAvailable()
                with self.conn:
                    print("Adding record for %s." % addon.name)
                    print("Version -> %s" % addon.newest_file)
                    print("Files extracted -> %s" % json.dumps(addon.files))
                    self.conn.execute("INSERT INTO addons VALUES (?, ?, ?, ?)",\
                                      (addon.name, addon.newest_file, True, json.dumps(addon.files), ))


    def updateAddons(self):
        """
        For all the addons in the addon db, check their version number
        and download status, and install any addons that have updates available
        or have never been installed.
        
        Arguments:
        - `self`:
        """
         
        with self.conn:
            cur = self.conn.execute("SELECT * FROM addons;")
            for addon in cur:
                addon = Addon(*addon)

                # check to see if an update is available
                # if the addon isn't installed at all, we will
                # still use the version fetched by this function
                # to record.
                print("Checking for updates to %s" % addon.name)
                available_version = addon.updateAvailable()
                if available_version and addon.installed:
                    addon.newest_file = available_version
                    print("Upate available, installing %s." % addon.name)
                    self.installAddon(addon)
                    
                else:
                    print("%s is up to date." % addon.name)
                    

    def listInstalledAddons(self):
        """
        List all currently installed addons.
        
        Arguments:
        - `self`:
        """
        with self.conn:
            installed_addons = self.conn.execute("SELECT * FROM addons;")
            for addon in installed_addons:
                addon = Addon(*addon)
                print("%s - version: %s - installed: %s" % (addon.name, addon.newest_file, addon.installed))

    def selectAddon(self, name):
        """
        Lookup and return an addon from the db by name. 
        Arguments:
        - `self`:
        - `name`:
        """
        with self.conn:
            addon = self.conn.execute("SELECT * FROM addons WHERE name=?",\
                                      (name, ))
            if addon:
                
                return Addon(*addon.fetchone())
                
            else:
                print("Couldn't find an addon named %s." % name)
                return False


    def uninstallAddon(self, name):
        """
        Uninstall an Addon.

        TODO: better deletion. WE should be able to just index the "root" folder(s)
        for a given addon and shutil.rmtree those. No need to index every subfolder
        and file.
        
        Arguments:
        - `self`:
        - `addon`:
        """
        addon = self.selectAddon(name)
        if addon:
            # get user confirmation
            print("Uninstalling %s." % addon.name)            
            for p in addon.files:
                if os.path.isfile(p):
                    os.remove(p)
                elif os.path.isdir(p):
                    shutil.rmtree(p)
                else:
                    print("WARNING: Unable to remove %s" % p)
                    
            # assume files removed
            # TODO: keep record for statistical purposes.
            with self.conn:
                self.conn.execute("UPDATE addons SET downloaded=?,files=? WHERE name=?;",\
                                      (False, json.dumps([]), addon.name, ))

        

        
M = Manager()

    

        

        
