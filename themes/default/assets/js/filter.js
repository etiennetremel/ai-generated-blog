const filterButton = document.getElementById("filter-btn");

filterButton.addEventListener("click", function () {
  const selectElement = document.getElementById("filter-model");
  const selectedValues = Array.from(selectElement.selectedOptions).map(
    (option) => option.value
  );

  const allFilterableItems = document.querySelectorAll("article");

  if (selectedValues.length === 0 || selectedValues[0] === "") {
    allFilterableItems.forEach(item => {
      item.classList.remove("hide");
    });
  } else {
    allFilterableItems.forEach(item => {
      const shouldShow = selectedValues.some(selectedValue => {
        console.log(item.classList);
        return item.classList.contains(selectedValue);
      });

      if (shouldShow) {
        item.classList.remove("hide");
      } else {
        item.classList.add("hide");
      }
    });
  }
});
