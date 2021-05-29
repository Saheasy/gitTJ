import git
repo = git.Repo('gitTJ')
repo.remotes.origin.pull()
exec(open("gitTJ/gamepadTest.py").read())