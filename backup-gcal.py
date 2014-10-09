#!/usr/bin/python

import sys
import os
import datetime
import shutil
import argparse
import mechanize
import magic
import getpass

__version__ = '1.0'
__author__ = "samyboy"


def download_icalzip(email, password, destination):
    """Download all the calendars in a zip format.
    Returns True if succeded, false if failed
    """

    login_url = 'https://www.google.com/calendar/'
    icalzip_url = 'https://www.google.com/calendar/exporticalzip'
    timeout = 10.0

    """Download the file"""
    br = mechanize.Browser()
    br.open(login_url, timeout=timeout)
    g = br.select_form(nr=0)
    br['Email'] = email
    br['Passwd'] = password
    br.submit()
    h = br.retrieve(icalzip_url)
    source = h[0]

    if not os.path.exists(source):
        return False

    # determine file type
    m = magic.open(magic.MAGIC_MIME)
    m.load()
    filetype = m.file(source)

    if filetype is None:
        return False

    if filetype.startswith('application/zip'):
        """ the file looks like a zip file:
        we are moving it to the wanted location
        """
        shutil.copyfile(source, destination)
        os.remove(source)
        return True

    """Things did not work as expected..."""
    os.remove(source)
    return False


def parse_arguments():

    global __author__
    global __version__

    version_string = "%(prog)s-%(version)s by %(author)s" % \
                     {"prog": "%(prog)s", "version": __version__, \
                     "author": __author__}

    p = argparse.ArgumentParser(description="Description",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    p.add_argument('-V', '--version', action='version',
                   help="shows program version", version=version_string)
    p.add_argument('account',
                   help='your google account')
    p.add_argument('-p', '--password',
                   help='password')
    p.add_argument('-d', '--directory', default=os.getcwd(),
                   help='Output directory')

    return p.parse_args()


def main():

    args = parse_arguments()

    if args.password is None:
        sys.stderr.write("Please type your password for account \"%s\"\n" % \
                         args.account)
        password = getpass.getpass()
    else:
        password = args.password

    """determine the new destination"""
    now = datetime.datetime.now()
    dateformat = now.strftime("%Y%m%d-%H%M")
    destination = args.directory + "/gcal-" + args.account + "-" + \
                  dateformat + ".zip"

    """download the file and get the filename"""
    result = download_icalzip(args.account, password, destination)

    if not result:
        sys.stderr.write("Failed to download calendar for account \"%s\"\n" % \
                         args.account)
        sys.exit(1)

    """Missions acomplished."""
    print destination
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("Program exited by user")
        sys.exit(1)
