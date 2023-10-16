#!/bin/env python

import argparse
import re
import sys
import time

m_str = r'(?P<m_user>.*) = .*'
u_str = r'(?P<u_user>.*) = (?P<u_name>.*)'
m_pattern = re.compile(m_str)
u_pattern = re.compile(u_str)

parser = argparse.ArgumentParser()
parser.add_argument(
        'map', 
        nargs='?',
        default='cable.sorted.map')
parser.add_argument(
        'users', 
        nargs='?',
        default='current_cable_users.clean.txt')
args = parser.parse_args()

with open(args.users,'r') as u:
    u_lines = u.readlines()
with open(args.map,'r') as m: 
    for m_line in m:
        m_match = m_pattern.match(m_line)
        if m_match is not None:
            m_user = m_match.group('m_user')
            found = False
            for u_line in u_lines:
                u_match = u_pattern.match(u_line)
                u_user = u_match.group('u_user')
                if u_user == m_user:
                    found = True
                    u_name = u_match.group('u_name')
                    break
            output = (
                    f'{m_user} = {u_name} <{m_user}@nci.org.au>'
                    if found else
                    f'{m_user} = {m_user} <{m_user}@nci.org.au>')
            print(output, flush=True)

