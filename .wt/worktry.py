"""
module worktry
"""
import json, os

def compute_project(name, depends, envs):
    """
    return computed_env.
    """
    ##Fixme
    worktree_path = os.path.realpath(os.path.join(os.path.dirname(__file__),
                                     ".."))
    projects = {}
    with open(os.path.join(worktree_path, 'projects.json')) as f:
        projects = json.loads(f.read())

    # Update projects with real path
    for p in projects:
        if projects[p].has_key('path'):
            projects[p]['path'] = os.path.join(worktree_path, projects[p]['path'])

    # Update envs with project info
    computed_env = {}
    computed_env['project_name'] = name
    computed_env['depends'] = depends
    computed_env['envs'] = envs
    for p in projects:
        if projects[p].has_key('path'):
            computed_env["{}_project_dir".format(p)] = os.path.realpath(projects[p]['path'])

    computed_env['project_dir'] = computed_env['{}_project_dir'.format(name)]
    return computed_env

def exec_cmd(cmd_str, computed_env):
    """
    Execute cmd_str in the command interpreter.
    """
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

def load_projects(projects):
    """
    Create a projects holder object.
    Each member correspond to a project script.
    """
    projects_holder = type('ProjectsHolder', (object,), {})()
    for p in projects:
        setattr(projects_holder, p, __import__('project_{}'.format(p))) 
        if 'git' in projects[p]:
            for k in projects[p]:
                getattr(projects_holder, p).computed_env[k] = projects[p][k]
 
    return projects_holder

def materialize(project_name, settings):
    """
    """
    import datetime
    import json
    import subprocess
    import uuid

    if 'git' in settings.keys():
        if os.path.exists(settings['path']):
            print "**WARNING** Project path already exist, skipping ..."
            return

    cmd_args = ['git', 'clone', settings['git'], settings['path']]
    d = {
        'content': " ".join(cmd_args),
        'end_time': None,
        'return_value': None,
        'start_time': str(datetime.datetime.utcnow()),
        'type': 'system_command',
        'uuid': uuid.uuid4().hex,
        #computed_env
        #environ
        }
    if settings.get('verbose', None):
        print("**VERBOSE** {}\n".format(json.dumps(d, sort_keys=True)))

    d['return_value'] = subprocess.call(cmd_args)
    d['end_time'] = str(datetime.datetime.utcnow())
    if settings.get('verbose', None):
        print("**VERBOSE** {}\n".format(json.dumps(d, sort_keys=True)))

def materialize_all(projects):
    for p in projects.__dict__:
        if 'git' in projects.__dict__[p].computed_env:
            materialize(p, projects.__dict__[p].computed_env)

##Fixme End common lib
