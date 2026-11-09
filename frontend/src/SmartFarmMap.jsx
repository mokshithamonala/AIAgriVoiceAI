import React, { useEffect, useRef, useState } from "react";
import {
  MapPin,
  Layers,
  Navigation,
  Plus,
  Sprout,
  Droplets,
  ShieldCheck,
  AlertTriangle,
  Sparkles,
  Volume2,
  Trash2,
} from "lucide-react";

export default function SmartFarmMap({
  zones = [],
  nearbyResources = [],
  selectedZoneId,
  onSelectZone,
  onAddZone,
  onDeleteZone,
  onExplainZone,
  explainData,
  explainLoading,
  onAskAssistant,
  onSpeakText,
}) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const layerGroupRef = useRef(null);
  const tileLayerRef = useRef(null);

  const [mapStyle, setMapStyle] = useState("street"); // "street" | "satellite"
  const [showResources, setShowResources] = useState(true);
  const [showBoundaries, setShowBoundaries] = useState(true);
  const [pickedCoords, setPickedCoords] = useState({ lat: 16.3067, lng: 80.4365 });
  const [showNewZoneForm, setShowNewZoneForm] = useState(false);
  const [newZone, setNewZone] = useState({
    name: "Zone E – West Plot",
    crop: "Groundnut",
    area_acres: 1.5,
    stage: "Vegetative",
    soil_type: "Red Sandy Loam",
    soil_ph: 6.6,
    moisture_pct: 64,
    irrigation_status: "Scheduled",
  });

  const activeZone =
    zones.find((z) => z.id === selectedZoneId) || zones[0] || null;

  // Initialize Leaflet Map
  useEffect(() => {
    const L = window.L;
    if (!L || !mapContainerRef.current || mapInstanceRef.current) return;

    const initialLat = activeZone?.lat || 16.3067;
    const initialLng = activeZone?.lng || 80.4365;

    const map = L.map(mapContainerRef.current, {
      center: [initialLat, initialLng],
      zoom: 16,
      scrollWheelZoom: false,
    });

    const streetTiles = L.tileLayer(
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors",
      }
    );
    streetTiles.addTo(map);
    tileLayerRef.current = streetTiles;

    const group = L.layerGroup().addTo(map);
    layerGroupRef.current = group;

    map.on("click", (e) => {
      const { lat, lng } = e.latlng;
      setPickedCoords({
        lat: Number(lat.toFixed(5)),
        lng: Number(lng.toFixed(5)),
      });
    });

    mapInstanceRef.current = map;

    setTimeout(() => {
      map.invalidateSize();
    }, 250);

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // Switch between OpenStreetMap Street and Esri World Imagery Satellite
  useEffect(() => {
    const L = window.L;
    const map = mapInstanceRef.current;
    if (!L || !map) return;

    if (tileLayerRef.current) {
      map.removeLayer(tileLayerRef.current);
    }

    if (mapStyle === "satellite") {
      tileLayerRef.current = L.tileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        {
          maxZoom: 19,
          attribution: "Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics",
        }
      ).addTo(map);
    } else {
      tileLayerRef.current = L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
          maxZoom: 19,
          attribution: "© OpenStreetMap contributors",
        }
      ).addTo(map);
    }
  }, [mapStyle]);

  // Render Farm Zone Polygons, Markers & Nearby Agricultural Resources
  useEffect(() => {
    const L = window.L;
    const map = mapInstanceRef.current;
    const group = layerGroupRef.current;
    if (!L || !map || !group) return;

    group.clearLayers();

    zones.forEach((zone) => {
      const isHealthy = zone.health_status === "Healthy";
      const isSelected = activeZone && activeZone.id === zone.id;
      const color = isHealthy ? "#23834D" : "#E8A83E";

      if (showBoundaries) {
        const delta = Math.max(0.0006, Math.sqrt(zone.area_acres || 1) * 0.00055);
        const bounds = [
          [zone.lat - delta, zone.lng - delta * 1.2],
          [zone.lat + delta, zone.lng + delta * 1.2],
        ];
        const rect = L.rectangle(bounds, {
          color: isSelected ? "#123B2A" : color,
          weight: isSelected ? 3 : 2,
          fillColor: color,
          fillOpacity: isSelected ? 0.42 : 0.25,
        });
        rect.on("click", () => {
          onSelectZone(zone.id);
        });
        rect.bindTooltip(
          `<strong>${zone.name}</strong><br/>${zone.crop} · ${zone.moisture_pct}% Moisture`,
          { sticky: true }
        );
        rect.addTo(group);
      }

      const badgeHtml = `
        <div style="
          background:${isHealthy ? "#123B2A" : "#92400e"};
          color:#fff;
          padding:4px 9px;
          border-radius:999px;
          font-size:11px;
          font-weight:700;
          white-space:nowrap;
          border:2px solid #fff;
          box-shadow:0 3px 10px rgba(0,0,0,0.25);
        ">
          🌱 ${zone.name.split("–")[0].trim()}: ${zone.crop.split("(")[0].trim()}
        </div>
      `;
      const icon = L.divIcon({
        html: badgeHtml,
        className: "custom-farm-pin",
        iconSize: [120, 26],
        iconAnchor: [60, 13],
      });
      const marker = L.marker([zone.lat, zone.lng], { icon });
      marker.on("click", () => onSelectZone(zone.id));
      marker.addTo(group);
    });

    if (showResources) {
      nearbyResources.forEach((res) => {
        const resIcon = L.divIcon({
          html: `<div style="
            background:#ffffff;
            color:#123B2A;
            padding:3px 8px;
            border-radius:8px;
            font-size:10px;
            font-weight:700;
            border:1.5px solid #23834D;
            white-space:nowrap;
            box-shadow:0 2px 8px rgba(0,0,0,0.18);
          ">🏛️ ${res.type} (${res.distance_km} km)</div>`,
          className: "custom-res-pin",
          iconSize: [130, 22],
          iconAnchor: [65, 11],
        });
        L.marker([res.lat, res.lng], { icon: resIcon })
          .bindPopup(
            `<b>${res.name}</b><br/><small>${res.services}</small><br/><b>Helpline:</b> ${res.phone}`
          )
          .addTo(group);
      });
    }
  }, [zones, nearbyResources, activeZone, showBoundaries, showResources]);

  function handleLocateMe() {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = Number(pos.coords.latitude.toFixed(5));
        const lng = Number(pos.coords.longitude.toFixed(5));
        setPickedCoords({ lat, lng });
        if (mapInstanceRef.current) {
          mapInstanceRef.current.setView([lat, lng], 15);
        }
      },
      () => {
        // Focus default farm center if geolocation denied
        if (mapInstanceRef.current && activeZone) {
          mapInstanceRef.current.setView([activeZone.lat, activeZone.lng], 16);
        }
      }
    );
  }

  function focusZoneOnMap(zone) {
    onSelectZone(zone.id);
    if (mapInstanceRef.current) {
      mapInstanceRef.current.setView([zone.lat, zone.lng], 16);
    }
  }

  function handleCreateZoneSubmit(e) {
    e.preventDefault();
    onAddZone({
      ...newZone,
      lat: pickedCoords.lat,
      lng: pickedCoords.lng,
    });
    setShowNewZoneForm(false);
  }

  return (
    <div className="smart-map-module">
      {/* Map Controls Toolbar */}
      <div className="map-toolbar-card">
        <div className="map-toolbar-left">
          <button
            type="button"
            className={`map-layer-btn ${mapStyle === "street" ? "active" : ""}`}
            onClick={() => setMapStyle("street")}
          >
            <Layers size={15} />
            <span>OpenStreetMap</span>
          </button>
          <button
            type="button"
            className={`map-layer-btn ${mapStyle === "satellite" ? "active" : ""}`}
            onClick={() => setMapStyle("satellite")}
          >
            <Layers size={15} />
            <span>Satellite View</span>
          </button>
          <button
            type="button"
            className={`map-layer-btn ${showBoundaries ? "active" : ""}`}
            onClick={() => setShowBoundaries((v) => !v)}
          >
            <Sprout size={15} />
            <span>Field Boundaries</span>
          </button>
          <button
            type="button"
            className={`map-layer-btn ${showResources ? "active" : ""}`}
            onClick={() => setShowResources((v) => !v)}
          >
            <MapPin size={15} />
            <span>Nearby KVK &amp; Mandis</span>
          </button>
        </div>

        <div className="map-toolbar-right">
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={handleLocateMe}
          >
            <Navigation size={15} />
            <span>My GPS Location</span>
          </button>
          <button
            type="button"
            className="btn btn-primary btn-sm"
            onClick={() => setShowNewZoneForm((v) => !v)}
          >
            <Plus size={15} />
            <span>Add Farm Zone</span>
          </button>
        </div>
      </div>

      {/* Add New Farm Zone Drawer */}
      {showNewZoneForm && (
        <form className="new-zone-form-card" onSubmit={handleCreateZoneSubmit}>
          <div className="new-zone-head">
            <h4>Register New Field Zone on Map</h4>
            <span className="coords-pill">
              Selected Coords: {pickedCoords.lat}, {pickedCoords.lng} (Click anywhere on map to move)
            </span>
          </div>
          <div className="new-zone-grid">
            <label>
              <span>Zone Name</span>
              <input
                type="text"
                value={newZone.name}
                onChange={(e) => setNewZone({ ...newZone, name: e.target.value })}
                required
              />
            </label>
            <label>
              <span>Crop Name</span>
              <input
                type="text"
                value={newZone.crop}
                onChange={(e) => setNewZone({ ...newZone, crop: e.target.value })}
                required
              />
            </label>
            <label>
              <span>Area (Acres)</span>
              <input
                type="number"
                step="0.1"
                min="0.1"
                value={newZone.area_acres}
                onChange={(e) =>
                  setNewZone({ ...newZone, area_acres: parseFloat(e.target.value) || 1.0 })
                }
                required
              />
            </label>
            <label>
              <span>Soil Type</span>
              <select
                value={newZone.soil_type}
                onChange={(e) => setNewZone({ ...newZone, soil_type: e.target.value })}
              >
                <option>Red Sandy Loam</option>
                <option>Alluvial Clay Loam</option>
                <option>Black Cotton Soil</option>
                <option>Enriched Loam</option>
              </select>
            </label>
            <label>
              <span>Estimated Soil Moisture (%)</span>
              <input
                type="number"
                min="15"
                max="95"
                value={newZone.moisture_pct}
                onChange={(e) =>
                  setNewZone({ ...newZone, moisture_pct: parseInt(e.target.value, 10) || 60 })
                }
              />
            </label>
          </div>
          <div className="new-zone-actions">
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => setShowNewZoneForm(false)}
            >
              Cancel
            </button>
            <button type="submit" className="btn btn-primary btn-sm">
              Save Zone to Digital Twin
            </button>
          </div>
        </form>
      )}

      {/* Main Interactive Map + Selected Zone Inspector */}
      <div className="map-split-layout">
        <div className="leaflet-map-wrapper">
          <div
            ref={mapContainerRef}
            className="leaflet-map-canvas"
            aria-label="Interactive Smart Farm Map"
          />
          <div className="map-caption-bar">
            <span>
              <strong>Interactive OpenStreetMap &amp; Satellite View</strong> · Click any
              field zone polygon to inspect crop health or click on the map to set
              coordinates.
            </span>
            <span className="demo-badge">Demonstration &amp; Farmer-Entered Data</span>
          </div>
        </div>

        {/* Selected Field Zone Inspector Panel */}
        {activeZone && (
          <aside className="zone-inspector-card">
            <div className="inspector-header">
              <div>
                <span className="inspector-eyebrow">SELECTED FIELD ZONE</span>
                <h3>{activeZone.name}</h3>
              </div>
              <span
                className={`health-pill ${
                  activeZone.health_status === "Healthy" ? "healthy" : "attention"
                }`}
              >
                {activeZone.health_status === "Healthy" ? (
                  <ShieldCheck size={14} />
                ) : (
                  <AlertTriangle size={14} />
                )}
                {activeZone.health_status}
              </span>
            </div>

            <div className="inspector-metrics-grid">
              <div className="inspector-metric">
                <small>Crop &amp; Variety</small>
                <strong>{activeZone.crop}</strong>
              </div>
              <div className="inspector-metric">
                <small>Field Area</small>
                <strong>{activeZone.area_acres} Acres</strong>
              </div>
              <div className="inspector-metric">
                <small>Growth Stage</small>
                <strong>{activeZone.stage}</strong>
              </div>
              <div className="inspector-metric">
                <small>Sowing Date</small>
                <strong>{activeZone.sowing_date}</strong>
              </div>
              <div className="inspector-metric">
                <small>Soil Type &amp; pH</small>
                <strong>
                  {activeZone.soil_type} (pH {activeZone.soil_ph})
                </strong>
              </div>
              <div className="inspector-metric">
                <small>Soil Moisture (Est.)</small>
                <strong>
                  <Droplets size={14} /> {activeZone.moisture_pct}%
                </strong>
              </div>
            </div>

            <div className="inspector-recommendation-box">
              <h4>
                <Sparkles size={15} /> Field-Specific AI Recommendation
              </h4>
              <p>{activeZone.recommendation}</p>
              <small>Irrigation Status: {activeZone.irrigation_status}</small>
            </div>

            <div className="inspector-actions">
              <button
                type="button"
                className="btn btn-primary full-width"
                onClick={() => onExplainZone(activeZone.id)}
                disabled={explainLoading}
              >
                <Sparkles size={16} />
                {explainLoading
                  ? "Analyzing Zone..."
                  : "AI Explain What Is Happening in This Zone"}
              </button>

              <div className="inspector-sub-actions">
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={() =>
                    onAskAssistant(
                      `My ${activeZone.crop} in ${activeZone.name} is at ${activeZone.stage} stage with ${activeZone.moisture_pct}% moisture. What care should I take this week?`
                    )
                  }
                >
                  Ask Voice Assistant
                </button>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={() =>
                    onSpeakText(
                      `${activeZone.name}, growing ${activeZone.crop}. Health status is ${activeZone.health_status}. ${activeZone.recommendation}`
                    )
                  }
                >
                  <Volume2 size={14} /> Listen
                </button>
                {zones.length > 1 && (
                  <button
                    type="button"
                    className="btn-icon-danger"
                    title="Delete zone"
                    onClick={() => onDeleteZone(activeZone.id)}
                  >
                    <Trash2 size={15} />
                  </button>
                )}
              </div>
            </div>

            {explainData && explainData.zone?.id === activeZone.id && (
              <div className="ai-explain-box">
                <strong>AI Zone Summary:</strong>
                <p>{explainData.summary}</p>
                {explainData.missing_data?.length > 0 && (
                  <div className="missing-data-note">
                    <b>Missing Data Identified:</b>{" "}
                    {explainData.missing_data.join("; ")}
                  </div>
                )}
              </div>
            )}
          </aside>
        )}
      </div>

      {/* Interactive Digital Twin Zone Selector Cards */}
      <div className="digital-twin-strip">
        <div className="twin-strip-header">
          <div>
            <span className="section-eyebrow">MY FARM — DIGITAL TWIN</span>
            <h3>Registered Field Zones ({zones.length})</h3>
          </div>
          <small>Click any zone card to focus on the map and inspect field health</small>
        </div>

        <div className="twin-zones-grid">
          {zones.map((z) => {
            const isSelected = activeZone?.id === z.id;
            const isHealthy = z.health_status === "Healthy";
            return (
              <button
                key={z.id}
                type="button"
                className={`twin-zone-card ${isSelected ? "selected" : ""}`}
                onClick={() => focusZoneOnMap(z)}
              >
                <div className="twin-zone-top">
                  <strong>{z.name}</strong>
                  <span className={`twin-badge ${isHealthy ? "ok" : "warn"}`}>
                    {z.health_status}
                  </span>
                </div>
                <div className="twin-crop-name">{z.crop}</div>
                <div className="twin-meta-row">
                  <span>{z.area_acres} Acres</span>
                  <span>Moisture: {z.moisture_pct}%</span>
                  <span>pH {z.soil_ph}</span>
                </div>
                <div className="twin-moisture-bar">
                  <div
                    className="twin-moisture-fill"
                    style={{ width: `${Math.min(100, z.moisture_pct)}%` }}
                  />
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Nearby Agricultural Resources Directory */}
      <div className="nearby-resources-panel">
        <h3>Nearby Agricultural Support &amp; Services</h3>
        <div className="resources-grid">
          {nearbyResources.map((res) => (
            <div key={res.id} className="resource-card">
              <div className="resource-type-tag">{res.type}</div>
              <h4>{res.name}</h4>
              <p>{res.services}</p>
              <div className="resource-footer">
                <span>📍 {res.distance_km} km away</span>
                <span>📞 {res.phone}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
