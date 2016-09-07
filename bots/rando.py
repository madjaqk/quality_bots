import json
import random
import sys

"""Chooses who to vote against at random (not counting itself)"""


my_num = sys.argv[1]

with open("data.json") as f:
	data = json.load(f)

# print("Here's the data dict", data)

targets = [i for i in data["players"] if i != my_num and data["players"][i]["alive"]]

print("I'm voting against: {}".format(random.choice(targets)))