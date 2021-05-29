import git
repo = git.Repo('Saheasy/gitTJ')
repo.remotes.origin.pull()
exec(open("gitTJ/gamepadTest.py").read())