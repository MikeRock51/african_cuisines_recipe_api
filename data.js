const fs = require("fs");
const data = require("./dataset.json");

const unique = {};
const filtered = [];

data.forEach((recipe, index) => {
  if (recipe.total_time_hours) {
    recipe.total_time_minutes = recipe.total_time_hours * 60
    delete recipe.total_time_hours
  }
  if (recipe.prep_time_hours) {
    recipe.prep_time_minutes = recipe.prep_time_hours * 60
    delete recipe.prep_time_hours
  }
  if (recipe.cook_time_hours) {
    recipe.cook_time_minutes = recipe.cook_time_hours * 60
    delete recipe.cook_time_hours
  }

  // if (unique.hasOwnProperty(recipe.recipe_name)) {
  //   unique[recipe.recipe_name] += 1;
  // } else {
  //   unique[recipe.recipe_name] = 1;
  //   filtered.push(recipe);
  // }
});
fs.writeFileSync('filteredDataset.json', JSON.stringify(data));
// console.log(data[0]);

// fs.writeFileSync('filteredDataset.json', JSON.stringify(filtered));
// console.log(filtered.length);

console.log(Object.keys(unique).length);
// console.log(unique);
// Object.keys(unique).forEach((food, index) => {
//     fs.appendFileSync('foodNames.txt', `${index + 1}. ${food}\n`);
// });
console.log(data.length);
