#! /usr/bin/env python
"""
Usage:
  {program_name}
"""
import git
import worktry as wt

def init_env():
    """
    """
    import os

    wt_dir = os.path.abspath(os.path.dirname(__file__))
    if wt_dir not in os.environ.get('PYTHONPATH', ''):
        os.environ['PYTHONPATH'] = "{}{}{}/.wt" .format(os.environ.get('PYTHONPATH', ''),
                                                        ':'
                                                        if os.environ.get('PYTHONPATH', '')
                                                        else "",
                                                        wt_dir)


def call_python():
    import os, subprocess, sys

    subprocess.call([sys.executable, '-i', '-c' 
                     "import os, sys;"
                     "execfile(os.environ['PYTHONSTARTUP']) if os.environ.get('PYTHONSTARTUP') else None;"
                     "import worktry as wt"],
                    env=os.environ, shell=True)

def materialize(project_name, settings):
    """
    """
    print project_name, settings
    init_env()

if __name__ == "__main__":
    import json, os, sys
    
    if not os.path.exists('projects.json'):
        raise IOError("'projects.json' not found.")

    with open('projects.json', 'r') as f:
        projects = json.loads(f.read())

    for p in projects:
        materialize(p, projects[p])

    init_env()
    call_python()
    print "END"
