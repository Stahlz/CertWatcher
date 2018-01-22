#!/usr/bin/env python

import certstream
import entropy
import datetime
import subprocess 
import configparser

date = datetime.datetime.now().date()
date = date.strftime('%b-%d-%Y')

get_pwd = subprocess.Popen(['pwd'],shell=False, stdout=subprocess.PIPE)
get_pwd = get_pwd.stdout.read().decode('utf-8')
get_pwd = get_pwd.strip()

configfilepath = '{0}/config.txt'.format(get_pwd)
config = configparser.ConfigParser()
config.read(configfilepath)

keywords = config.get('certstreamer','keywords')
tlds = config.get('certstreamer', 'tlds')

write_file_name = '{0}/output/'.format(get_pwd) + date +'_CertStream' + '.log'

word_list = []
tld_list = []

for domain in keywords.split(','):
    word_list.append(domain)

for tld in tlds.split(','):
    tld_list.append(tld)


def score_domain(domain):
    score = 0
    for tld in tld_list:
        if domain.endswith(tld):
            score += 20

    for keyword in word_list:
        if keyword in domain:
            score += 60

    score += int(round(entropy.shannon_entropy(domain) * 50))

    if 'xn--' not in domain and domain.count('-') >= 4:
        score += 20
    return score


def callback(message, context):
    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        for domain in all_domains:
            score = score_domain(domain)
            if score > 75:
                print(
                    "Suspicious:"
                    "{0} :score={1})".format(domain, score))

                with open(write_file_name, 'a') as f:
                    f.write("{0}".format(domain) + '\n')
            elif score > 65:
                print(
                    "Potential: "
                    "{0} :score={1})".format(domain, score))


certstream.listen_for_events(callback)