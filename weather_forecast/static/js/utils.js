function displayWeatherData(data) {
  document.getElementById("weatherData").innerHTML = data.html;
}

function displayGlobalErrors(error, show) {
  const globalErrorBlock = document.getElementById("globalErrors");
  if (show) {
    globalErrorBlock.innerHTML = error;
    globalErrorBlock.classList.remove("d-none");
  } else {
    globalErrorBlock.innerHTML = "";
    globalErrorBlock.classList.add("d-none");
  }
}

function getStorageKey(formData) {
  if (formData) {
    return `${parseFloat(formData.latitude).toFixed(4)}-${parseFloat(
      formData.longitude
    ).toFixed(4)}-${formData.forecast_type}`;
  }
  return null;
}

function isCacheExpired(timestamp) {
  return Date.now() - timestamp > CACHE_EXPIRATION_TIME * 60 * 1000;
}

function displayWeatherTable(weatherData) {
  const table = document.createElement("table");
  table.setAttribute("id", "weather-table");
  table.setAttribute("class", "table table-striped");

  const thead = document.createElement("thead");
  thead.setAttribute("class", "thead-dark");

  const tbody = document.createElement("tbody");
  const headers = [
    "Forecast Time",
    "Longitude",
    "Latitude",
    "Temperature",
    "Description",
    "Visibility",
    "Clouds",
    "Wind Speed",
  ]; // Add more headers as needed

  // Create header row
  const headerRow = thead.insertRow();
  headers.forEach((headerText) => {
    const header = document.createElement("th");
    header.textContent = headerText;
    headerRow.appendChild(header);
  });

  // Append header to table
  table.appendChild(thead);

  // Create data rows
  weatherData.forEach((entry) => {
    const weatherData = entry.weatherData; // Get the 'weatherData' object from each entry

    weatherData.forEach((item) => {
      const row = tbody.insertRow();
      const rowData = [
        `${item.forecast_date} ${item.forecast_time}`,
        item.lon,
        item.lat,
        item.temprature,
        item.weather.description,
        item.visibility,
        item.clouds,
        item.wind_speed,
      ];

      rowData.forEach((value) => {
        const cell = row.insertCell();
        cell.textContent = value;
      });
    });
  });

  // Append tbody to table
  table.appendChild(tbody);

  // Append table to weather-data div
  const weatherTableBlock = document.getElementById("weather-data-block");
  weatherTableBlock.classList.remove("d-none");

  const weatherDataDiv = document.getElementById("weather-table");
  weatherDataDiv.innerHTML = "";
  weatherDataDiv.appendChild(table);

  // Pagination
  const totalRecordsLength = weatherData.reduce(
    (total, entry) => total + entry.weatherData.length,
    0
  );
  const totalRecords = weatherData.reduce(
    (total, entry) => total.concat(entry.weatherData),
    []
  );
  const totalPages = Math.ceil(totalRecordsLength / 10); // 10 records per page

  if (totalRecordsLength > 10) {
    const pagination = document.createElement("ul");
    pagination.setAttribute("class", "pagination");

    for (let i = 1; i <= totalPages; i++) {
      const li = document.createElement("li");
      li.setAttribute("class", "page-item");
      const link = document.createElement("a");
      link.setAttribute("class", "page-link");
      link.textContent = i;

      if (i === 1) {
        link.classList.add("active");
      }

      link.addEventListener("click", () => {
        displayPage(i, totalRecords);
        // Remove "active" class from previously selected link
        const previousActiveLink =
          pagination.querySelector(".page-link.active");
        if (previousActiveLink) {
          previousActiveLink.classList.remove("active");
        }
        // Add "active" class to the clicked link
        link.classList.add("active");
      });
      li.appendChild(link);
      pagination.appendChild(li);
    }

    const weatherTablePagination = document.getElementById(
      "table-pagination-block"
    );
    weatherTablePagination.innerHTML = "";
    weatherTablePagination.appendChild(pagination);
  }

  // Function to display a specific page
  function displayPage(pageNumber, data) {
    tbody.innerHTML = ""; // Clear existing rows
    const startIndex = (pageNumber - 1) * 10;
    const endIndex = pageNumber * 10;
    for (let i = startIndex; i < endIndex && i < totalRecordsLength; i++) {
      const item = data[i];
      const row = tbody.insertRow();
      const rowData = [
        `${item.forecast_date} ${item.forecast_time}`,
        item.lon,
        item.lat,
        `${item.temprature} °C`,
        item.weather.description,
        `${item.visibility} km`,
        `${item.clouds} %`,
        `${item.wind_speed} km/h`,
      ];

      rowData.forEach((value) => {
        const cell = row.insertCell();
        cell.textContent = value;
      });
    }
  }

  // Inital Pagination
  displayPage(1, totalRecords);
}

function displayValidationErrors(errors) {
  // Loop through each error in the errors object
  Object.keys(errors).forEach(function (field) {
    const errorElement = document.getElementById("error_" + field);
    const inputElement = document.getElementById("id_" + field);
    if (inputElement && errorElement) {
      inputElement.classList.add("is-invalid");
      errorElement.innerHTML = errors[field][0]; // Display only the first error message for simplicity
    }
  });
}

function clearErrors() {
  let inputElements = document.querySelectorAll(".form-control");
  let errorElements = document.querySelectorAll(".invalid-feedback");
  inputElements.forEach((item) => {
    item.addEventListener("input", () => {
      item.classList.remove("is-invalid");
    });
  });
  errorElements.forEach((item) => {
    item.addEventListener("input", () => {
      item.innerHTML = "";
    });
  });
}

const currentCardAttr = "data-current-card";
const totalCardsAttr = "data-total-cards";

async function handlePagination(action, key) {
  const paginatorBlock = document.getElementById("pagination-block");
  const currentCard = parseInt(paginatorBlock.getAttribute(currentCardAttr));
  const totalCards = parseInt(paginatorBlock.getAttribute(totalCardsAttr));

  const cachedData = await getCachedWeather(false, false, key);

  if (action === "next" && currentCard <= totalCards) {
    document.getElementById("weatherData").innerHTML =
      cachedData.weatherData[currentCard + 1].html;
  }

  if (action === "back" && currentCard > 0) {
    document.getElementById("weatherData").innerHTML =
      cachedData.weatherData[currentCard - 1].html;
  }

}
