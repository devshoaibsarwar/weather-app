async function fetchWeatherData(formData) {
  const cachedData = await getCachedWeather(false, formData);

  if (cachedData && !isCacheExpired(cachedData.timestamp)) {
    console.log("[DEBUG] Returning from cache");
    return {
      status: "SUCCESS",
      data: cachedData.weatherData,
      timestamp: cachedData.timestamp,
    };
  }

  try {
    const response = await fetch(submitURL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(formData),
    });

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("[ERROR] ", error);
    return null;
  }
}

async function submitWeatherForm() {
  clearErrors();
  displayGlobalErrors("", false);

  const form = document.getElementById("weather-form");
  const formData = {
    longitude: form.querySelector("#id_longitude").value,
    latitude: form.querySelector("#id_latitude").value,
    forecast_type: form.querySelector("#id_forecast_type").value,
  };
  const weatherData = await fetchWeatherData(formData);

  if (weatherData.status === "SUCCESS") {
    cacheWeatherData(formData, weatherData.data, weatherData.timestamp);
    displayWeatherData(weatherData.data[0]);
    preloadRecentRequest();
  }

  if (weatherData.status === "ERROR") {
    if (weatherData.errors.hasOwnProperty("__all__")) {
      displayGlobalErrors(weatherData.errors["__all__"], true);
    } else {
      displayValidationErrors(weatherData.errors);
    }
  }
}

async function preloadRecentRequest() {
  const weatherData = await getCachedWeather(true);

  if (weatherData?.length) {
    displayWeatherTable(weatherData);
  }
}
