#!/bin/env python
# Copyright 2022 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

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
args = parser.parse_args()

m_str = r'(?P<m_user>.*) = (?P<m_name>.*) <(?P<m_email>.*)>'
m_pattern = re.compile(m_str)

# GitHub authorization used for name and team membership lookup
auth = Auth.Token(token_str)

g = github.MainClass.Github(auth=auth)
cable_lsm = g.get_organization('CABLE-LSM')
dev_team = cable_lsm.get_team_by_slug('devs')

# Use the dictionary t_users to collect users for Tractive
t_users = dict()

with open(args.map,'r') as m:
    for m_line in m:
        time.sleep(4)
        m_match = m_pattern.match(m_line.rstrip())
        m_user = m_match.group('m_user')
        m_name = m_match.group('m_name')
        m_email = m_match.group('m_email')
        print('[',m_user,']', file=sys.stderr, flush=True)

        # Set a default GitHub username
        t_username = 'ccarouge'
        if len(m_name) > 0:
            # Look up c_user_name as a GitHub user
            g_result = g.search_users(m_name)
            if g_result.totalCount > 0:
                g_named_user = g_result[0]
                # Look up the GitHub user as a CABLE-LSM dev team member
                if dev_team.has_in_members(g_named_user):
                    t_username = g_named_user.login

        t_users[m_user] = {
                    'email': m_email,
                    'name': m_name,
                    'username': t_username}
    t_yaml = {'users': t_users}
    print(yaml.dump(t_yaml, Dumper=yaml.Dumper))

