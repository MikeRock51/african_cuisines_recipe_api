const data = require("./dataset.json");

data.recipes.forEach((recipe) => {console.log(recipe.recipe_name)});

console.log(data.recipes.length);
