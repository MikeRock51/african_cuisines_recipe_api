const fs = require("fs");
const data = require("./dataset.json");

const unique = {};
const filtered = [];

data.forEach((recipe, index) => {
  recipe.name = recipe.recipe_name
  delete recipe.recipe_name
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
