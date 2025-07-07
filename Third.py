import json
import random
import sys

if len(sys.argv) != 3:
    print("Должно быть передано аргументов: 2 ")
    print("1) номер версии продукта ")
    print("2) имя конфигурационного файла с шаблонами версий ")
    sys.exit()

version = sys.argv[1]
confFile = sys.argv[2]

templates: dict
try:
    with open(confFile, "r") as file:
        content = file.read()
        correctContent = content.replace('{', '{"').replace(':', '":').replace(",", ',"')
        templates = json.loads(correctContent)

    versions = []
    for template in templates.values():
        rand = random.randrange(0, 10)
        versions.append(str(template).replace("*", str(rand)))
        rand = random.randrange(0, 10)
        versions.append(str(template).replace("*", str(rand)))
    versions.sort()
    print("Сгенерированные версии: " + str(versions))
except Exception as e:
    print(f"При чтении файла {confFile} произошла ошибка - {e}")
    sys.exit()

try:
    print(f"Версии старше {version}")
    for item in versions:
        if item < version:
            print(item)

except Exception as e:
    print(f"ошибка при сравнении версий с {version} - {e}")



