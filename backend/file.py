import re
kLINK_DETECTION_REGEX = r"/(([a-z]+:\/\/)?(([a-z0-9\-]+\.)+([a-z]{2}|aero|arpa|biz|com|coop|edu|gov|info|int|jobs|mil|museum|name|nato|net|org|pro|travel|local|internal))(:[0-9]{1,5})?(\/[a-z0-9_\-\.~]+)*(\/([a-z0-9_\-\.]*)(\?[a-z0-9+_\-\.%=&amp;]*)?)?(#[a-zA-Z0-9!$&'()*+.=-_~:@/?]*)?)(\s+|$)/gi;"

class File:
    def __init__(self, path, content, owner, repo, sha):
        self.path = path
        self.content = content
        self.owner = owner
        self.repo = repo
        self.sha = sha
    def find_python_api(self, split):
        for line in split:
            if "import" in line:
                words = line.split(" ")
                if 'from' in words:
                    yield words[words.index('from') + 1]
                elif 'import' in words:
                    yield words[words.index('import') + 1]
            elif "http" in line:
                match = re.match(kLINK_DETECTION_REGEX, line)
                if match:
                    yield match.group(0)
    def find_js_api(self, split):
        for line in split:
            if "import" in line or 'require' in line:
                words = line.split(" ")
                if 'from' in words:
                    yield words[words.index('from') + 1]
                elif 'import' in words:
                    yield words[words.index('import') + 1]
                else:
                    require = line.split("require")
                    if len(require) > 1:
                        yield require[1]
            elif "http" in line:
                match = re.match(kLINK_DETECTION_REGEX, line)
                if match:
                    yield match.group(0)

    def find_cpp_api(self, split):
        for line in split:
            if "include" in line:
                words = line.split(" ")
                if 'include' in words:
                    yield words[words.index('include') + 1]
            elif "http" in line:
                match = re.match(kLINK_DETECTION_REGEX, line)
                if match:
                    yield match.group(0)
    
    def find_rust_api(self, split):
        for line in split:
            if "use" in line:
                words = line.split(" ")
                if 'use' in words:
                    yield words[words.index('use') + 1]
            elif "http" in line:
                match = re.match(kLINK_DETECTION_REGEX, line)
                if match:
                    yield match.group(0)

    
    def find_python_struct_names(self, split):
        for line in split:
            if "class " in line:
                match = re.match(r'class\s+(\w+)', line)
                if match:
                    yield match.group(1)
            elif "def " in line:
                match = re.match(r'def\s+(\w+)', line)
                if match:
                    yield match.group(1)
    
    def find_js_struct_names(self, split):
        for line in split:
            if "class " in line:
                match = re.match(r'class\s+(\w+)', line)
                if match:
                    yield match.group(1)
            elif "function " in line:
                match = re.match(r'function\s+(\w+)', line)
                if match:
                    yield match.group(1)
    
    def find_cpp_struct_names(self, split):
        for line in split:
            if "class " in line:
                match = re.match(r'class\s+(\w+)', line)
                if match:
                    yield match.group(1)
            elif "struct " in line:
                match = re.match(r'struct\s+(\w+)', line)
                if match:
                    yield match.group(1)
    
    def find_rust_struct_names(self, split):
        for line in split:
            if "struct " in line:
                match = re.match(r'struct\s+(\w+)', line)
                if match:
                    yield match.group(1)
            if "fn " in line:
                match = re.match(r'fn\s+(\w+)', line)
                if match:
                    yield match.group(1)                

    def find_api(self):
        split = self.content.split("\n")
        if self.path.endswith(".py"):
            api = self.find_python_api(split)
            struct_names = self.find_python_struct_names(split)
            
        elif self.path.endswith(".ts") or self.path.endswith(".js"):
            return self.find_js_api(split)
        elif self.path.endswith(".cpp"):
            return self.find_cpp_api(split)
        elif self.path.endswith(".rs"):
            return self.find_rust_api(split)
        else:
            raise Exception("Unsupported file type")