import json
import os
import shutil
import subprocess
import sys
from datetime import datetime

def log(message: str):
    print(str(datetime.now()) + " - " + message)

def deleteDir(path: str, searchedPath: str):
    if (searchedPath in path):
        return
    if os.listdir(path):
        for item in os.listdir(path):
            newPath = os.path.join(path, item).replace("\\", "/")
            if (os.path.isdir(newPath)):
                deleteDir(newPath, searchedPath)
            else:
                try:
                    os.remove(newPath)
                    log(f"Файл {newPath} удален")
                except Exception as e:
                    log(f"Ошибка при удалении файла {path} - {e}")

        if (not os.listdir(path)):
            try:
                shutil.rmtree(path)
                log(f"Каталог {path} удален")
            except Exception as e:
                log(f"Ошибка при удалении каталога {path} - {e}")




if len(sys.argv) != 4:
    log("Аргументы были переданы неправильно. ")
    sys.exit()

repoUrl = sys.argv[1]
path = sys.argv[2]
version = sys.argv[3]
destinationPath = "./repo"

try:
    subprocess.run(['git', 'clone', repoUrl, destinationPath], check=True)
    log("Репозиторий успешно скачан")
except Exception as e:
    log(f"Ошибка при скачивании репозитория: {e}")
    sys.exit()

deleteDir(destinationPath, path)

try:
    with open(os.path.join(destinationPath, path, "version.json").replace("\\", "/"), "w+") as file:
        files = []
        for item in os.listdir(os.path.join(destinationPath, path)):
            if item.endswith(".py") or item.endswith(".js") or item.endswith(".sh"):
                files.append(item)
        data = {"name": "hello world", "version": version, "files": files}
        json.dump(data, file)
        log("Файл version.json успешно создан")
except Exception as e:
    log(f"При создании 'version.json' произошла ошибка - {e}")
    sys.exit()

archiveName = str(path).split('/')[-1] + datetime.now().strftime("%d%m%Y")
archivePath = os.path.join(destinationPath, archiveName)
try:
    shutil.make_archive(
        base_name=archivePath,
        format="zip",
        root_dir=os.path.join(destinationPath, path)
    )
    log("Архив создан")
except Exception as e:
    log("Архив не создан")



