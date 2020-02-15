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

import worktry

project_name = 'oiio'
depends = {
    'darwin': {
        'formulae': [
            'boost',
            'field3d',
            'giflib',
            'glew',
            'ilmbase', 
            'jpeg',
            'libraw',
            'opencv',
            'openexr',
            'openjpeg',
            'webp',
            ],
        }
}
envs = None
computed_env = {}

def clean():
    """
    clean action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'make clean'.format(**computed_env), computed_env)

def configure():
    """
    configure action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    pass

def distclean():
    """
    distclean action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'make realclean'.format(**computed_env), computed_env)

def make():
    """
    make action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'make -j8'.format(**computed_env), computed_env)

def make_depends():
    """
    make_depends action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    if sys.platform == 'darwin':
        worktry.make_depends(depends['darwin'], computed_env)

def materialize():
    """
    """
    worktry.materialize(project_name, computed_env)

computed_env.update(worktry.compute_project(project_name, depends, envs))
actions = {
    'all': lambda: (configure(), make()),
    'configure': configure,
    'make': make,
    'clean':clean,
    'distclean':distclean,
    'make_depends':make_depends,
}
computed_env['actions'] = sorted(actions.keys())
computed_env['program_name'] = __file__ 
__doc__ = __doc__.format(computed_env=pprint.pformat(computed_env), **computed_env)

if __name__ == "__main__":
    if len(sys.argv) != 2 or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    action = sys.argv[1]
    if action not in actions:
        raise NotImplementedError('Action {}'.format(action))

    actions[action]()
