import json

from ruamel.yaml import YAML

filename = 'yaml/1.yaml'

yaml = YAML()
with open(filename) as fpi:
    data = yaml.load(fpi)
with open("files/document.json", 'w') as fpo:
    json.dump(data, fpo, indent=2)
