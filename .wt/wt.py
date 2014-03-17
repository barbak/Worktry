#! /usr/bin/env python
"""
Usage:
  {program_name}

Options:

"""

def init_env():
    """
    """
    import os
    import subprocess

    wt_dir = os.path.abspath(os.path.dirname(__file__))
    if wt_dir not in os.environ.get('PYTHONPATH', ''):
        os.environ['PYTHONPATH'] = "{}{}{}/.wt" .format(os.environ.get('PYTHONPATH', ''),
                                                        ':'
                                                        if os.environ.get('PYTHONPATH', '')
                                                        else "",
                                                        wt_dir)

    if not os.path.exists(os.path.join(wt_dir, 'wt-python')):
        import worktry
        subprocess.call(['virtualenv', 'wt-python'])
        subprocess.call(['virtualenv', 'wt-python', '--relocatable'])

def call_python(projects):
    """
    TODO: Use virtualenv wt-python interpreter
    """
    import subprocess, sys

    subprocess.call([sys.executable, '-i', '-c',
                     "import os;"
                     "execfile(os.environ['PYTHONSTARTUP']) if os.environ.get('PYTHONSTARTUP') else None;"
                     "import worktry as wt;"
                     "projects={}".format(projects)])


if __name__ == "__main__":
    import json, os, sys
    
    if not os.path.exists('projects.json'):
        raise IOError("'projects.json' not found.")

    with open('projects.json', 'r') as f:
        projects = json.loads(f.read())

    init_env()
    call_python(projects)
    print "END"
