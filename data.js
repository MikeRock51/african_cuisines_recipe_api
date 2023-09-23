const fs = require('fs');
const data = require("./dataset.json");

const unique = {};
const filter = []


data.recipes.forEach((recipe, index) => {
    // fs.appendFileSync('test.json', `${index + 1}. ${recipe.recipe_name}\n`);
    // console.log(recipe.recipe_name)

    // console.log(recipe.recipe_name)
    if (unique.hasOwnProperty(recipe.recipe_name)) {
        unique[recipe.recipe_name] += 1
    } else {
        unique[recipe.recipe_name] = 1
    }
});



// console.log(unique);
// console.log(Object.keys(unique).length);
// console.log(data.recipes.length);
