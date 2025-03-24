let map;
let markers = {};
let vehicleData = {};

function initMap() {
  console.log("[initMap] Initializing map...");

  const mapOptions = {
    center: { lat: 51.5074, lng: -0.1278 },
    zoom: 12,
    mapId: "bcf0a696868cd64"
  };

  map = new google.maps.Map(document.getElementById("map"), mapOptions);
  console.log("[initMap] Map initialized.");

  // Load initial data from /api/initial-data
  loadInitialData();

  // Establish Socket.IO connection
  const socket = io.connect(window.location.origin);
  console.log("[initMap] Socket.IO attempting to connect to:", window.location.origin);

  // Listen for vehicle updates
  socket.on("vehicle_update", async (data) => {
    console.log("[socket.on('vehicle_update')] Received vehicle update:", data);
    await handleVehicleUpdates(data);
  });
}

async function loadInitialData() {
  console.log("[loadInitialData] Fetching initial data...");
  try {
    const response = await fetch("/api/initial-data");
    if (response.ok) {
      const vehicles = await response.json();
      console.log("[loadInitialData] ✅ Initial vehicle data loaded:", vehicles);
      handleVehicleUpdates(vehicles);
    } else {
      console.error("[loadInitialData] ❌ Failed to load initial data:", response.status, response.statusText);
    }
  } catch (error) {
    console.error("[loadInitialData] ❌ Error loading initial data:", error);
  }
}

/**
 * Main handler for incoming vehicle updates.
 * Currently uses the simulation's status field directly.
 * If you want to re-enable model predictions, uncomment the prediction code below.
 */
async function handleVehicleUpdates(vehicles) {
  console.log("[handleVehicleUpdates] Received vehicles array:", vehicles);

  // -----------------------------------------
  // OPTION A: Use the simulation's status directly (no model calls):
  for (let vehicle of vehicles) {
    // Just copy the simulation's status into predicted_status
    vehicle.predicted_status = vehicle.status;
  }

  // -----------------------------------------
  // OPTION B: Re-enable Vertex AI predictions (comment out the above loop and uncomment below):
  //
  // for (let vehicle of vehicles) {
  //   console.log(`[handleVehicleUpdates] Requesting prediction for vehicle ID ${vehicle.id}...`);
  //   const prediction = await getVehiclePrediction(vehicle);
  //   console.log(`[handleVehicleUpdates] Prediction for vehicle ID ${vehicle.id}:`, prediction);
  //   vehicle.predicted_status = prediction === 0 ? "on-time" : "delayed"; 
  // }

  updateVehicleData(vehicles);
}

async function getVehiclePrediction(vehicle) {
  console.log("[getVehiclePrediction] Sending prediction request for:", vehicle);

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        lat: vehicle.lat,
        lng: vehicle.lng,
        speed: vehicle.speed,
        type: vehicle.type
      })
    });

    if (response.ok) {
      const result = await response.json();
      console.log("[getVehiclePrediction] Prediction result:", result);
      return result.prediction;
    } else {
      console.error("[getVehiclePrediction] Prediction request failed:", response.statusText);
      return 0; // fallback to 0 = on-time
    }
  } catch (error) {
    console.error("[getVehiclePrediction] Error in prediction request:", error);
    return 0; // fallback to on-time
  }
}

function updateVehicleData(vehicles) {
  console.log("[updateVehicleData] Updating global vehicle data with:", vehicles);

  vehicles.forEach(vehicle => {
    vehicleData[vehicle.id] = vehicle;
  });

  const allVehicles = Object.values(vehicleData);
  updateMarkers(allVehicles);
  updateVehicleStatusPanel(allVehicles);
  updateNotificationsPanel(allVehicles);
}

function updateMarkers(vehicles) {
  console.log("[updateMarkers] Updating markers for vehicles:", vehicles);

  const currentVehicleIds = new Set();

  vehicles.forEach(vehicle => {
    currentVehicleIds.add(vehicle.id);

    if (!markers[vehicle.id]) {
      const markerImage = {
        url: `/static/images/${vehicle.type}-icon.png`,
        scaledSize: new google.maps.Size(30, 30)
      };

      markers[vehicle.id] = new google.maps.Marker({
        position: { lat: vehicle.lat, lng: vehicle.lng },
        map: map,
        title: `${vehicle.type.charAt(0).toUpperCase() + vehicle.type.slice(1)} ${vehicle.id}`,
        icon: markerImage
      });
      console.log(`[updateMarkers] Created new marker for vehicle ID ${vehicle.id}`);
    } else {
      markers[vehicle.id].setPosition(new google.maps.LatLng(vehicle.lat, vehicle.lng));
      console.log(`[updateMarkers] Moved marker for vehicle ID ${vehicle.id} to (${vehicle.lat}, ${vehicle.lng})`);
    }
  });

  // Remove markers for any vehicle IDs that are no longer present
  for (const id in markers) {
    if (!currentVehicleIds.has(Number(id))) {
      markers[id].setMap(null);
      delete markers[id];
      console.log(`[updateMarkers] Removed marker for vehicle ID ${id}`);
    }
  }
}

function updateVehicleStatusPanel(vehicles) {
  console.log("[updateVehicleStatusPanel] Updating vehicle status panel with:", vehicles);

  const statusPanel = document.getElementById("vehicle-status");
  statusPanel.innerHTML = "";

  vehicles.forEach(vehicle => {
    const statusClass = vehicle.predicted_status === "on-time" ? "status-on-time" : "status-delayed";
    statusPanel.innerHTML += `
      <div class="vehicle-status-entry ${statusClass}">
        <p>
          <img src="/static/images/${vehicle.type}-icon.png" class="vehicle-icon">
          <strong>${vehicle.type.charAt(0).toUpperCase() + vehicle.type.slice(1)} ${vehicle.id}:</strong> 
          <span>Predicted Status: ${vehicle.predicted_status}</span><br>
          <span>Speed: ${vehicle.speed} km/h</span>
        </p>
      </div>
    `;
  });
}

function updateNotificationsPanel(vehicles) {
  console.log("[updateNotificationsPanel] Updating notifications with vehicles:", vehicles);

  const notificationsPanel = document.getElementById("notifications");
  const delayedVehicles = vehicles.filter(vehicle => vehicle.predicted_status === "delayed");

  if (delayedVehicles.length === 0) {
    notificationsPanel.innerHTML = `
      <div class="notification-panel">
        <div class="notification-text">All vehicles are running on time.</div>
      </div>
    `;
    console.log("[updateNotificationsPanel] No delayed vehicles; showing 'on time' message.");
    return;
  }

  let groupedVehicles = delayedVehicles.reduce((acc, vehicle) => {
    if (!acc[vehicle.type]) acc[vehicle.type] = [];
    acc[vehicle.type].push(vehicle.id);
    return acc;
  }, {});

  let notificationContent = Object.entries(groupedVehicles).map(([type, ids]) => `
    <div class="notification-group">
      <strong>${type.charAt(0).toUpperCase() + type.slice(1)}s (${ids.length} delayed):</strong>
      <p>${ids.join(", ")}</p>
    </div>
  `).join("");

  notificationsPanel.innerHTML = `
    <div class="notification-panel">
      <div class="notification-text">${delayedVehicles.length} vehicle(s) delayed:</div>
      ${notificationContent}
    </div>
  `;
  console.log("[updateNotificationsPanel] Delayed vehicles found; updated notification panel.");
}

window.onload = initMap;
