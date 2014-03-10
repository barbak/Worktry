#! /usr/bin/env python
import git
import worktry as wt

def init_env():
    """
    """
    import os, sys, subprocess

    shell_cmd = os.environ.get('SHELL', '/bin/sh')
    wt_dir = os.path.abspath(os.path.dirname(__file__))
    if wt_dir not in os.environ.get('PYTHONPATH', ''):
        os.environ['PYTHONPATH'] = "{}{}{}/.wt" .format(os.environ.get('PYTHONPATH', ''),
                                                        ':'
                                                        if os.environ.get('PYTHONPATH', '')
                                                        else "",
                                                        wt_dir)

    subprocess.call(shell_cmd, env=os.environ, shell=True)

def materialize(project_name, settings):
    """
    """
    print project_name, settings

if __name__ == "__main__":
    import json, os, sys
    
    if not os.path.exists('projects.json'):
        raise IOError("'projects.json' not found.")

    with open('projects.json', 'r') as f:
        projects = json.loads(f.read())

    for p in projects:
        materialize(p, projects[p])

    init_env()
    print "END"
