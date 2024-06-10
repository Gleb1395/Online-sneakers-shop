document.addEventListener("DOMContentLoaded", function() {
    const rangeInputs = document.querySelectorAll(".range-input input");
    const priceInputs = document.querySelectorAll(".price-input input");
    const priceSlider = document.getElementById("price-slider");

    // Set the price gap
    let priceGap = 500;

    // Add event listeners to price input elements
    priceInputs.forEach((input, index) => {
        input.addEventListener("input", (e) => {
            let minPrice = parseInt(priceInputs[0].value);
            let maxPrice = parseInt(priceInputs[1].value);

            if (minPrice < 0) {
                alert("Minimum price cannot be less than 0");
                priceInputs[0].value = 0;
                minPrice = 0;
            }

            if (maxPrice > 10000) {
                alert("Maximum price cannot be greater than 10000");
                priceInputs[1].value = 10000;
                maxPrice = 10000;
            }

            if (minPrice > maxPrice - priceGap) {
                if (index === 0) {
                    priceInputs[0].value = maxPrice - priceGap;
                    minPrice = maxPrice - priceGap;
                } else {
                    priceInputs[1].value = minPrice + priceGap;
                    maxPrice = minPrice + priceGap;
                }
            }

            rangeInputs[0].value = minPrice;
            rangeInputs[1].value = maxPrice;

            updateSlider();
        });
    });

    // Add event listeners to range input elements
    rangeInputs.forEach((input) => {
        input.addEventListener("input", (e) => {
            let minVal = parseInt(rangeInputs[0].value);
            let maxVal = parseInt(rangeInputs[1].value);

            if ((maxVal - minVal) < priceGap) {
                if (e.target.className === "min-range") {
                    rangeInputs[0].value = maxVal - priceGap;
                } else {
                    rangeInputs[1].value = minVal + priceGap;
                }
            } else {
                priceInputs[0].value = minVal;
                priceInputs[1].value = maxVal;

                updateSlider();
            }
        });
    });

    function updateSlider() {
        let minVal = parseInt(rangeInputs[0].value);
        let maxVal = parseInt(rangeInputs[1].value);
        let maxRange = parseInt(rangeInputs[1].max);

        priceSlider.style.left = ((minVal / maxRange) * 100) + "%";
        priceSlider.style.right = (100 - (maxVal / maxRange) * 100) + "%";
    }

    updateSlider();
});
