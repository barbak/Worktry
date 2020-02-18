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
    import platform
    import subprocess

    wt_dir = os.path.join(os.path.realpath(os.path.dirname(__file__)), '.wt')
    if platform.system() != 'Windows' and wt_dir not in os.environ.get('PYTHONPATH', ''):
        os.environ['PYTHONPATH'] = "{}{}{}" .format(os.environ.get('PYTHONPATH', ''),
                                                    ':' if os.environ.get('PYTHONPATH', False)
                                                    else "",
                                                    wt_dir)


def call_python(projects):
    """
    Launch the virtualenv python interpreter.
    """
    import os
    import platform

    os_name = platform.system()
    return os.system(
        ('source wt-python/bin/activate && ' if os_name != 'Windows' else '') +
        '{}ipython -i -c '.format('wt-python\\Scripts\\' if os_name == 'Windows' else '') +
        '"import os;'
        'execfile(os.environ[\'PYTHONSTARTUP\']) if os.environ.get(\'PYTHONSTARTUP\') else None;'
        'import worktry as wt;'
        'wt.verbose={verbose};'
        'projects=wt.load_projects({projects});'
        'p=projects;"'.format(verbose=verbose, projects=projects)
    )


if __name__ == "__main__":
    import json, os, sys
    
    if not os.path.exists('projects.json'):
        raise IOError("'projects.json' not found.")

    with open('projects.json', 'r') as f:
        projects = json.loads(f.read())

    init_env()
    call_python(projects)
    print("END")
