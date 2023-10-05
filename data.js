const fs = require("fs");
const data = require("./dataset.json");

const unique = {};

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
});

fs.writeFileSync('filteredDataset.json', JSON.stringify(data));
console.log(Object.keys(unique).length);
console.log(data.length);
