import git
repo = git.Repo('Lovebird_PiWars2021')
repo.remotes.origin.pull()
exec(open("Lovebird_PiWars2021/rfRun.py").read())