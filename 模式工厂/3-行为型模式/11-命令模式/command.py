import os

verbose = True


class RenameFile:
    def __init__(self, path_src, path_dest):
        self.path_src = path_src
        self.path_dest = path_dest

    def execute(self):
        if verbose:
            print(f"[ renaming {self.path_src}  to {self.path_dest}]")
        os.rename(self.path_src, self.path_dest)

    def undo(self):
        if verbose:
            print(f"[ renaming {self.path_dest} back to {self.path_src}]")
        os.rename(self.path_dest, self.path_src)


class CreateFile:
    def __init__(self, path, txt="hello,world!\n"):
        self.path = path
        self.txt = txt

    def execute(self):
        if verbose:
            print(f"[ creating file {self.path} ]")
        with open(self.path, "w", encoding="utf-8") as f_w:
            f_w.write(self.txt)

    def undo(self):
        if verbose:
            print(f"deleting file {self.path}")
        os.remove(self.path)


class ReadFile:
    def __init__(self, path):
        self.path = path

    def execute(self):
        if verbose:
            print(f"[ reading file {self.path}]")
        with open(self.path, "r", encoding="utf-8") as f_r:
            print(f_r.read())


def main():
    orig_name, new_name = "file_1", "file_2"
    commands = []

    for cmd in CreateFile(orig_name), ReadFile(orig_name), RenameFile(orig_name, new_name):
        commands.append(cmd)

    [c.execute() for c in commands]

    answer = input("reverse the executed commands? [y/n]")
    if str(answer).lower() != 'y':
        print(f"the result is {new_name}")

    for c in reversed(commands):
        try:
            c.undo()
        except AttributeError as e:
            print(f"AttributeError is {e}")


if __name__ == '__main__':
    main()
