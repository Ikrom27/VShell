import os
from zipfile import ZipFile
import sys


class VShell:
    def __init__(self, file_system):
        self.ROOT = "root:"
        self.local_path = ""
        self.all_files = ZipFile(file_system).filelist

    def __delete_symbol(self, path):
        for letter in path:
            if letter == "/":
                path = path[1:]
            else:
                break
        return path

    def __pathFormat(self, path, extension_path):
        if "root:" in extension_path:
            path = extension_path[len("root:"):]
        else:
            path += "/" + extension_path
        return self.__delete_symbol(path)

    def __filesColor(self, name):
        if ".txt" in name:
            return "\033[34m{}\033[0m".format(name)
        return "\033[33m{}\033[0m".format(name)

    def ls(self, path, files):
        path = self.__delete_symbol(path)
        for file in files:
            if path in file.filename:
                file_names = file.filename[len(path):].split("/")
                file_names = list(filter(None, file_names))
                if len(file_names) > 1 or not file_names:
                    continue
                print(self.__filesColor(file_names[0]))

    def cd(self, path: str, extension_path: str, files: list) -> bool:
        path = self.__pathFormat(path, extension_path)
        if path == "":
            self.local_path = ""
            return True
        if "../" in path:
            self.local_path = self.local_path[:len(self.local_path) - len(self.local_path.split("/")[-1]) - 1]
            return True
        for file in files:
            if path in file.filename:
                self.local_path = "/" + path
                return True
        return False

    def cat(self, path, extension_path, zip_file):
        path = self.__pathFormat(path, extension_path)
        flag = False
        for file in ZipFile(zip_file).filelist:
            if path in file.filename:
                flag = True
                with ZipFile(zip_file) as files:
                    with files.open(path, 'r') as file:
                        for line in file.readlines():
                            print(line.decode('utf8').strip())
        if not flag:
            print("\033[31m{}\033[0m".format("Can`t open this file"))

    def commandProcessing(self):
        command = input(self.ROOT + "/> ")
        while command != "exit":
            command = command.split(" ")

            match command[0]:
                case "pwd":
                    print("\033[32m{}\033[0m".format("  " + self.ROOT + ("/" if not self.local_path else self.local_path)))
                case "ls":
                    self.ls(self.local_path, self.all_files)
                case "cd":
                    try:
                        command[1]
                    except IndexError:
                        print("\033[31m{}\033[0m".format("Don`t know this command"))
                    if self.cd(self.local_path, command[1], self.all_files):
                        pass
                    else:
                        print("\033[31m{}\033[0m".format("The path does not exist"))
                case "cat":
                    self.cat(self.local_path, command[1], "MyShell.zip")
                case _:
                    print("\033[31m{}\033[0m".format("Don`t know this command"))

            command = input(self.ROOT + ("/" if not self.local_path else self.local_path) + "> ")


if __name__ == '__main__':
    start = VShell("MyShell.zip")
    start.commandProcessing()
