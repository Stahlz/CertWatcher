import subprocess
import datetime
import configparser
import os

class redundant():

    global FNULL
    FNULL = open(os.devnull, 'w')

    """Initing the color class"""
    def __init__(self):
        pass

    def get_user(self):
        get_user = subprocess.Popen(['whoami'], shell=False, stdout=subprocess.PIPE)
        get_user = get_user.stdout.read().decode('utf-8')
        get_user = get_user.strip('\n')
        return get_user


    def get_pwd(self):
        get_pwd = subprocess.Popen(['pwd'], shell=True, stdout=subprocess.PIPE)
        get_pwd = get_pwd.stdout.read().decode('utf-8').strip('\n')
        get_pwd = get_pwd.strip('\lib')
        return get_pwd

    def get_date(self):
        current = datetime.datetime.now()
        date = current.date()
        return date

    def check_email(self):
        pwd = subprocess.Popen(['pwd'], shell=True, stdout=subprocess.PIPE)
        pwd = pwd.stdout.read().decode('utf-8').strip('\n')
        pwd = pwd.strip('lib')
        configfilepath = '{0}/config.txt'.format(pwd)
        config = configparser.ConfigParser()
        config.read(configfilepath)

        from_email = config.get('email', 'from_email')
        to_email = config.get('email', 'to_email')
        email_user = config.get('email', 'email_username')
        email_pass = config.get('email', 'email_password')
        smtp_server = config.get('email', 'server')
        smtp_port = config.get('email', 'port')

        if from_email == '' or to_email == '' or email_pass == '' or email_user == '' or smtp_server == '' or smtp_port == '':
            return False
        else:
            return True

    def check_certstreamer(self):
        pwd = subprocess.Popen(['pwd'], shell=True, stdout=subprocess.PIPE)
        pwd = pwd.stdout.read().decode('utf-8').strip('\n')
        pwd = pwd.strip('lib')
        configfilepath = '{0}/config.txt'.format(pwd)
        config = configparser.ConfigParser()
        config.read(configfilepath)

        keywords = config.get('certstreamer', 'keywords')
        tlds = config.get('certstreamer', 'tlds')

        if keywords == None or tlds == None:
            return False
        else:
            return True

    def get_email(self):
        pwd = subprocess.Popen(['pwd'], shell=True, stdout=subprocess.PIPE)
        pwd = pwd.stdout.read().decode('utf-8').strip('\n')
        pwd = pwd.strip('lib')
        configfilepath = '{0}/config.txt'.format(pwd)
        config = configparser.ConfigParser()
        config.read(configfilepath)
        to_email = config.get('email', 'to_email')
        return to_email

    def get_pid(self):
        pid = subprocess.Popen(['cat', '/var/run/certwatcher.pid'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = pid.stdout.read().decode('utf-8')
        stderr = pid.stderr.read().decode('utf-8')
        stdout = str(stdout)
        stderr = str(stderr)
        if stdout != '':
            return stdout
        if stderr != '':
            return stderr

    def get_ps(self):
        command = 'ps -ef | grep agent.py | grep -v \'grep\' | awk \'{print $2}\''
        psef = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
        psef = psef.stdout.read().decode('utf-8').strip()
        return psef

    def start_agent(self):
        pwd = subprocess.Popen(['pwd'], shell=True, stdout=subprocess.PIPE)
        pwd = pwd.stdout.read().decode('utf-8').strip('\n')
        pwd = pwd.strip('lib')
        subprocess.Popen(['bash', '{0}/lib/bashscripts/start.sh'.format(pwd), pwd], shell=False, stdout=FNULL, stderr=FNULL)

