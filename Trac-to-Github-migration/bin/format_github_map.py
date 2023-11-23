#!/bin/env python
# Copyright 2022 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

import argparse
import re
import sys
import time

m_str = r'(?P<m_user>.*) = (?P<m_name>.*) <(?P<m_email>.*)>'
u_str = r'(?P<u_user>.*) = (?P<u_name>.*)'
m_pattern = re.compile(m_str)
u_pattern = re.compile(u_str)

parser = argparse.ArgumentParser()
parser.add_argument(
        'map', 
        nargs='?',
        default='cable.github.map')
parser.add_argument(
        'users', 
        nargs='?',
        default='current_cable_users.github.extra.sorted.txt')
args = parser.parse_args()

with open(args.map,'r') as m:
    m_lines = m.readlines()
with open(args.users,'r') as u:
    for u_line in u:
        u_match = u_pattern.match(u_line.rstrip())
        if u_match is not None:
            u_user = u_match.group('u_user')
            u_name = u_match.group('u_name')
            found = False
            for m_line in m_lines:
                m_match = m_pattern.match(m_line.rstrip())
                m_name = m_match.group('m_name')
                if m_name == u_name:
                    found = True
                    m_email = m_match.group('m_email')
                    break
            output = (
                    f'{u_user} = {u_name} <{m_email}>'
                    if found else
                    f'{u_user} = {u_name} <{u_user}@nci.org.au>')
            print(output, flush=True)

