import os
import glob


def get_all_package_name(path: str) -> list[str]:
    def is_package(d: str):
        d = os.path.join(path, d)
        return os.path.isdir(d) and glob.glob(os.path.join(d, "__init__.py"))
    return list(filter(is_package, os.listdir(path)))
