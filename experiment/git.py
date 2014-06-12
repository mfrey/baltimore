#!/usr/bin/env python3

import os

from subprocess import Popen, PIPE

class Git:
    def get_revision(self, path_to_repository):
        if path_to_repository.startswith("~"):
            home_dir = os.path.expanduser("~")
            path_to_repository = home_dir + path_to_repository[1:]

        revision =  Popen("git rev-parse HEAD ",  cwd=path_to_repository, stdout=PIPE, shell=True).stdout.read()
        return revision.rstrip()


if __name__ == "__main__":
    git = Git()
    print(git.get_revision("~/Desktop/Projekte/code/ara-sim"))
    print(git.get_revision("/vol/home-vol1/simulant/frey/Desktop/Projekte/code/ara-sim"))
