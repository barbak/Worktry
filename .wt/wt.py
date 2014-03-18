#! /usr/bin/env python
"""
Usage:
  {program_name}

Options:

"""
verbose = True

def init_env():
    """
    Initialize the python environment.
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
        worktry.exec_cmd("virtualenv wt-python", {'verbose': verbose})
        worktry.exec_cmd("virtualenv wt-python --relocatable", {'verbose': verbose})

def call_python(projects):
    """
    Launch the virtualenv python interpreter.
    """
    import os

    os.system('source wt-python/bin/activate && '
              'python -i -c '
              '"import os;'
              'execfile(os.environ[\'PYTHONSTARTUP\']) if os.environ.get(\'PYTHONSTARTUP\') else None;'
              'import worktry as wt;'
              'wt.verbose={verbose};'
              'projects=wt.load_projects({projects});'
              'p=projects;"'.format(verbose=verbose, projects=projects))

if __name__ == "__main__":
    import json, os, sys
    
    if not os.path.exists('projects.json'):
        raise IOError("'projects.json' not found.")

    with open('projects.json', 'r') as f:
        projects = json.loads(f.read())

    init_env()
    call_python(projects)
    print "END"
