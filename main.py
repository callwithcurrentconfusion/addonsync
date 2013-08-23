## addonsync ##
## syncronize wow addons from curse.com/wow based on URL ##

import os
import requests
import sqlite3
import re

## TODO:
## add a new addon and auto-download/index (based on name)
## sqlitedb to keep track of updates and versions

## - Wrapper for ensuring directory creation if necessary ??
## - Time-delay to prevent curse.com from detecting automation and blocking

## Target directory
# addons_dir = "/home/curtis/.local/share/wineprefixes/wowtrial/drive_c/Program Files (x86)/World of Warcraft/Interface/AddOns"
addons_dir = "/home/curtis/Desktop/Addons/"

## base url where addons are found
addon_base_url = "http://www.curse.com/addons/wow/"

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

## Temporary location to save addons into
## TODO: Why?
addon_temp_dir = "/home/curtis/.addonsync"
temp_dir = "/tmp/"

## Database for tracking updates and changes
addon_db = "/home/curtis/Code/Python/addonsync/addon.db"

## add tables to DB unless they already exists
# conn = sqlite3.connect(addon_db)

## what we should do is parse the pages for the addons to get either
## their updated date, or their version number, and compare with our
## own records. if we have an addon that needs updating, download and
## extract to addons directory

class Addon(object):
    """
    """
    
    def __init__(self, name):
        """
        
        Arguments:
        - `name`:
        """
        self.name = name

        # the addon has a 'homepage' as well as a download page
        self.url = addon_base_url + self.name + "/"
        self.download_url = self.url + "download/"

        # where to save the file
        # TODO: versioning? tmpfile?
        self.zip_file = addons_dir + self.name

    def matchVersion(self):
        """
        Figure out current version of an addon.

        Arguments:
        - `self`:
        """
        True

    def matchZipFile(self):
        """
        Parse a webpage looking for a zipfile for an addon.
        
        Return the URL if a file is found, or False if not.

        Arguments:
        - `self`: 
        """

        ms = "http://addons\.curse\.cursecdn\.com/files/.*\.zip"
        page = requests.get(self.download_url)

        fa = re.findall(ms, page.text)
        if fa:
            return fa[0]
        else:
            return False

    def getFile(self):
        """
        Download the file to a target dir
        
        Arguments:
        - `self`:
        """
        zipfile = self.matchZipFile()
        if zipfile:
            
            file_stream = requests.get(zipfile, stream = True)

            with open(self.zip_file, 'wb') as f:
                for chunk in file_stream.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        else:
            # error
            print("Unable to find file for %s" % self.name)

    
            



# ## NOTES ##

# ## Version Number ##
# <ul class="details-list">
# <li class="game"><a href="/addons/wow">World of Warcraft</a></li>
# <li class="average-downloads">333,533 Monthly Downloads</li>
# <li class="version version-up-to-date">Supports: 5.2.0</li>
# <li class="downloads">12,297,036 Total Downloads</li>
# <li class="updated">Updated <abbr class="standard-date" data-epoch="1365805546" title="Fri, 12 Apr 2013 17:25:46 CDT (UTC-5:00)">04/12/2013</abbr></li>
# <li class="updated">Created <abbr class="standard-date" data-epoch="1144961161" title="Thu, 13 Apr 2006 15:46:01 CDT (UTC-5:00)">04/13/2006</abbr></li>
# <li class="favorited">16,737 Favorites</li>
# <li class="curseforge"><a href="http://www.curseforge.com/projects/2057/">Project Site</a></li>
# <li class="comments"><a href="#comments">Comments</a></li>
# <li class="release">Release Type: Release</li>
# <li class="license">License: All Rights Reserved </li>
# <li class="newest-file">Newest File: 5.2.3</li>
# </ul>

# ## DOWNLOAD LINK
# <div class="download-options">
# <ul class="regular-dl ">
# <li><em class="cta-button download-large"><a href="/addons/wow/omni-cc/download">Download Now</a></em></li>
# <li><em class="cta-button download-cc-large"><a href="/addons/wow/omni-cc/693805-client">Install via Curse Client</a></em></li>
# </ul>
# <div class="premium-upsell">
# <em><span>or</span></em>
# <ul class="premium-dl premium-info">
# <li>Download at premium <em>fast</em> speed <a href="/premium">Learn More</a></li>
# </ul>
# </div>

# ## DOWNLOAD
file_string = ' <p>If your download doesnt begin <a class="download-link" data-file="693805" data-href="http://addons.curse.cursecdn.com/files/693/805/OmniCC_5.2.3.zip" data-project="2057" href="#">click here</a>.</p>'


