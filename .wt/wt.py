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
    import subprocess, sys

    subprocess.call([sys.executable, '-i', '-c',
                     "import os;"
                     "execfile(os.environ['PYTHONSTARTUP']) if os.environ.get('PYTHONSTARTUP') else None;"
                     "import worktry as wt;"])

def materialize(project_name, settings):
    """
    """
    import json, subprocess

    project = {'name': project_name}
    project.update(settings)
    print json.dumps(project, sort_keys=True)
    init_env()
    if 'git' in settings.keys():
        if os.path.exists(settings['path']):
            print "**WARNING** Project path already exist, skipping ..."

        else:
            subprocess.call(['git', 'clone', settings['git'], settings['path']])


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
