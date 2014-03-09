#! /usr/bin/env python
"""
NAME
    {program_name} - {project_name} build actions script.

SYNOPSIS
    {program_name} actions

DESCRIPTION
    actions
        {actions}

    computed_env
{computed_env}
"""
import os, sys
import json

import pprint

project_name = 'duke'
depends = {
    'darwin': {
        'projects':["oiio"],
        'formulae':[],
        },
    }

envs = {
    "default": {},
    "darwin": {
        "dyld_library_path": ["{oiio_project_dir}/dist/macosx"]
        },
}

##Fixme Should be in a lib or a template
worktree_path = os.path.realpath(os.path.dirname(__file__))
projects = {}
with open('projects.json') as f:
    projects = json.loads(f.read())

# Update projects with real path
for p in projects:
    if projects[p].has_key('path'):
        projects[p]['path'] = os.path.join(worktree_path, projects[p]['path'])

# Update envs with project info
computed_env = {}
computed_env['program_name'] = __file__
computed_env['project_name'] = project_name
computed_env['depends'] = depends
computed_env['envs'] = envs
for p in projects:
    if projects[p].has_key('path'):
        computed_env["{}_project_dir".format(p)] = os.path.realpath(projects[p]['path'])

computed_env['project_dir'] = computed_env['{}_project_dir'.format(project_name)]

def _exec_cmd(cmd_str):
    import uuid, datetime
    
    d = {
        'content': cmd_str,
        'end_time': None,
        'return_value': None,
        'start_time': str(datetime.datetime.utcnow()),
        'type': 'system_command',
        'uuid': uuid.uuid4().hex,
        #computed_env
        #environ
        }
    if computed_env.get('verbose', None):
        print("**VERBOSE** {}\n".format(json.dumps(d, sort_keys=True)))
    
    d['return_value'] = os.system(cmd_str)
    d['end_time'] = str(datetime.datetime.utcnow())
    if computed_env.get('verbose', None):
        print("**VERBOSE** {}\n".format(json.dumps(d, sort_keys=True)))

##Fixme End common lib

## main commands
def clean():
    """
    clean action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    _exec_cmd('cd {project_dir};'
              'OPENIMAGEIO_ROOT_DIR={oiio_project_dir}/dist/macosx/ make clean'\
                  .format(**computed_env))

def configure():
    """
    configure action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    _exec_cmd('cd {project_dir};'
              'OPENIMAGEIO_ROOT_DIR={oiio_project_dir}/dist/macosx/ ./configure'\
                  .format(**computed_env))

def distclean():
    """
    distclean action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    _exec_cmd('cd {project_dir};'
              'OPENIMAGEIO_ROOT_DIR={oiio_project_dir}/dist/macosx/ make distclean'\
                  .format(**computed_env))

def make():
    """
    make action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    _exec_cmd('cd {project_dir};'
              'OPENIMAGEIO_ROOT_DIR={oiio_project_dir}/dist/macosx/ make -j8'\
                  .format(**computed_env))

def make_depends():
    """
    make_depends action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    #Fixme naive implementation
    #Todo topological sort on depends
    for d in depends['darwin']:
        _exec_command('./project_{}.py all')

actions = {
    'all': lambda: (configure(), make()),
    'configure': configure,
    'make': make,
    'clean':clean,
    'distclean':distclean,
    'make_depends':make_depends,
}
computed_env['actions'] = sorted(actions.keys())
__doc__ = __doc__.format(computed_env=pprint.pformat(computed_env), **computed_env)

if __name__ == "__main__":
    if len(sys.argv) != 2 or '-h' in sys.argv:
        print __doc__
        sys.exit(0)

    action = sys.argv[1]
    if action not in actions:
        raise NotImplementedError('Action {}'.format(action))

    actions[action]()
