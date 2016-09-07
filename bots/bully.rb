require 'json'

# Always votes for the bot with the lowest quality

f = File.read("data.json")
data = JSON.parse(f)

# puts ARGV[0]
# puts data["players"].values.select {|player| player["alive"] && player["id"] != ARGV[0].to_i }
voting_against = data["players"].values.select {|player| player["alive"] && player["id"] != ARGV[0].to_i }.min_by { |player| player["quality"] }

puts "I'm voting against #{voting_against["id"]}"