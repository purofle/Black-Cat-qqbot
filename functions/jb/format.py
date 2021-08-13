from graia.application.group import Group


def format(group: Group, data: dict) -> str:
    data = data[group.id]
    # sorted the data
    data = sorted(data.items(), key=lambda x: x[1])
    # unpack
    result = []
    for i in data:
        result.append(f"{i[0]}：共断了{i[1]}根jb")
    return "\n".join(result)
