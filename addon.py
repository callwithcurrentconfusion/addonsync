import requests
import re
import zipfile
import json
import tempfile

def prompt_for_update(message):
    """
    
    Arguments:
    - `message`: (String) notice to paste to user.
    """

    while True:
        s = raw_input(message).upper()
        if s == "Y" or s == "YES":
            return True
        elif s == "N" or s == "NO":
            return False
        else:
            print("Please enter (y)es or (n)o.")


def find_on_page(url, ms):
    """
    Return of list of FIRST matches of match_string found
    in the next of a webpage.

    If none are found, return False.
    
    Arguments:
    - `url`: (String) the URL of the addon page
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
    Returns a boolean value.
    
    - `available_version`: (String) 
    - `current_version`: (String)
    """

    # if we have a valid available_version, but no current_version
    # return True
    if available_version and not current_version:
        return True

    # if the versions are identical, return false
    if available_version == current_version:
        return False

    # if the versions aren't exactly the same, try and compare them
    try:
        print("Comparing installed verion %s and available version %s"\
              % (current_version, available_version))
        
        # some version will not use a dot convention.
        available_modes = available_version.split(".")
        current_modes = current_version.split(".")

        # compare each revision:
        # version 6.4.0 -> [6,4,0] against
        # vession 6.3.1 -> [6,3,1]
        # -> 6/6 -> 4/3 -> TRUE
        for (x,y) in zip(available_modes, current_modes):

            if x > y:
                return True
            elif y > x:
                return False
            elif len[x] > len[y]:
                return True
                
        return False
        
    except:
        print("WARNING: Unable to compare versions automatically.")
        return prompt_for_update("Manually update? y\n:> ")
    


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

    def getNewestVersion(self):
        """
        Return the newest file version, if possible.
        Return False if not.
    
        Arguments:
        - `self`:
        """
        
        print("Checking for updates to %s" % self.name)
        
        ms = "Newest File: ([0-9\.]+)"
        available_version = find_on_page(self.url, ms)

        if available_version:
            return available_version
        else:
            return False
        
        
    def updateAvailable(self):
        """
        Check for an update. Return the version number of
        the latest file if it is greater than our current number.

        Return false if there is no newer version available, or we
        fail to get a version for this addon.

        TODO: better logic for comparing versions.

        Arguments:
        - `self`:
        """

        available_version = self.getNewestVersion()
      
        if available_version:
            if newer_version(available_version, self.newest_file):
                print("Current available version of %s: %s." % (self.name, available_version))
                print("Update available!")
                return available_version
            else:
                return False
    
        else:
            # if we're unable to parse for a version, prompt for manual imput
            print("Unable to find newest file listed for %s" % self.name)
            response = prompt_for_update("Update? y/n:> ")
            return response


    def getFile(self):
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
            
            print("Downloading %s" % z)
            try:
                target_file = tempfile.NamedTemporaryFile(delete=False)
                for chunk in file_stream.iter_content(chunk_size = 1024):
                    if chunk:
                        target_file.write(chunk)
                        target_file.flush()
                target_file.close()
            except:
                print("Error downloading file to tempfile.")
                self.zipfile = None
                return False

            # objectify our file.
            #self.zipfile = zipfile.ZipFile(target_file)
            self.zipfile = target_file

            return True
            
        else:
            # error
            print("Unable to find file for %s" % self.name)
            return False
            

    def unzipFile(self, target_dir):
        """
        Extract the contents of our zipfile into the target directory.

        Arguments:
        - `self`:
        """
        zf = zipfile.ZipFile(self.zipfile.name)
        if not zf:
            print("No zipfile!!!!")
            return False

        # TODO: try/except here, validation of file contents
        #  to prevent traversal exploits
        for name in zf.namelist():
            self.files.append(target_dir + name)

        print("Extracting zipfile to %s." % target_dir)
        zf.extractall(target_dir)

        # clean up the tmp file.
        print("Cleaning up tmpfile.")
        zf.close()
        
        return True


