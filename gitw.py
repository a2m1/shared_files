#!/usr/bin/env python

from sys import argv
import git

sourceBranch = argv[1]
targetBranch = argv[2]
repoPath = argv[3]


def checkout_branch(self):
    print "Trying to checkout branch: " + self
    try:
        repo.git.checkout(self)
    except Exception, e:
        print "Error! Bad branch!!!"
        raise e


def push_to_remote_branch():
    print "Trying to push changes"
    try:
        repo.git.push()
    except Exception, e:
        print "Error! Failed to push changes!!!"
        raise e


def find_merge_commit():

    """
    Note:
    '%H': commit hash
    '%P': parent hashes
    """
    commit_log = str(repo.git.log('--pretty=format:%H:%P'))
    commit_log = commit_log.split("\n")
    commit_list = []
    for line in commit_log:
        line = line.split(":")
        commit_list.append(line)

    proceed_flag = True  # to remove only latest merge commit
    rebase_flag = False  # to use commit for rebase before merge

    for commit in commit_list:
        if rebase_flag:
            try:
                repo.git.rebase("-i", commit[0])
            except Exception, e:
                print "Error! Rebase has been failed!!!"
                raise e
            proceed_flag = False
        if not proceed_flag:
            break
        else:
            parent_list = commit[1].split(" ")
            if len(parent_list) > 1:
                print "Founded merge commit with few parent commits: " + commit[0]
                for parent_commit in parent_list:
                    branches = repo.git.branch("--contains", parent_commit)
                    branches = branches.replace("\n", " ").split(" ")
                    for branch in branches:
                        if branch == sourceBranch:
                            print "Parent commit " + parent_commit + " exists in source branch \"" + branch + "\""
                            rebase_flag = True


print "Trying to open repository: " + repoPath
try:
    repo = git.Repo(repoPath)
except Exception, e:
    print "Error! Bad repository!!!"
    raise e

checkout_branch(sourceBranch)
checkout_branch(targetBranch)

mergedBranches = str(repo.git.branch("--merged", targetBranch))
mergedBranches = mergedBranches.replace("\n"," ").split(" ")

for mergedBranch in mergedBranches:
    if mergedBranch == sourceBranch:
        print "Source branch \"" + sourceBranch + "\" already merged in the target branch \"" + targetBranch + "\""
        find_merge_commit()

try:
    mergeBranch = "origin/" + sourceBranch
    repo.git.merge(mergeBranch, "--squash")
except Exception, e:
    print "Error! Merge has been failed!!!"
    raise e
repo.git.add(all=True)
print repo.git.commit(m='Merge squash commit')
push_to_remote_branch()