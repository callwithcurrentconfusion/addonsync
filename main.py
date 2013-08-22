## addonsync ##
## syncronize wow addons from curse.com/wow based on URL ##

import urllib2
import lxml
from bs4 import BeautifulSoup
import sqlite3
import re

## TODO:
## add a new addon and auto-download/index (based on name)
## sqlitedb to keep track of updates and versions
## 

addons_dir = "/home/curtis/.local/share/wineprefixes/wowtrial/drive_c/Program Files (x86)/World of Warcraft/Interface/AddOns"

addon_template = "http://www.curse.com/addons/wow/"

addon_links = [
    "http://www.curse.com/addons/wow/omni-cc/download"
    "http://www.curse.com/addons/wow/tidy-plates/download"
    "http://www.curse.com/addons/wow/battlegroundtargets/download"
    "http://www.curse.com/addons/wow/quartz/download"
    "http://www.curse.com/addons/wow/reforgelite/download"
    "http://www.curse.com/addons/wow/gladius/download"
    "http://www.curse.com/addons/wow/tip-tac/download"
    "http://www.wowinterface.com/downloads/download21377-PlateBuff-Mop"]

addon_temp_dir = "/home/curtis/.addonsync"
temp_dir = "/tmp/"
addon_db = "/home/curtis/Code/Python/addonsync/addon.db"

## add tables to DB unless they already exists
conn = sqlite3.connect(addon_db)

## what we should do is parse the pages for the addons to get either
## their updated date, or their version number, and compare with our
## own records. if we have an addon that needs updating, download and
## extract to addons directory

class AddonPage(object):
    """
    """
    
    def __init__(self, URL):
        """
        
        Arguments:
        - `URL`: string or URL???
        """
        self._URL = URL


class Addon(BeautifulSoup):
    """ Represents an addon.
    """
    
    def __init__(self, name):
        """
        Arguments:
        - `name`: name of the addon
        """
        self.name = name
        self._url = urllib2.urlopen(addon_template + name)
        BeautifulSoup.__init__(self, self._url) # initialize parent class


    def downloadAddon(self):
        """ Download the addon zip.
        """
        download_url = addon_template + name + "/download"
        download_url = urllib2.urlopen(download_url)
        download_soup = BeautifulSoup(download_url)

        ## no guarentee this will work every time. should do a search for tags with data-href in them
        file_url = download_soup.p.a['data-href']
        target_file = addon_temp_dir + "/" + self.name

        ## download the file
        urllib2.urlretrieve(file_url, target_file)
        
        
    def addonVersion(self):
        """ Check the version of the addon
        """
        

    def indexAddon(self):
        """ update information about the addon in the db.
        """
        print "test"



## page = urllib2.urlopen("http://www.curse.com/addons/wow/omni-cc/")
soup = Addon("omni-cc")
## testpage = BeautifulSoup(open("/home/curtis/Code/Python/addonsync/resources/download"))


def findversion(soup):
    """
    """
    uls = soup.find_all('ul')
    for l in uls:
        for li in l.find_all("li"):
            if li['class'] == "details-list":
                li.string


    


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
# <p>If your download doesn't begin <a class="download-link" data-file="693805" data-href="http://addons.curse.cursecdn.com/files/693/805/OmniCC_5.2.3.zip" data-project="2057" href="#">click here</a>.</p>