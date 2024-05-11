import os
import shutil
import tarfile
import tempfile

from github import Github, Auth
from github.Repository import Repository
from github.GitRef import GitRef
import requests


class RepoService:
    def __init__(self, repo_owner: str, repo_name: str, github_auth_token: str):
        self._repo_owner = repo_owner
        self._repo_name = repo_name
        self._github = Github(auth=Auth.Token(github_auth_token))

        self._repo = self._github.get_repo(f"{self._repo_owner}/{self._repo_name}")

    @property
    def default_branch(self):
        return self._repo.default_branch

    @property
    def sha(self):
        return self._repo.get_branch(self.default_branch).commit.sha

    @property
    def tarball_url(self):
        return self._repo.get_archive_link("tarball", ref=self.sha)

    @property
    def contents(self):
        return self._repo.get_contents("")

    def download(self):
        tmp_dir = tempfile.mkdtemp(prefix=f"{self._repo_owner}-{self._repo_name}_{self.sha}")
        tmp_repo_dir = os.path.join(tmp_dir, "repo")
        os.makedirs(tmp_repo_dir, exist_ok=True)

        # Clean the directory
        for root, dirs, files in os.walk(tmp_repo_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        tarfile_path = os.path.join(tmp_dir, f"{self.sha}.tar.gz")

        response = requests.get(self.tarball_url, stream=True)
        if response.status_code == 200:
            with open(tarfile_path, "wb") as f:
                f.write(response.content)
        else:
            raise Exception(
                f"Failed to get tarball url for {self.tarball_url}. Please check if the repository exists and the provided token is valid."
            )

        with tarfile.open(tarfile_path, "r:gz") as tar:
            tar.extractall(path=tmp_repo_dir)  # extract all members normally
            extracted_folders = [
                name
                for name in os.listdir(tmp_repo_dir)
                if os.path.isdir(os.path.join(tmp_repo_dir, name))
            ]
            if extracted_folders:
                root_folder = extracted_folders[0]  # assuming the first folder is the root folder
                root_folder_path = os.path.join(tmp_repo_dir, root_folder)
                for item in os.listdir(root_folder_path):
                    s = os.path.join(root_folder_path, item)
                    d = os.path.join(tmp_repo_dir, item)
                    if os.path.isdir(s):
                        shutil.move(
                            s, d
                        )  # move all directories from the root folder to the output directory
                    else:
                        # Skipping symlinks to prevent FileNotFoundError.
                        if not os.path.islink(s):
                            shutil.copy2(
                                s, d
                            )  # copy all files from the root folder to the output directory

                shutil.rmtree(root_folder_path)  # remove the root folder

        return tmp_dir, tmp_repo_dir




