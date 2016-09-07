// Always votes for the player with the highest quality

var my_num = process.argv[2]
// console.log("My number is", my_num)

var data = require("../data.json")

max_found = [0, undefined] // Value and index of maximum 

for(var idx in data["players"]){
	if(idx != my_num && data["players"][idx]["alive"] && data["players"][idx]["quality"] > max_found[0]){
		max_found = [data["players"][idx]["quality"], idx]
	}
}

console.log("I'm voting against", max_found[1])