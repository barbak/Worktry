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

from pprint import pprint, pformat

import worktry

project_name = 'duke_third_party'
depends = {
    'default': {
        'projects': ['duke.materialize'],
    },
    'darwin': {
        'projects': [],
        'formulae': [],
        },
    }

envs = {
    "default": {
        'dependencies': {
            # str(package_name): {
            #   'uris': [
            #       (str(url), str(urn), str(extracted_dir)),
            #       ...
            #   ],
            #   ...
            # }, ...
            'flatbuffers': {
                'uris': [
                    ("https://github.com/google/flatbuffers/archive/v1.0.0.zip",
                     "flatbuffers-1.0.0.zip",
                     "flatbuffers-1.0.0")
                ],
            },
            'boost': {
                'uris': [
                    ("http://sourceforge.net/projects/boost/files/boost/1.56.0/boost_1_56_0.tar.gz/download",
                     "boost_1_56_0.tar.gz",
                     "boost_1_56_0")
                ],
            },
            'openexr': {
                'uris': [
                    ("http://download.savannah.nongnu.org/releases/openexr/ilmbase-2.1.0.tar.gz",
                     "ilmbase.tar.gz",
                     "ilmbase-2.1.0"),
                    ("http://download.savannah.nongnu.org/releases/openexr/openexr-2.1.0.tar.gz",
                     "openexr.tar.gz",
                     "openexr-2.1.0")
                ],
            },
            'oiio': {
                'uris': [
                    ("https://github.com/gchatelet/oiio/archive/master.zip",
                     "oiio.zip",
                     "oiio-master"),
                ],
            },
            'libav': {
                'uris': [
                    ("http://libav.org/releases/libav-10.1.tar.gz",
                     "libav-10.1.tar.gz",
                     "libav-10.1"),
                ],
            },
            'libraw': {
                'uris': [
                    ("https://github.com/LibRaw/LibRaw/archive/0.16.0.zip",
                     "libraw.zip",
                     "LibRaw-0.16.0"),
                ],
            },
            'gtest': {
                'uris': [
                    ("https://github.com/google/googletest/archive/release-1.7.0.zip",
                     "gtest-1.7.0.zip",
                     "gtest-1.7.0"),
                ],
            },
        }
    },
    "darwin": {
        # "dyld_library_path": ["{oiio_project_dir}/dist/macosx"]
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
                     'make clean'
                     .format(**computed_env), computed_env)


# def configure():
#     """
#     configure action.
#     """
#     if sys.platform != 'darwin':
#         raise NotImplementedError(sys.platform)
#
#     worktry.exec_cmd('cd {project_dir};'
#                      'OPENIMAGEIO_ROOT_DIR={oiio_project_dir}/dist/macosx/ ./configure'
#                      .format(**computed_env), computed_env)


def distclean():
    """
    distclean action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'make distclean'
                     .format(**computed_env), computed_env)


def make():
    """
    make action.
    """
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    worktry.exec_cmd('cd {project_dir};'
                     'make -j4'.format(**computed_env), computed_env)


def make_depends():
    """
    make_depends action.
    """
    worktry.make_depends(depends['default'], computed_env)
    if sys.platform != 'darwin':
        raise NotImplementedError(sys.platform)

    if sys.platform != 'darwin':
        worktry.make_depends(depends['darwin'], computed_env)


def materialize():
    """
    """
    # worktry.materialize(project_name, computed_env)
    download_archives()


def download_archives():
    """
    """
    def download_archive(url, urn, dirname):
        worktry.download_to(url, urn, computed_env)

    git_commit = "sha1"
    _run_func_on_depency(download_archive)


def extract_archives():
    def extract_archive(url, urn, dirname):
        worktry.extract_to(urn, dirname, computed_env)
        # print("TODO worktry.extract_to(urn, dirname, computed_env)")
        # # worktry.exec_cmd("")
        # if os.path.exists(dirname) is False:
        #     print("TODO os.rename(worktry.get_archive_root_dirname(urn), dirname)", urn, dirname)

    _run_func_on_depency(extract_archive)


def _run_func_on_depency(func):
    for k in computed_env['envs']['default']['dependencies']:
        dependency = computed_env['envs']['default']['dependencies'][k]['uris']
        for d in dependency:
            url, urn, dirname = d
            func(url,
                 os.path.join(computed_env['duke_third_party_project_dir'], urn),
                 os.path.join(computed_env['duke_third_party_project_dir'], dirname))


computed_env.update(worktry.compute_project(project_name, depends, envs))
actions = {
    'all': lambda: (download_archives(), extract_archives()),
    # 'configure': configure,
    'extract': extract_archives,
    'download_archives': download_archives,
    'make': make,
    'clean': clean,
    'distclean': distclean,
    'make_depends': make_depends,
}
computed_env['actions'] = sorted(actions.keys())
computed_env['program_name'] = __file__ 
__doc__ = __doc__.format(computed_env=pformat(computed_env), **computed_env)

if __name__ == "__main__":
    if len(sys.argv) != 2 or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    action = sys.argv[1]
    if action not in actions:
        raise NotImplementedError('Action {}'.format(action))

    actions[action]()
    sys.exit(0)
