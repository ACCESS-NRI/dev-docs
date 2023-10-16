#!/bin/env python

import argparse
import github
import re
import sys
import time
import yaml

from github import Auth
from github_organization_token import token_str

parser = argparse.ArgumentParser()
parser.add_argument(
        'map', 
        nargs='?',
        default='cable.map')
parser.add_argument(
        'bootstrap', 
        nargs='?',
        default='tractive.config.bootstrap.yaml')
args = parser.parse_args()

# GitHub authorization used for name lookup
auth = Auth.Token(token_str)
g = github.MainClass.Github(auth=auth)

# Regular expression pattern matching args.map
m_str = r'(?P<m_user>.*) = (?P<m_name>.*) <(?P<m_email>.*)>'
m_pattern = re.compile(m_str)

with open(args.map,'r') as m:
    m_lines = m.readlines()

# Use the dictionary t_users to collect users for Tractive
t_users = dict()
with open(args.bootstrap,'r') as b:
    b_yaml = yaml.load(b.read(), Loader=yaml.Loader)
    b_users =  b_yaml['users']
    for b_user in b_users:
        time.sleep(4)
        print(b_user, file=sys.stderr, flush=True)
        # If b_user includes multiple NCI usernames, use the first one
        n_user = (b_user.split(',')[0]
                if ',' in b_user else
                b_user)
        # Look for the NCI username n_user 
        b_user_dict = b_users[n_user]
        b_found = False
        for m_line in m_lines:
            m_match = m_pattern.match(m_line)
            m_user = m_match.group('m_user')
            if m_user == n_user:
                b_found = True
                m_name = m_match.group('m_name')
                # Look up m_name as a GitHub user
                g_result = g.search_users(m_name)
                g_user = (
                    g_result[0].login 
                    if g_result.totalCount > 0 else
                    'ccarouge')
                m_email = m_match.group('m_email')
                break
        if b_found:
            t_users[b_user] = {
                    'email': m_email,
                    'name': m_name,
                    'username': g_user}
        else:
            t_users[b_user] = {
                    'email': 'ccarouge@nci.org.au',
                    'name': b_user,
                    'username': 'ccarouge'}
    t_yaml = {'users': t_users}
    print(yaml.dump(t_yaml, Dumper=yaml.Dumper))

