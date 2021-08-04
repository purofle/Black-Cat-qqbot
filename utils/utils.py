import os
import traceback
import glob


def get_all_package_name(path: str) -> list[str]:
    def is_package(d: str):
        d = os.path.join(path, d)
        return os.path.isdir(d) and glob.glob(os.path.join(d, "__init__.py"))

    return list(filter(is_package, os.listdir(path)))


def uncaught_error_handler(cls, ex):
    print("?")
    root = os.getcwd().rsplit(os.sep)[-1]
    print(f"{ex['exception'].__class__.__name__}: {ex['exception']}")
    for i in traceback.extract_tb(ex["exception"].__traceback__):
        obj_name = (
            "bot"
            + i.filename.rstrip(".py").rsplit(root, 1)[1].replace(os.sep, ".")
            + "."
            + i.name
        )
        filename = i.filename.rsplit(os.sep, 1)[1]
        print(f"\nat {obj_name}({filename}:{i.lineno})")
