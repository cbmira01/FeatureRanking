
devtype_readable = { 
    "1": "DEFAULT",
    "2": "CPU",
    "4": "GPU",
    "8": "ACCELERATOR",
    "16": "CUSTOM",
    }

def discover_platforms():
    with open('../data/datasets.json', 'r') as file:
        datasets_dict = json.load(file)
    return datasets_dict['datasets']