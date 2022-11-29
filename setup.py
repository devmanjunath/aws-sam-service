from setuptools import Command, find_packages, setup
import git
import os
from pathlib import Path

GIT_REPO_DIR=Path.joinpath(Path(__file__).parent, "shared_services")
requirements_file = Path.joinpath(GIT_REPO_DIR, "requirements.txt")

required = []
if os.path.exists(requirements_file):
    with open(requirements_file) as f:
      required = f.read().splitlines()

class GitInit(Command):
    description = "Fetch Shared folder from layer repository"

    user_options = []

    def initialize_options(self):
        self.pre_install()

    def finalize_options(self):
        pass

    def run(self):
        try:
            repo = git.Repo(GIT_REPO_DIR)
            current_remote = repo.remotes.origin
            current_remote.pull()
        except Exception:
            print("Shared folder does not exist")
            git.Repo.clone_from("https://github.com/devmanjunath/aws-sam-layer.git", to_path=GIT_REPO_DIR, branch="staging")
    
    def pre_install(self):
        pass



setup_info = {
    "name": "aws-sam-services",
    "version": "1.0.0",
    "packages": find_packages(exclude=["shared"]),
    "install_requires": required,
    "package_data":{
        "shared":["shared"]
    },
    "cmdclass": {
        "pull_code": GitInit,
    },
}

if __name__ == "__main__":
    setup(**setup_info)