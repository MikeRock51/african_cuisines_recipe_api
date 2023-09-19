const fs = require('fs');
const data = require("./dataset.json");

// data.recipes.forEach((recipe, index) => {
    // recipe.recipe_name === 'Kenyan Maharagwe' && console.log(recipe);
    // fs.appendFileSync('test.json', `${index + 1}. ${recipe.recipe_name}\n`);
    // console.log(recipe.recipe_name)
// });

console.log(data.recipes.length);
