import yaml

def read(path: str):
    with open(path, "r") as f:
        n = f.read()
    return yaml.load(n)

if __name__ == "__main__":
    save("config.yaml")
