"""
module worktry
"""
import json, os

verbose = True if os.environ.get('VERBOSE') else False


def compute_project(name, depends, envs):
    """
    return computed_env.
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
            computed_env["{}_project_dir".format(p)] = os.path.realpath(projects[p]['path'])

    computed_env['project_dir'] = computed_env['{}_project_dir'.format(name)]
    return computed_env

def exec_cmd(cmd_str, computed_env):
    """
    Execute cmd_str in the command interpreter.
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
            # exec_cmd('python project_{}.py all'.format(project_name),
            #          computed_env)
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
        if os.path.exists(settings['path']):
            print ("**WARNING** Project path '{}' "
                   "already exist, skipping ...".format(settings['path']))

        else:
            cmd_args = ['git', 'clone', settings['git'], settings['path']]
            exec_cmd(" ".join(cmd_args), settings)

        import git

        if git_submodules and git.Repo(settings['path']).git.submodule():
            cmd_str = ("cd {};"
                       "git submodule init;"
                       "git submodule update;".format(settings['path']))
            exec_cmd(cmd_str, settings)


def materialize_all(projects):
    for p in projects.__dict__:
        if 'git' in projects.__dict__[p].computed_env:
            materialize(p, projects.__dict__[p].computed_env)

def pip(arg_str):
    """
    """
    exec_cmd("pip {}".format(arg_str), {'verbose': verbose})
##Fixme End common lib
