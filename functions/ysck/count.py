def count(data: dict):
    """

    生成各种星级的武器/角色数量

    Args:
      data(dict): 获取的data

    Returns:
      count，可使用count(xxx)["x星xx"]来访问

    """
    count = {"5星角色": 0, "5星武器": 0, "3星武器": 0, "3星武器": 0, "4星角色": 0, "3星角色": 0}
    for i in data["list"]:
        count[i["rank_type"] + "星" + i["item_type"]] += 1

    return count
