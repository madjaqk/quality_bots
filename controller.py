import collections
import itertools
import json
import subprocess
import random
import re

NUMBER_REGEX = re.compile(r"\d+")

def play_game(bots):
	random.shuffle(bots)

	players = {idx: {"name": bot, "quality": idx+1, "alive": True, "path": paths[bot], "score": 0, "id": idx} for idx, bot in enumerate(bots)}

	remaining_score = int(len(players)*(len(players)+1)/2)

	"""
	test = subprocess.check_output("ruby ./bots/bully.rb 16")

	print("Function output: {}".format(test))
	"""
	# print(players)

	data = {"players": players, "log": []}

	for turn in range(len(players)-1):
		# print("Turn {}".format(turn))

		with open("data.json", "w+") as f:
			json.dump(data, f, indent="\t")

		votes = {}

		for idx, player in data["players"].items():
			if not player["alive"]:
				continue

			# print("Invoking bot #{} ({})".format(idx, player["name"]))
			
			ans = str(subprocess.check_output("{} {}".format(player["path"], idx)))
			ans = int(NUMBER_REGEX.search(ans).group())

			# print("Found number {} in response".format(ans))
			
			if ans in data["players"] and data["players"][ans]["alive"]:
				votes[idx] = ans
			else:
				votes[idx] = idx

			# print("***")

		# print("Votes: {}".format(votes))
		c = collections.Counter(votes.values())
		# print(c)
		voted_off = max(c, key=lambda x: (c[x], -data["players"][x]["quality"]))

		data["players"][voted_off]["alive"] = False
		remaining_score -= data["players"][voted_off]["quality"]

		for player in data["players"]:
			if data["players"][player]["alive"]:
				data["players"][player]["score"] += remaining_score

		data["log"].append(votes)
		# print(data)
	# print(data["players"])
	# print([player for player in data["players"].values() if player["alive"] ])

	for player in data["players"]:
		if data["players"][player]["alive"]:
			data["players"][player]["score"] += len(players)

	with open("data.json", "w+") as f:
			json.dump(data, f, indent="\t")

	return [{"name": player["name"], "score": player["score"]} for player in data["players"].values()]


paths = {
	"rando": "python ./bots/rando.py",
	"scrub": "node ./bots/scrub.js",
	"bully": "ruby ./bots/bully.rb",
	"mope": "python ./bots/mope.py",
}

bots = []

while len(bots) < 8:
	bots.extend(list(paths.keys()))

random.shuffle(bots)

scores = collections.defaultdict(int)

TOTAL_GAMES = 1000
# games_played = 1

# for bot_perm in itertools.permutations(bots):
for game in range(TOTAL_GAMES):
	print("---GAME {}---".format(game+1))
	res = play_game(bots)

	# print(res)

	for player in res:
		scores[player["name"]] += player["score"]

	# games_played += 1
	# if games_played > TOTAL_GAMES: break

print(sorted(scores.items(), key=lambda x: -x[1]))
