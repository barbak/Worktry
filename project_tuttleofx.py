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

project_name = 'tuttleofx'
depends = {
    'darwin': {
        'formulae': [
            'scons',
            'boost',
            'ffmpeg',
            'fontconfig',
            'freeglut',
            'freetype',
            'imagemagick',
            'jpeg',
            'jpeg-turbo',
            'openexr',
            'openjpeg',
            'libraw',
            'swig',
            ],
        'projects': ['oiio']
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
                     'TUTTLEOFX={project_dir} scons -c'.format(**computed_env), computed_env)

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
                     'rm -rf .dist'.format(**computed_env), computed_env)

def make(arg=''):
    """
    make action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'TUTTLEOFX={project_dir} scons -j8'.format(**computed_env) +
                     " {}".format(arg),
                     computed_env)

def make_depends():
    """
    make_depends action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    #Fixme naive implementation
    #Todo topological sort on depends
    if sys.platform == 'darwin':
        worktry.make_depends(depends['darwin'], computed_env)

def materialize():
    """
    """
    worktry.materialize(project_name, computed_env)
    if sys.platform == 'darwin':
        if 'formulae' in depends['darwin']:
            worktry.exec_cmd('brew install --build-from-source {}'\
                                 .format(" ".join(depends['darwin']['formulae'])),
                             computed_env)


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
