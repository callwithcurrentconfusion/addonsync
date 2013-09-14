#!/usr/bin/env python

from manager import Manager
import argparse

command_help_text = "[list|info|install|uninstall|update]"

addon_folder = "/home/curtis/Desktop/Addons/"

# Our manager
M = Manager()

# Argument parsing
parser = argparse.ArgumentParser(description="Manage your WoW addons with ease!")

def info(args):
    """

    Arguments:
    - `name`:
    """
    addon = M.selectAddon(args.name)
    print("Name -> %s." % addon.name)
    print("Version -> %s" % addon.newest_file)
    print("Installed -> %s" % addon.installed)
    # print("Files extracted -> %s" % json.dumps(addon.files))

def install(args):
    """

    Arguments:
    - `name`:
    """
    M.installAddon(args.name)

def uninstall(args):
    """

    Arguments:
    - `name`:
    """
    M.uninstallAddon(args.name)

def list():
    """

    Arguments:
    - `name`:
    """
    M.listInstalledAddons()

def update():
    """
    """
    M.updateAddons()


subparsers = parser.add_subparsers()

# info
parser_info = subparsers.add_parser("info", help="List info for a specific addon.")
parser_info.add_argument("name", help="Addon name")
parser_info.set_defaults(func=info)


# install
parser_install = subparsers.add_parser("install", help="Install an addon.")
parser_install.add_argument("name", help="Addon name")
parser_install.set_defaults(func=install)

# uninstall
parser_uninstall = subparsers.add_parser("uninstall", help="Uninstall an addon.")
parser_uninstall.add_argument("name", help="Addon name")
parser_uninstall.set_defaults(func=uninstall)

#list
parser_list = subparsers.add_parser("list", help="list all addons in db.")
parser_list.set_defaults(func=list)

# update
parser_update = subparsers.add_parser("update", help="Attempt to update all installed addons.")
parser_update.set_defaults(func=update)

# run


    
        
if __name__ == "__main__":
    args = parser.parse_args()

    if "name" in args:
        args.func(args)
    else:
        args.func()
