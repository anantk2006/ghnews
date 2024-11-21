class File:
    def __init__(self, path, content, owner, repo, sha):
        self.path = path
        self.content = content
        self.owner = owner
        self.repo = repo
        self.sha = sha
    def find_api(self):
        pass