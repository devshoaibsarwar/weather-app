function getCachedWeather(showAll, formData, primaryKey) {
  const dbPromise = window.indexedDB.open(INDEX_DB_NAME, 1);

  return new Promise((resolve, reject) => {
    dbPromise.onupgradeneeded = function (event) {
      const db = event.target.result;
      // Create the object store if it doesn't exist
      if (!db.objectStoreNames.contains("weatherData")) {
        db.createObjectStore("weatherData", {
          keyPath: "id",
          autoIncrement: true,
        });
      }
    };

    dbPromise.onsuccess = function (event) {
      const db = event.target.result;
      // Create the object store if it doesn't exist
      if (!db.objectStoreNames.contains("weatherData")) {
        resolve(null)
      } else {  
        const transaction = db.transaction("weatherData", "readonly");
        const store = transaction.objectStore("weatherData");
        let query = store.getAll();
        
        if ((formData && !showAll) || primaryKey) {
          // Create a key based on form data
          const key = getStorageKey(formData);
          query = store.get(primaryKey || key);
        }
        
        query.onsuccess = function () {
          if (query.result) {
            // Parse the stored JSON data back into JavaScript objects
            if (showAll && !formData) {
              const weatherData = query.result.map((item) => {
                // Parse the 'data' field and assign the parsed value back to the object
                return {
                  timestamp: item.timestamp,
                  weatherData: JSON.parse(item.weatherData),
                };
              });
              
              resolve(weatherData);
            }
            
            if (formData || primaryKey) {
              resolve({
                weatherData: JSON.parse(query.result.weatherData),
                timestamp: query.result.timestamp,
              });
            }
          } else {
            resolve(null);
          }
        };
        
        transaction.oncomplete = function () {
          db.close();
        };
      }
    };

    dbPromise.onerror = function (event) {
      console.log("[ERROR] opening indexedDB:", event.target.error);
      reject(event.target.error);
    };
  });
}

function cacheWeatherData(formData, weatherData, cachedTime) {
  const dbPromise = window.indexedDB.open(INDEX_DB_NAME, 1);

  dbPromise.onsuccess = function (event) {
    const db = event.target.result;
    const transaction = db.transaction("weatherData", "readwrite");
    const store = transaction.objectStore("weatherData");
    console.log("[DEBUG] Adding to DB", typeof weatherData);

    // Create a key based on form data
    let timestamp = Date.now();
    if (cachedTime) {
      timestamp = cachedTime;
    }

    const key = getStorageKey(formData);
    store.add({
      id: key,
      formData: JSON.stringify(formData),
      weatherData: JSON.stringify(weatherData),
      timestamp,
    });

    transaction.oncomplete = function () {
      console.log("[DEBUG] Compete, DB close");
      db.close();
    };
  };

  dbPromise.onerror = function (event) {
    console.log("[ERROR] opening indexedDB:", event.target.error);
  };
}
