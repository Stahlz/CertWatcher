import subprocess
from .color import backgroundColor
import os
from .misc import redundant

"""I am the subprocess King"""
class certstreams():

    def __init__(self):
        pass

    global initcolor
    initcolor = backgroundColor()
    global initmisc
    initmisc = redundant()

    global FNULL
    FNULL = open(os.devnull, 'w')

    def cert_service_install(self):
        pwd = initmisc.get_pwd()
        """Gets the current user"""
        try:
            print(initcolor.OKBLUE + '[*] Grabbing Current User' + initcolor.ENDC)
            user_check = True
            get_user = initmisc.get_user()
        except:
            print(initcolor.WARNING + '[-] Could not get the current user' + initcolor.ENDC)
            user_check = False

        """Checks for crontab"""
        if get_user != None:
            look_for_crontab = subprocess.Popen(['ls', '/var/spool/cron/crontabs/{0}'.format(get_user)], shell=False, stdout=subprocess.PIPE, stderr=FNULL)
            look_for_crontab = look_for_crontab.stdout.read().decode('utf-8')
            if 'cannot access' in look_for_crontab:
                print(initcolor.WARNING + '[-] Crontab for user {0} Does not exist'.format(get_user) + initcolor.ENDC)
                print(initcolor.OKGREEN + '[*] Adding Crontab for user: ' + initcolor.WARNING + '{0}'.format(get_user) + initcolor.ENDC)
                try:
                    subprocess.Popen(['touch', '/var/spool/cron/crontabs/{0}'.format(get_user)], shell=False)
                except:
                    print(initcolor.WARNING + '[-] could not make a crontab for user: ' + initcolor.WARNING + '{0}'.format(get_user) + initcolor.ENDC)
            else:
                cat_cron = subprocess.Popen(['cat', '/var/spool/cron/crontabs/{0}'.format(get_user)],shell=False, stdout=subprocess.PIPE)
                cat_cron = cat_cron.stdout.read().decode('utf-8')
                if '{0}/certwatcher.py'.format(pwd) and 'emailer.py' not in cat_cron:
                    try:
                        """I hated having to do it this way"""
                        cert_restart_cron = 'echo "0 0 * * * cd {0}; python {0}/certwatcher.py -c restart" >> /var/spool/cron/crontabs/{1}'.format(pwd, get_user)
                        cert_email_cron = 'echo "0 0 * * * cd {0}; python {0}/lib/emailer.py" >> /var/spool/cron/crontabs/{1}'.format(pwd, get_user)
                        subprocess.Popen(cert_restart_cron, shell=True)
                        subprocess.Popen(cert_email_cron, shell=True)
                        print(initcolor.OKBLUE + '[*] Writing Restart and Email Cron Entries' + initcolor.ENDC)
                        cron_check = True
                    except Exception as R:
                        print(initcolor.WARNING + '[-] Problem installing Cron entries: ' + initcolor.WARNING + '{0}'.format(R) + initcolor.ENDC)
                        cron_check = False
                elif '{0}/certwatcher.py'.format(pwd) and 'emailer.py' in cat_cron:
                    print(initcolor.OKBLUE + '[*] Certstream Cron entry already there, moving along' + initcolor.ENDC)
                    cron_check = True
                elif ['{0}/certwatcher.py'.format(pwd) in cat_cron] and ['emailer.py' not in cat_cron]:
                    try:
                        cert_email_cron = 'echo "0 0 * * * cd {0}; python {0}/lib/emailer.py" >> /var/spool/cron/crontabs/{1}'.format(pwd, get_user) + '\n'
                        subprocess.Popen(cert_email_cron, shell=True)
                        cron_check = True
                        print(initcolor.OKBLUE + '[*] Writing Emailer cron entry' + initcolor.ENDC)
                    except Exception as R:
                        print(initcolor.WARNING + '[-] Problem installing Cron entries: ' + initcolor.WARNING + '{0}'.format(R) + initcolor.ENDC)
                        cron_check = False
                elif ['{0}/certwatcher.py'.format(pwd) not in cat_cron] and ['emailer.py' in cat_cron]:
                    try:
                        cert_restart_cron = 'echo "0 0 * * * cd {0}; python {0}/certwatcher.py -c restart" >> /var/spool/cron/crontabs/{1}'.format(pwd, get_user) + '\n'
                        subprocess.Popen(cert_restart_cron, shell=True)
                        cron_check = True
                        print(initcolor.OKBLUE + '[*] Writing Service Restart Cron entry' + initcolor.ENDC)
                    except Exception as R:
                        print(initcolor.WARNING + '[-] Problem installing Cron entries: {0}'.format(R) + initcolor.ENDC)
                        cron_check = False
                elif '{0}/certwatcher.py'.format(pwd) and 'emailer.py' in cat_cron:
                    print(initcolor.OKBLUE + '[*] Cron entries already present, skipping..' + initcolor.ENDC)
                    cron_check = True

        if user_check == False or cron_check == False:
            print(initcolor.FAIL + '[-] CertStream service Failed to install, Please check the error messages above' + initcolor.ENDC)
            return False
        else:
            print(initcolor.OKGREEN + '[*] CertStream service was successfully installed' + initcolor.ENDC)
            print(initcolor.OKGREEN + '[*] Start CertWatcher:' + initcolor.WARNING + ' python {0}/certwatcher.py -c start'.format(pwd) + initcolor.ENDC)
            return True

    """This is to uninstall the previous statement"""
    def cert_service_uninstall(self):
        try:
            get_user = initmisc.get_user()
            pwd = initmisc.get_pwd()
            user_check = True
            print(initcolor.OKBLUE + '[*] Grabbing Current User' + initcolor.ENDC)
        except Exception as uninstall_user:
            print(initcolor.WARNING + '[-] Couldnt Grab User: {0}'.format(uninstall_user) + initcolor.ENDC)
            user_check = False
        try:
            cat_cron = subprocess.Popen(['ls', '/var/spool/cron/crontabs/{0}'.format(get_user)], shell=False, stdout=subprocess.PIPE)
            cat_cron = cat_cron.stdout.read().decode('utf-8')
            cat_cron_check = True
            print(initcolor.OKBLUE + '[*] Checking for crontab availability' + initcolor.ENDC)
        except Exception as cat_cron_error:
            print(initcolor.WARNING + '[-] Couldnt Grab User: {0}'.format(cat_cron_error) + initcolor.ENDC)
            cat_cron_check = False

        if get_user and cat_cron != None:
            cron_file = '/var/spool/cron/crontabs/{0}'.format(get_user)
            with open(cron_file, 'r') as f:
                read_cron = f.read()
                print(initcolor.OKBLUE + '[*] Opening Cron File: {0}'.format(cron_file) + initcolor.ENDC)
                if '{0}/certwatcher.py'.format(pwd) and 'emailer.py' in read_cron:
                    f.close()
                    try:
                        with open(cron_file, 'w') as r:
                            read_cron = read_cron.replace('0 0 * * * cd {0}; python {0}/certwatcher.py -c restart'.format(pwd), '')
                            r.write(read_cron)
                            r.close()
                            print(initcolor.OKBLUE + '[*] Removing restart and emailer Cron objects from: {0}'.format(cron_file) + initcolor.ENDC)
                        with open(cron_file, 'w') as s:
                            replace_cron = read_cron.replace('0 0 * * * cd {0}; python {0}/lib/emailer.py'.format(pwd), '')
                            s.write(replace_cron)
                            s.close()
                            replace_cron = True
                    except Exception as cronz:
                        print(initcolor.WARNING + '[-] Could not remove cron Entries: {0}'.format(cronz) + initcolor.ENDC)
                        replace_cron = False
                elif ['{0}/certwatcher.py'.format(pwd) in read_cron] and ['emailer.py' not in read_cron]:
                    try:
                        with open(cron_file, 'w') as r:
                            read_cron = read_cron.replace('0 0 * * * cd {0}; python {0}/certwatcher.py -c restart'.format(pwd), '')
                            r.write(read_cron)
                            r.close()
                            print(initcolor.OKBLUE + '[*] Removing Restart Cron object from: {0}'.format(cron_file) + initcolor.ENDC)
                            replace_cron = True
                    except Exception as cronz:
                        print(initcolor.OKBLUE + '[-] Could not remove cron Entry: {0}'.format(cronz) + initcolor.ENDC)
                        replace_cron = False
                elif ['{0}/certwatcher.py'.format(pwd) not in read_cron] and ['emailer.py' in read_cron]:
                    try:
                        with open(cron_file, 'w') as r:
                            read_cron = read_cron.replace('0 0 * * * cd {0}; python {0}/lib/emailer.py'.format(pwd), '')
                            r.write(read_cron)
                            r.close()
                            print(initcolor.OKBLUE + '[*] Removing Emailer Cron object from: {0}'.format(cron_file) + initcolor.ENDC)
                            replace_cron = True
                    except Exception as cronz:
                        print(initcolor.WARNING + '[-] Could not remove cron Entries: {0}'.format(cronz) + initcolor.ENDC)
                        replace_cron = False
                elif '{0}/certwatcher.py'.format(pwd) and 'emailer.py' not in read_cron:
                    f.close()
                    print(initcolor.OKGREEN + '[*] Neither Cron entry present, moving along: {0}'.format(cron_file) + initcolor.ENDC)
                    replace_cron = True

        if user_check == False or cat_cron_check == False or replace_cron == False:
            print(initcolor.FAIL + '[-] Service Failed to uninstall, Please check the error messages above' + initcolor.ENDC)
            return False1
        else:
            print(initcolor.OKGREEN + '[*] Service was successfully uninstalled' + initcolor.ENDC)
            return True

    def cert_service_start(self):
        try:
            pwd = initmisc.get_pwd()
            date = initmisc.get_date()
            to_email = initmisc.get_email()
            pid = initmisc.get_pid().strip()
            psef = initmisc.get_ps().strip()
            if 'No such file' in pid:
                print(initcolor.WARNING + '[*] Service not running' + initcolor.ENDC)
                """Starting Agent.py"""
                initmisc.start_agent()
                psef = initmisc.get_ps()
                print(initcolor.WARNING + '[*] Adding pid File to /var/run/certwatcher.pid' + initcolor.ENDC)
                with open('/var/run/certwatcher.pid', 'w') as pidder:
                    pidder.write(psef)
                    pidder.close()
                pid = initmisc.get_pid()
                print(initcolor.OKGREEN + '[*] Started Service, PID: ' + initcolor.WARNING + '{0}'.format(pid) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] You can check for sites here: ' + initcolor.FAIL + '{0}/output/{1}.log'.format(pwd, date) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] Everyday you will get an email report to: ' + initcolor.FAIL +'{0}'.format(to_email) + initcolor.ENDC)
                print(initcolor.WARNING + '[*] Exiting' + initcolor.ENDC)
            elif pid == 'empty':
                print(initcolor.WARNING + '[*] Service not running' + initcolor.ENDC)
                """Starting Agent.py"""
                initmisc.start_agent()
                psef = initmisc.get_ps()
                print(initcolor.WARNING + '[*] Adding pid File to /var/run/certwatcher.pid' + initcolor.ENDC)
                with open('/var/run/certwatcher.pid', 'w') as pidder:
                    pidder.write(psef)
                    pidder.close()
                pid = initmisc.get_pid()
                print(initcolor.OKGREEN + '[*] Started Service, PID: ' + initcolor.WARNING + '{0}'.format(pid) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] You can check for sites here: ' + initcolor.FAIL + '{0}/output/{1}.log'.format(pwd, date) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] Everyday you will get an email report to: ' + initcolor.FAIL +'{0}'.format(to_email) + initcolor.ENDC)
                print(initcolor.WARNING + '[*] Exiting' + initcolor.ENDC)
            elif pid == '':
                psef = initmisc.get_ps().strip()
                if psef == '':
                    print(initcolor.WARNING + '[*] Service not running' + initcolor.ENDC)
                    """Starting Agent.py"""
                    initmisc.start_agent()
                    psef = initmisc.get_ps()
                    print(initcolor.WARNING + '[*] Adding pid File to /var/run/certwatcher.pid' + initcolor.ENDC)
                    with open('/var/run/certwatcher.pid', 'w') as pidder:
                        pidder.write(psef)
                        pidder.close()
                    pid = initmisc.get_pid()
                    print(initcolor.OKGREEN + '[*] Started Service, PID: ' + initcolor.WARNING + '{0}'.format(pid) + initcolor.ENDC)
                    print(initcolor.OKBLUE + '[*] You can check for sites here: ' + initcolor.FAIL + '{0}/output/{1}.log'.format(pwd, date) + initcolor.ENDC)
                    print(initcolor.OKBLUE + '[*] Everyday you will get an email report to: ' + initcolor.FAIL + '{0}'.format(to_email) + initcolor.ENDC)
                    print(initcolor.WARNING + '[*] Exiting' + initcolor.ENDC)
            elif pid != '' or psef != '':
                if pid != '':
                    print(initcolor.OKGREEN + '[*] Service already started Service, PID: ' + initcolor.WARNING + '{0}'.format(pid) + initcolor.ENDC)
                elif psef != '':
                    print(initcolor.OKGREEN + '[*] Service already started Service, PID: ' + initcolor.WARNING + '{0}'.format(psef) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] You can check for sites here: ' + initcolor.FAIL + '{0}/output/{1}.log'.format(pwd, date) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] Everyday you will get an email report to: ' + initcolor.FAIL + '{0}'.format(to_email) + initcolor.ENDC)
                print(initcolor.WARNING + '[*] Exiting' + initcolor.ENDC)
            else:
                print(initcolor.FAIL + '[-] Could not find process pid' + initcolor.ENDC)
        except Exception as R:
            print(initcolor.FAIL + '[-] Failed to Start CertWatcher: ' + initcolor.WARNING + '{0}'.format(R) + initcolor.ENDC)

    def cert_service_stop(self):
        try:
            cat_pid = initmisc.get_pid().strip()
            psef = initmisc.get_ps().strip()
            psef = psef.strip('\n')
            if cat_pid != 'empty':
                print(initcolor.OKBLUE + 'Found CertWatcher PID: ' + initcolor.WARNING + '{0}'.format(cat_pid) + initcolor.ENDC)
                print(initcolor.OKBLUE + 'Stopping CertWatcher' + initcolor.ENDC)
                subprocess.Popen(['kill {0}'.format(cat_pid)], shell=True, stdout=FNULL, stderr=FNULL)
                subprocess.Popen(['echo "empty" > /var/run/certwatcher.pid'], shell=True, stdout=FNULL, stderr=FNULL)
            elif psef != '' or None:
                print(initcolor.OKBLUE + 'Found CertWatcher PID: ' + initcolor.WARNING + '{0}'.format(psef) + initcolor.ENDC)
                print(initcolor.OKBLUE + 'Stopping CertWatcher' + initcolor.ENDC)
                subprocess.Popen(['kill {0}'.format(psef)], shell=True, stdout=FNULL, stderr=FNULL)
                subprocess.Popen(['echo "empty" > /var/run/certwatcher.pid'], shell=True, stdout=FNULL, stderr=FNULL)
            elif cat_pid == 'empty':
                print(initcolor.OKBLUE + 'CertWatcher is already stopped' + initcolor.ENDC)
        except Exception as R:
            print(initcolor.FAIL + '[-] Failed to stop CertStream Service: ' + initcolor.WARNING + '{0}'.format(R) + initcolor.ENDC)

    def cert_service_restart(self):
        try:
            cat_pid = initmisc.get_pid()
            psef = initmisc.get_ps().strip()
            to_email = initmisc.get_email()
            pwd = initmisc.get_pwd().strip()
            date = initmisc.get_date()
            """Checks certwatcher.pid for process id"""
            if cat_pid != '':
                print(initcolor.OKBLUE + 'Found CertWatcher PID: ' + initcolor.WARNING + '{0}'.format(cat_pid) + initcolor.ENDC)
                print(initcolor.OKBLUE + 'Stopping CertWatcher' + initcolor.ENDC)
                subprocess.Popen(['kill {0}'.format(cat_pid)], shell=True, stdout=FNULL, stderr=FNULL)
                print(initcolor.OKBLUE + 'Starting CertWatcher' + initcolor.ENDC)
                initmisc.start_agent()
                psef = initmisc.get_ps().strip()
                with open('/var/run/certwatcher.pid', 'w') as pidder:
                    pidder.write(psef)
                    pidder.close()
                pid = initmisc.get_pid().strip()
                print(initcolor.OKGREEN + '[*] Started Service, PID: ' + initcolor.WARNING + '{0}'.format(pid) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] You can check for sites here: ' + initcolor.FAIL + '{0}/output/{1}.log'.format(pwd, date) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] Everyday you will get an email report to: ' + initcolor.FAIL + '{0}'.format(to_email) + initcolor.ENDC)
                print(initcolor.WARNING + '[*] Exiting' + initcolor.ENDC)
            elif psef != '':
                print(initcolor.OKBLUE + 'Found CertWatcher PID: ' + initcolor.WARNING + '{0}'.format(psef) + initcolor.ENDC)
                print(initcolor.OKBLUE + 'Stopping CertWatcher' + initcolor.ENDC)
                subprocess.Popen(['kill {0}'.format(psef)], shell=True, stdout=FNULL, stderr=FNULL)
                print(initcolor.OKBLUE + 'Starting CertWatcher' + initcolor.ENDC)
                initmisc.start_agent()
                psef = initmisc.get_ps().strip()
                with open('/var/run/certwatcher.pid', 'w') as pidder:
                    pidder.write(psef)
                    pidder.close()
                pid = initmisc.get_pid().strip()
                print(initcolor.OKGREEN + '[*] Started Service, PID: ' + initcolor.WARNING + '{0}'.format(pid) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] You can check for sites here: ' + initcolor.FAIL + '{0}/output/{1}.log'.format(pwd, date) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] Everyday you will get an email report to: ' + initcolor.FAIL + '{0}'.format(to_email) + initcolor.ENDC)
                print(initcolor.WARNING + '[*] Exiting' + initcolor.ENDC)
            elif cat_pid == '' and psef == '':
                print(initcolor.OKBLUE + 'CertWatcher was not running, it will be started' + initcolor.ENDC)
                initmisc.start_agent()
                psef = initmisc.get_ps().strip()
                with open('/var/run/certwatcher.pid', 'w') as pidder:
                    pidder.write(psef)
                    pidder.close()
                pid = initmisc.get_pid().strip()
                print(initcolor.OKGREEN + '[*] Started Service, PID: ' + initcolor.WARNING + '{0}'.format(pid) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] You can check for sites here: ' + initcolor.FAIL + '{0}/output/{1}.log'.format(pwd, date) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] Everyday you will get an email report to: ' + initcolor.FAIL + '{0}'.format(to_email) + initcolor.ENDC)
                print(initcolor.WARNING + '[*] Exiting' + initcolor.ENDC)
            else:
                print(initcolor.OKBLUE + 'CertWatcher was not running, it will be started' + initcolor.ENDC)
                initmisc.start_agent()
                psef = initmisc.get_ps()
                with open('/var/run/certwatcher.pid', 'w') as pidder:
                    pidder.write(psef)
                    pidder.close()
                pid = initmisc.get_pid().strip()
                print(initcolor.OKGREEN + '[*] Started Service, PID: ' + initcolor.WARNING + '{0}'.format(pid) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] You can check for sites here: ' + initcolor.FAIL + '{0}/output/{1}.log'.format(pwd, date) + initcolor.ENDC)
                print(initcolor.OKBLUE + '[*] Everyday you will get an email report to: ' + initcolor.FAIL + '{0}'.format(to_email) + initcolor.ENDC)
                print(initcolor.WARNING + '[*] Exiting' + initcolor.ENDC)
        except Exception as Restart_error:
            print(initcolor.FAIL + '[-] Could not restart CertWatcher' + initcolor.WARNING + '{0}'.format(Restart_error) + initcolor.ENDC)
