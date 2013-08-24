import requests
import re
import zipfile
import json

def find_on_page(url, ms):
    """
    Return of list of FIRST matches of match_string found
    in the next of a webpage.

    If none are found, return False.
    
    Arguments:
    - `url`:
    """
    
    # ms = "http://addons\.curse\.cursecdn\.com/files/.*\.zip"
    page = requests.get(url)

    fa = re.findall(ms, page.text)
    if fa:
        return fa[0]
    else:
        return False

def newer_version(available_version, current_version):
    """
    Compare two version, keeping in mind the current version might be None.
    Arguments:
    - `available_version`:
    - `current_version`:
    """

    # if we have a valid available_version, but no current_version
    # return True
    if available_version and not current_version:
        return True
    elif available_version > current_version:
        return True
    else:
        return False
    


class Addon(object):
    """
    """
    
    def __init__(self, name, newest_file=None, installed=False, files="[]"):
        """
        
        Arguments:
        - `name`:
        """
        self.name = name
        self.newest_file = newest_file
        self.installed = installed
        self.files = json.loads(files)

        # the addon has a 'homepage' as well as a download page
        addon_base_url = "http://www.curse.com/addons/wow/"
        self.url = addon_base_url + self.name + "/"
        self.download_url = self.url + "download/"

        self.zipfile = None
        
        
    def updateAvailable(self):
        """
        Check for an update. Return the version number of
        the latest file if it is greater than our current number.

        Return false if there is no newer version available, or we
        fail to get a version for this addon.

        Arguments:
        - `self`:
        """
        ms = "Newest File: ([0-9\.]+)"
        available_version = find_on_page(self.url, ms)

        if available_version:
            if newer_version(available_version, self.newest_file):
                print(available_version)
                return available_version
            else:
                return False
                                
        else:
            print("Unable to find newest file listed for %s" % self.name)
            return False


    def getFile(self, target_file):
        """
        Parse a webpage looking for a zipfile for an addon.
        If a file is found, download it. Else Fail.
        
        Arguments:
        - `self`:
        """
        ms = "http://addons\.curse\.cursecdn\.com/files/.*\.zip"
        z = find_on_page(self.download_url, ms)
        if z:
            
            file_stream = requests.get(z, stream = True)

            with open(target_file, 'wb') as f:
                for chunk in file_stream.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

            # objectify our file.
            self.zipfile = zipfile.ZipFile(target_file)

            return True
            
        else:
            # error
            print("Unable to find file for %s" % self.name)
            return False
            

    def unzipFile(self, target_dir):
        """
        Extract the contents of our zipfile into the target directory.
        TODO: for each file we extract, add it + path to self.files
        Arguments:
        - `self`:
        """

        if not self.zipfile:
            print("No zipfile!!!!")
            return False

        # TODO: try/except here, validation of file contents
        #  to prevent traversal exploits
        self.zipfile.extractall(target_dir)
        return True

    

quartz = Addon("quartz")    