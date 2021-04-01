def count(data: dict):
    count = {"5星角色": 0, "5星武器": 0, "3星武器": 0, "3星武器": 0, "4星角色": 0, "3星角色": 0}
    for i in data["list"]:
        count[i["rank_type"] + "星" + i["item_type"]] += 1

    return count
