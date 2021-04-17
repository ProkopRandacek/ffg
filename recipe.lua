#!/usr/bin/lua
luna = require 'lunajson'

-- fake data object for the recipe file
data = {table}
-- with fake extend function
function data:extend(table)
	self.table = table
end

-- run the recipes file from factorio. It writes to the data object
require("../factorio-data.base.prototypes.recipe")

-- encode it into a json
local json = luna.encode(data.table)

-- write that json into a file
file = io.open("src/recipe.json", "w+")
io.output(file)
io.write(json)
io.close(file)

