import git
import shutil
import os
from pathlib import Path
import pandas as pd
import pandemics.processing
from typing import *
import subprocess

def clone_repo(git_url: str, path: str, force: bool = True, use_ssh: bool = False) -> Union[git.Repo, None]:
    repo_path = Path(path)
    if repo_path.exists():
        if not force:
            return git.Repo(path)
        shutil.rmtree(repo_path)
    if use_ssh:
        key = os.path.expanduser('~/.ssh/id_rsa')
        repo = git.Repo.clone_from(git_url, path, env={'GIT_SSH_COMMAND': f'ssh -i {key}'})
    else:
        repo = git.Repo.clone_from(git_url, path)
    
    return repo

def clone_jhu(path: str, force: bool = True) -> None:
    return clone_repo('git@github.com:CSSEGISandData/COVID-19.git', path, force=force, use_ssh=False)

def push_files(repo: git.Repo, files: Iterable[str], msg: str = '') -> None:
    try:
        origin = repo.remote(name='origin')
        origin.pull()
        print(f'Pushing files to {repo}')
        repo.git.add(files)
        repo.index.commit(msg)
        origin.push()
    except Exception as e:
        print(f'Error pushing files: {e}')

def push_files_cmd(repo_dir: str, files: Iterable[str], msg: str = '') -> None:
    os.chdir(repo_dir)

    subprocess.call(['git', 'pull'])

    for f in files:
        subprocess.call(['git', 'add', f])
    
    subprocess.call(['git', 'commit', '-m', msg])
    subprocess.call(['git', 'push'])