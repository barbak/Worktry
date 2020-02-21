"""
module worktry
"""
import json
import os

from pprint import (
    pformat,
    pprint,
)

verbose = True if os.environ.get('VERBOSE') else False


class LogContextManager(object):
    pass

def compute_project(name, depends, envs):
    """
    return computed_env.
    TODO
    # darwin
    # (wt-python) $ sysctl -n hw.ncpu
    # 4
    """
    ##Fixme Relative search
    worktree_path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    projects = {}
    with open(os.path.join(worktree_path, 'projects.json')) as f:
        projects = json.loads(f.read())

    # Update projects with real path
    for p in projects:
        if 'path' in projects[p]:
            projects[p]['path'] = os.path.join(worktree_path, projects[p]['path'])

    # Update envs with project info
    computed_env = {
        'project_name': name,
        'depends': depends,
        'envs': envs,
        'verbose': verbose
    }
    for p in projects:
        if 'path' in projects[p]:
            computed_env["{}_project_dir".format(p)] = projects[p]['path']
            if p == name:
                computed_env['path'] = projects[p]['path']

        if 'git' in projects[p]:
            computed_env["{}_git_url".format(p)] = projects[p]['git']
            if p == name:
                computed_env['git'] = projects[p]['git']

    computed_env['project_dir'] = computed_env['{}_project_dir'.format(name)]
    return computed_env


def download_to(url, urn, computed_env):
    """
    """
    from pprint import pprint
    print("*"*42)
    pprint(computed_env)
    print(url, urn)
    # if os.path.exists(urn) is False:
    #     exec_cmd(f"curl -L -o {urn} {url}", computed_env)


def exec_cmd(cmd_str, computed_env):
    """
    Execute cmd_str in the command interpreter.
    TODO
        use subprocess
        use computed_env as the environment execution
        try / catch exception
    """
    import uuid, datetime

    computed_env['verbose'] = verbose
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
    if computed_env['verbose']:
        print("*VERBOSE* {}".format(json.dumps(d, sort_keys=True)))

    d['return_value'] = os.system(cmd_str)
    d['end_time'] = str(datetime.datetime.utcnow())
    if computed_env['verbose']:
        print("*VERBOSE* {}".format(json.dumps(d, sort_keys=True)))


def download_to(name, dirname, computed_env):
    """
    TODO usse tarfile and zipfile instead of exec cmd
    """
    if os.path.exists(dirname) is True:
        raise RuntimeError(f"Destination dir {repr(dirname)} already exists.")

    print("TODO worktry.extract_to(urn, dirname, computed_env)")
    if os.uname().sysname == 'Darwin':
        if name.endswith('gz'):
            exec_cmd(f"tar zxvf {name}")

        elif name.endswith('zip'):
            exec_cmd(f"unzip x {name}")

    if os.path.exists(dirname) is False:
        # with LogContextManager(verbose):
        print("TODO os.rename(worktry.get_archive_root_dirname(urn), dirname)", name, dirname)
        # os.rename(get_archive_root_dirname(name), dirname)


def load_projects(projects):
    """
    Create a projects holder object.
    Each member correspond to a project script.
    """
    projects_holder = type('ProjectsHolder', (object,), {})()
    for p in projects:
        setattr(projects_holder, p, __import__('project_{}'.format(p)))
        for k in projects[p]:
            getattr(projects_holder, p).computed_env[k] = projects[p][k]

    return projects_holder


def make_depends(depends, computed_env):
    """
    """
    computed_env['verbose'] = verbose
    #Fixme naive implementation
    #Todo topological sort on depends
    if 'projects' in depends:
        for project_name in depends['projects']:
            tokens = project_name.split('.')
            project_name = tokens[0]
            action = tokens[1] if len(tokens) == 2 else 'all'
            exec_cmd('python project_{}.py {}'.format(project_name, action),
                     computed_env)

    if 'formulae' in depends:
        exec_cmd(
            'brew install --build-from-source {}'.format(
                " ".join(depends['formulae'])
            ),
            computed_env
        )


def materialize(project_name, settings, git_submodules=True):
    """
    Materialize project_name depending on settings dict.
    If git_submodules is True and project_name is materailized from
    a git repository, git submodules will also be checked out.
    """
    settings['verbose'] = verbose
    if 'git' in settings:
        git_clone_from_pygit2(project_name, settings, git_submodules)

        # if os.path.exists(settings['path']):
        #     print("**WARNING** Project path '{}' "
        #           "already exist, skipping ...".format(settings['path']))
        #
        # else:
        #     cmd_args = ['git', 'clone', settings['git'], settings['path']]
        #     exec_cmd(" ".join(cmd_args), settings)
        #
        # import git
        #
        # if git_submodules and git.Repo(settings['path']).git.submodule():
        #     cmd_str = ("cd {};"
        #                "git submodule init;"
        #                "git submodule update;".format(settings['path']))
        #     exec_cmd(cmd_str, settings)


def materialize_all(projects):
    for p in projects.__dict__:
        if 'git' in projects.__dict__[p].computed_env:
            materialize(p, projects.__dict__[p].computed_env)


def pip(arg_str):
    """
    """
    exec_cmd("pip {}".format(arg_str), {'verbose': verbose})

##Fixme End common lib

### GETTERS ?
import tarfile
import zipfile


def get_zipfile_root_dirname(filename):
    if zipfile.is_zipfile(filename) is False:
        raise RuntimeError(f"File {repr(filename)} is not a zipfile.")

    return list(
        {f.split('/')[0] for f in zipfile.ZipFile(filename).namelist()}
    )[0]


def get_tarfile_root_dirname(filename):
    if tarfile.is_tarfile(filename) is False:
        raise RuntimeError(f"File {repr(filename)} is not a tarfile.")

    with tarfile.open(filename) as tf:
        return list(
            {f.split('/')[0] for f in tf.getnames()}
        )[0]


def get_archive_root_dirname(filename):
    if tarfile.is_tarfile(filename) is True:
        return get_tarfile_root_dirname(filename)

    if zipfile.is_zipfile(filename) is True:
        return get_zipfile_root_dirname(filename)

    raise RuntimeError(f"File {repr(filename)} is not handled.")

### /GETTERS

### GIT UTILS
def git_clone_from_pygit2(project_name, settings, git_submodules=True):
    """
    TODO
        SUBMODULE FLAG
        EVENT DICT LOG - VERBOSE
        BETTER CALLBAKS PRINTING
    """

    import pygit2

    class MyRemoteCallbacks(pygit2.RemoteCallbacks):

        username = None
        password = None

        def credentials(self, url, username_from_url, allowed_types):
            """
            *****
            """
            import getpass

            print(url, username_from_url, allowed_types)
            if not self.username:
                self.username = input(f"User name for '{url}' ? ")
                self.password = getpass.getpass(f"Password for '{url}' ? ")

            return pygit2.UserPass(self.username, self.password)

        def transfer_progress(self, stats):
            """Transfer progress callback

            Override with your own function to report transfer progress.

            :param TransferProgress stats: The progress up to now

            self.total_objects = tp.total_objects
            Total number of objects to download

            self.indexed_objects = tp.indexed_objects
            Objects which have been indexed

            self.received_objects = tp.received_objects
            Objects which have been received up to now

            self.local_objects = tp.local_objects
            Local objects which were used to fix the thin pack

            self.total_deltas = tp.total_deltas
            Total number of deltas in the pack

            self.indexed_deltas = tp.indexed_deltas
            Deltas which have been indexed

            self.received_bytes = tp.received_bytes
            Number of bytes received up to now
            """
            # def clear_current_terminal_line():
            #     print(f"\r{ ' ' * os.get_terminal_size().columns}\r", end='')
            #     sys.stdout.flush()
            #

            import sys
            clear_current_terminal_line = lambda: print(f"\r{ ' ' * os.get_terminal_size().columns}\r", end='')
            clear_current_terminal_line()
            sys.stdout.write(f"Stats: {stats.total_objects}\t{stats.indexed_objects}\t"
                  f"{stats.received_objects}\t{stats.local_objects}\t"
                  f"{stats.total_deltas}\t{stats.indexed_deltas}\t{stats.received_bytes}",
                  )
            sys.stdout.flush()

    pygit2_remote_callbacks = MyRemoteCallbacks()
    print(f"Cloning {repr(project_name)} with pygit2")
    destination = settings['path']
    git_url = settings['git']
    if os.path.exists(destination):
        print(f"Directory '{destination}' already exist.")

    else:
        print(f"Cloning {git_url} to {destination} ...")
        r = pygit2.clone_repository(git_url, destination, callbacks=pygit2_remote_callbacks)
        if git_submodules is True and r.listall_submodules() != []:
            print("\nSubmodules fetching.")
            r.update_submodules(init=True, callbacks=pygit2_remote_callbacks)

        print(f"\n{r}")
        print("OK")

### /GIT UTILS
