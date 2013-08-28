## addonsync ##
## syncronize wow addons from curse.com/wow based on URL ##
#!PROJECT!addonsync

import os
import sqlite3 as db
from addon import Addon
import json
import shutil
from platform import system


## TODO:

## - Time-delay to prevent curse.com from detecting automation and blocking
## - cache for downloads (prevent too much downloading).
## - threading (help with net and file io bottlenecks).
## - configfile/prompt for wow-addon folder?
## - Verbose output
## - More information stored in DB (number of installs, date installed, date of update...)
## - better looking output.
## - windows EXE (py2exe)
## - VERSION CHECKING FOR DIFFERENT LENGTH VERSIONS

## TESTING:
## - failure on invalid item name, bad url, no file, etc..


## CHANGEME - This value controls where your addons will be installed.
## For linux users, edit appropriately
addon_folder = "/home/curtis/.local/share/wineprefixes/wowtrial/drive_c/Program Files (x86)/World of Warcraft/Interface/AddOns/"

class Manager(object):
    """
    Handles the updating and installation of Addons.
    """
    
    def __init__(self, addons_dir=None):
        """
        """

        ## file locations
        s = system()

        if addons_dir:
            self.addons_dir = addons_dir
        elif s == 'Linux':
            self.addons_dir = addon_folder
        elif s == 'Windows':
            self.addons_dir = "C:\\Program Files (x86)\\World of Warcraft\\Interface\\AddOns\\"
        elif s == 'Darwin':
            print("Ur a fagit!")
            raise FagitExceptionError()

        if not os.path.isdir(self.addons_dir):
            raise AddonFolderNotFound("Addon directory not found!")

        ## connect to DB
        self.db = "/home/curtis/Code/Python/addonsync/addon.db"
        self.conn = db.connect(self.db)

    def installAddon(self, addon):
        """
        Download, and extract an addon into the addons folder.
        
        Arguments:
        - `self`:
        - `addon`: Addon or String
        """

        if isinstance(addon, str):
            addon = Addon(addon)

        # check if item is already in the DB
        with self.conn:
            in_db = self.conn.execute("SELECT name FROM addons WHERE name=?",\
                                      (addon.name, ))

            if not addon.installed and not in_db.fetchone():

                # add new
                if addon.getFile() and addon.unzipFile(self.addons_dir):
                    addon.newest_file = addon.updateAvailable()
                    with self.conn:
                        # print debugging
                        print("Adding record for %s." % addon.name)
                        print("Version -> %s" % addon.newest_file)
                        print("Files extracted -> %s" % json.dumps(addon.files))
                        self.conn.execute("INSERT INTO addons VALUES (?, ?, ?, ?)",\
                                          (addon.name, addon.newest_file, True, json.dumps(addon.files), ))

            else:
                #update... assume new version number and files only
                if addon.getFile() and addon.unzipFile(self.addons_dir):
                    addon.newest_file = addon.updateAvailable()
                    with self.conn:
                        # print debugging
                        print("Updating record for %s." % addon.name)
                        print("Version -> %s" % addon.newest_file)
                        print("Files extracted -> %s" % json.dumps(addon.files))
                        self.conn.execute("UPDATE addons SET version=?,files=?,downloaded=? WHERE name=?;",\
                                          (addon.newest_file, json.dumps(addon.files), True, addon.name, ))

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


    def uninstallAddon(self, addon):
        """
        Uninstall an Addon.

        TODO: better deletion. WE should be able to just index the "root" folder(s)
        for a given addon and shutil.rmtree those. No need to index every subfolder
        and file.
        
        Arguments:
        - `self`:
        - `addon`:
        """
        if isinstance(addon, str):
            addon = self.selectAddon(addon)
            
        if addon:
            # get user confirmation
            print("Uninstalling %s." % addon.name)            
            for p in addon.files:
                if os.path.isfile(p):
                    print("deleting %s" % p)
                    os.remove(p)
                elif os.path.isdir(p):
                    print("deleting %s" % p)
                    shutil.rmtree(p)
                else:
                    print("WARNING: Unable to remove %s" % p)
                    
            # assume files removed
            # TODO: keep record for statistical purposes.
            with self.conn:
                self.conn.execute("UPDATE addons SET downloaded=?,files=? WHERE name=?;",\
                                      (False, json.dumps([]), addon.name, ))


    

class AddonFolderNotFound(Exception):
    """
    """
    
    def __init__(self, value):
        """
        """
        self.value = value

    def __str__(self):
        return repr(self.value)

class FagitExceptionError(Exception):
    """
    """
    
    def __init__(self, value):
        """
        
        Arguments:
        - `value`:
        """
        self.value = value
        
    def __str__(self):
        return repr(self.value)
        

        
