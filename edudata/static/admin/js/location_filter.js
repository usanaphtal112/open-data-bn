document.addEventListener("DOMContentLoaded", function () {
    function updateDropdown(url, paramName, sourceElement, targetElement) {
        sourceElement.addEventListener("change", function () {
            const selectedValue = this.value;
            if (!selectedValue) {
                targetElement.innerHTML = '<option value="">---------</option>';
                return;
            }

            fetch(`${url}?${paramName}=${selectedValue}`)
                .then(response => response.json())
                .then(data => {
                    targetElement.innerHTML = '<option value="">---------</option>';
                    data.forEach(item => {
                        let option = new Option(item.name, item.code);
                        targetElement.add(option);
                    });
                })
                .catch(error => console.error("Error fetching data:", error));
        });
    }

    const provinceField = document.querySelector("#id_province");
    const districtField = document.querySelector("#id_district");
    const sectorField = document.querySelector("#id_sector");
    const cellField = document.querySelector("#id_cell");
    const villageField = document.querySelector("#id_village");

    if (provinceField && districtField) {
        updateDropdown("/api/v1/edudata/districts/", "province_code", provinceField, districtField);
    }
    if (districtField && sectorField) {
        updateDropdown("/api/v1/edudata/sectors/", "district_code", districtField, sectorField);
    }
    if (sectorField && cellField) {
        updateDropdown("/api/v1/edudata/cells/", "sector_code", sectorField, cellField);
    }
    if (cellField && villageField) {
        updateDropdown("/api/v1/edudata/villages/", "cell_code", cellField, villageField);
    }
});
