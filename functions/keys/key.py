import yaml

def save(path: str):
    key = {
            "fanyi": {
                "appid": "12345678",
                "authKey": "shssksks"
                }
            }
    with open(path,"w") as f:
        f.write(yaml.dump(key))


def read(path: str):
    with open(path, "r") as f:
        n = f.read()
    return yaml.load(n)

if __name__ == "__main__":
    save("config.yaml")
