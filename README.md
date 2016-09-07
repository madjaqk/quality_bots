# Quality Bots

The game is straightfoward: At the beginning of each game, each player is randomly assigned a quality from 1 to N, where N is the number of player.  Each round, the players vote one player out (simple plurality, and in case of a tie the lowest-quality player loses), and the remaining players each get X points, where X is the sum of the qualities of each living player.  The last living player at the end of the game receives a bonus N points.

The winner is the player with the highest total number of points scored over many games (right now, I'm thinking 500 or 1000, probably).

If you want flavor, the game is like Weakest Link, where the quality is how many trivia questions that player will be able to answer correctly.  Keeping smart people around means the team will win more money, but at some point you'll want to start voting the stronger players off so that you have a better chance to win.

# The Bots

Each bot is called from the command line with a single argument, their ID number for that game.  There's also a `data.json` file that contains every bot's quality score and the history of votes in the current game.  The bot needs to print a number (yes, print, as in to STDOUT) representing its vote.  If you print more than one number, the controller will ignore everything after the first!  The controller program will also ignore any non-numbers you print!

Here are some example bots in Python, Ruby, and Javascript to show how to read the JSON and the command line arguments:

```python
# rando.py

import json
import random
import sys

"""Chooses who to vote against at random (not counting itself)"""

my_num = sys.argv[1]

with open("data.json") as f:
	data = json.load(f)

targets = [i for i in data["players"] if i != my_num and data["players"][i]["alive"]]

print("I'm voting against: {}".format(random.choice(targets)))
```

```ruby
# bully.rb
require 'json'

# Always votes for the bot with the lowest quality

f = File.read("data.json")
data = JSON.parse(f)

voting_against = data["players"].values.select {|player| player["alive"] && player["id"] != ARGV[0].to_i }.min_by { |player| player["quality"] }

puts "I'm voting against #{voting_against["id"]}"
```

```javascript
// scrub.js
// Always votes for the player with the highest quality

var my_num = process.argv[2]

var data = require("../data.json")

max_found = [0, undefined] // Value and index of maximum 

for(var idx in data["players"]){
	if(idx != my_num && data["players"][idx]["alive"] && data["players"][idx]["quality"] > max_found[0]){
		max_found = [data["players"][idx]["quality"], idx]
	}
}

console.log("I'm voting against", max_found[1])
```

Keep in mind that I use Python 3 by default; if your program only works in Python 2 (because you're absuing integer division, maybe), be sure to let me know.

Also: The controller program takes forever to run!  I'm never running another of these contests that accepts multiple languages again.