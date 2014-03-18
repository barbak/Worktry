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
computed_env = {}

def clean():
    """
    clean action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'OPENIMAGEIO_ROOT_DIR={oiio_project_dir}/dist/macosx/ make clean'\
                         .format(**computed_env), computed_env)

def configure():
    """
    configure action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'OPENIMAGEIO_ROOT_DIR={oiio_project_dir}/dist/macosx/ ./configure'\
                         .format(**computed_env), computed_env)

def distclean():
    """
    distclean action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'OPENIMAGEIO_ROOT_DIR={oiio_project_dir}/dist/macosx/ make distclean'\
                         .format(**computed_env), computed_env)

def make():
    """
    make action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'OPENIMAGEIO_ROOT_DIR={oiio_project_dir}/dist/macosx/ make -j8'\
                         .format(**computed_env), computed_env)

def make_depends():
    """
    make_depends action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    #Fixme naive implementation
    #Todo topological sort on depends
    for d in depends['darwin']:
        worktry.exec_command('./project_{}.py all')

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
__doc__ = __doc__.format(computed_env=pprint.pformat(computed_env), **computed_env)

if __name__ == "__main__":
    if len(sys.argv) != 2 or '-h' in sys.argv:
        print __doc__
        sys.exit(0)

    action = sys.argv[1]
    if action not in actions:
        raise NotImplementedError('Action {}'.format(action))

    actions[action]()
