from lib.art import ascii
from lib.certstreamz import certstreams
from lib.color import backgroundColor
from lib.misc import redundant
import argparse
import sys

"""Initing Section"""
initart = ascii()
initcert = certstreams()
initcolor = backgroundColor()
initmisc = redundant()

"""Get Working Directory"""
pwd = initmisc.get_pwd()

"""Email Config Checker"""
check_email_configs = initmisc.check_email()
if check_email_configs == False:
    print(initcolor.FAIL + '[-] Please fill out the email section of the: {0}/config.txt'.format(pwd) + initcolor.ENDC)
    sys.exit()

"""Check Agent Config"""
check_agent_configs = initmisc.check_certstreamer()
if check_agent_configs == False:
    print(initcolor.FAIL + '[-] Please fill out the certstreamer section of the: {0}/config.txt'.format(pwd) + initcolor.ENDC)
    print(initcolor.FAIL + '[-] Seperate the keywords with commas'.format(pwd) + initcolor.ENDC)
    sys.exit()

"""Printing Ascii Art"""
print(initart.opening_ascii_art())

"""ArgParse Segment for adding Arguments"""
parser = argparse.ArgumentParser()
parser.add_argument('-c','--certstream', dest='cert_init', choices=['start', 'stop', 'restart', 'install', 'uninstall'], help='Please Select one')
args = parser.parse_args()

if args.cert_init == 'start':
    print(initcolor.OKGREEN + '[*] Attempting to start CertWatcher service' + initcolor.ENDC)
    initcert.cert_service_start()
elif args.cert_init == 'stop':
    print(initcolor.OKGREEN + '[*] Attempting to stop CertWatcher service' + initcolor.ENDC)
    initcert.cert_service_stop()
elif args.cert_init == 'restart':
    print(initcolor.OKGREEN + '[*] Trying to restart CertWatcher service' + initcolor.ENDC)
    initcert.cert_service_restart()
elif args.cert_init == 'install':
    print(initcolor.OKGREEN + '[*] Attempting to uninstall CertWatcher service' + initcolor.ENDC)
    initcert.cert_service_install()
elif args.cert_init == 'uninstall':
    print(initcolor.OKGREEN + '[*] Attempting to install CertWatcher service' + initcolor.ENDC)
    initcert.cert_service_uninstall()
else:
    print(initcolor.FAIL + '[-] You must give a valid choice' + initcolor.ENDC)
