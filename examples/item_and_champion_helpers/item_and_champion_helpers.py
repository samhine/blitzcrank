from blitzcrank import Blitzcrank

b = Blitzcrank("RGAPI-this-doesnt-really-matter","euw1")

champion_id = "222"
champion_name = b.champion.by_id(champion_id)["name"]

item_id = "350"
item_name = b.item.by_id(item_id)["name"]

print(champion_name, item_name)