import requests
import re


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
        addon_base_url = "http://www.curse.com/addons/wow/"
        self.url = addon_base_url + self.name + "/"
        self.download_url = self.url + "download/"

        # where to save the file
        # TODO: versioning? tmpfile?

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

    def getFile(self, target_file):
        """
        Download the file to a target dir
        
        Arguments:
        - `self`:
        """
        zipfile = self.matchZipFile()
        if zipfile:
            
            file_stream = requests.get(zipfile, stream = True)

            with open(target_file, 'wb') as f:
                for chunk in file_stream.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        else:
            # error
            print("Unable to find file for %s" % self.name)

    
            

