/**
 * Location Form Handler
 * Handles GPS location detection and map interaction for business/product forms
 */

// Global variables
let map;
let marker;
let currentLocation = null;
let userLocationObtained = false;
let mapLocationSelected = false;
let locationPermissionGranted = false;

// Configuration - set from template
let config = {
    latitudeFieldId: null,
    longitudeFieldId: null,
    addressFieldId: null,
    reverseGeocodeUrl: null,
    initialLat: null,
    initialLng: null
};

/**
 * Initialize the location form with configuration
 */
function initLocationForm(options) {
    config = { ...config, ...options };
}

/**
 * Show location status message
 */
function showLocationStatus(message, type = 'info') {
    const statusDiv = document.getElementById('location-status');
    const messageSpan = document.getElementById('location-message');

    if (statusDiv && messageSpan) {
        statusDiv.className = `alert alert-${type}`;
        messageSpan.textContent = message;
        statusDiv.style.display = 'block';

        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => hideLocationStatus(), 5000);
        }
    }
}

/**
 * Hide location status message
 */
function hideLocationStatus() {
    const statusDiv = document.getElementById('location-status');
    if (statusDiv) {
        statusDiv.style.display = 'none';
    }
}

/**
 * Update coordinates and address
 */
function updateCoordinates(lat, lng, source = 'gps') {
    if (source === 'gps') {
        userLocationObtained = true;
    } else if (source === 'map') {
        mapLocationSelected = true;
    }

    const latField = document.getElementById(config.latitudeFieldId);
    const lngField = document.getElementById(config.longitudeFieldId);

    if (latField) latField.value = lat;
    if (lngField) lngField.value = lng;

    currentLocation = { lat, lng };

    // Update map if available
    if (typeof window.updateMapLocation === 'function') {
        window.updateMapLocation(lat, lng);
    } else if (map) {
        updateMapLocation(lat, lng);
    }

    // Update address field
    getAddressFromCoordinates(lat, lng);

    // Show success message
    showLocationStatus(
        `Location ${source === 'gps' ? 'detected' : 'selected'}: ${lat.toFixed(6)}, ${lng.toFixed(6)}`,
        'success'
    );
}

/**
 * Get address from coordinates using Django backend proxy
 */
function getAddressFromCoordinates(lat, lng) {
    const addressField = document.getElementById(config.addressFieldId);
    if (!addressField) return;

    // Show loading state
    addressField.placeholder = 'Getting address...';
    const originalValue = addressField.value;

    if (!config.reverseGeocodeUrl) {
        console.error('Reverse geocode URL not configured');
        addressField.placeholder = 'Address lookup not configured';
        return;
    }

    // Use Django backend proxy to avoid CORS issues
    fetch(`${config.reverseGeocodeUrl}?lat=${lat}&lon=${lng}`)
        .then(response => response.json())
        .then(data => {
            if (data.display_name) {
                addressField.value = data.display_name;
                addressField.placeholder = 'Address auto-filled from location';
            } else if (data.error) {
                console.error('Reverse geocoding error:', data.error);
                addressField.value = originalValue;
                addressField.placeholder = 'Could not get address. Please enter manually.';
                showLocationStatus('Could not retrieve address', 'warning');
            } else {
                addressField.placeholder = 'Address not found';
            }
        })
        .catch(error => {
            console.error('Reverse geocoding failed:', error);
            addressField.value = originalValue;
            addressField.placeholder = 'Could not get address. Please enter manually.';
            showLocationStatus('Error getting address', 'warning');
        });
}

/**
 * Request location permission and get current position
 */
function requestLocationPermission() {
    if (!navigator.geolocation) {
        showLocationStatus('Geolocation is not supported by your browser. Please use the map to select a location.', 'warning');
        return Promise.resolve(false);
    }

    showLocationStatus('Requesting location permission...', 'info');

    return new Promise((resolve) => {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                locationPermissionGranted = true;
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;

                updateCoordinates(lat, lng, 'gps');
                resolve(true);
            },
            function (error) {
                locationPermissionGranted = false;

                let errorMessage = 'GPS access denied';
                if (error.code === error.PERMISSION_DENIED) {
                    errorMessage = '❌ GPS access denied - You can still select a location on the map.';
                } else if (error.code === error.POSITION_UNAVAILABLE) {
                    errorMessage = '❌ GPS information unavailable - Please check your GPS settings or use the map.';
                } else if (error.code === error.TIMEOUT) {
                    errorMessage = '❌ GPS request timed out - Please try again or use the map.';
                }

                showLocationStatus(errorMessage, 'warning');
                resolve(false);
            },
            {
                enableHighAccuracy: true,
                timeout: 15000,
                maximumAge: 300000 // 5 minutes
            }
        );
    });
}

/**
 * Clear location data
 */
function clearLocationData() {
    const latField = document.getElementById(config.latitudeFieldId);
    const lngField = document.getElementById(config.longitudeFieldId);
    const addressField = document.getElementById(config.addressFieldId);

    if (latField) latField.value = '';
    if (lngField) lngField.value = '';

    if (addressField) {
        addressField.value = '';
        addressField.placeholder = 'No location selected';
    }

    currentLocation = null;
    userLocationObtained = false;
    mapLocationSelected = false;
    hideLocationStatus();

    // Clear map marker if exists
    if (map && marker) {
        map.removeLayer(marker);
        marker = null;
    }
}

/**
 * Update map location (for Leaflet maps)
 */
function updateMapLocation(lat, lng) {
    if (!map) return;

    const newLatLng = L.latLng(lat, lng);

    if (marker) {
        marker.setLatLng(newLatLng);
    } else {
        marker = L.marker(newLatLng, {
            draggable: true,
            icon: L.divIcon({
                className: 'location-marker',
                iconSize: [24, 24],
                iconAnchor: [12, 24]
            })
        }).addTo(map);

        marker.on('dragend', function (event) {
            const position = marker.getLatLng();
            updateCoordinates(position.lat, position.lng, 'map');
        });
    }

    map.setView(newLatLng, 15);
}

/**
 * Initialize the Leaflet map
 * Returns a Promise that resolves when map is fully initialized
 */
function initMap() {
    return new Promise((resolve, reject) => {
        const mapElement = document.getElementById('map');
        if (!mapElement) {
            console.error('Map element not found');
            reject(new Error('Map element not found'));
            return;
        }

        // Check if container is visible
        const mapSection = document.getElementById('map-section');
        if (mapSection && mapSection.style.display === 'none') {
            console.warn('Map section is hidden, skipping initialization');
            reject(new Error('Map section is hidden'));
            return;
        }

        // If map is already initialized, just refresh it
        if (map) {
            console.log('Map already exists, invalidating size');
            // Force recalculation of map size with delays
            setTimeout(() => {
                if (map) {
                    map.invalidateSize(true);
                    console.log('Map size invalidated');
                }
            }, 50);
            setTimeout(() => {
                if (map) {
                    map.invalidateSize(true);
                }
            }, 200);
            setTimeout(() => {
                if (map) {
                    map.invalidateSize(true);
                }
            }, 500);
            resolve(map);
            return;
        }

        console.log('Initializing new map instance');

        // Use existing coordinates or default
        const initialLat = parseFloat(document.getElementById(config.latitudeFieldId)?.value) || config.initialLat || 0;
        const initialLng = parseFloat(document.getElementById(config.longitudeFieldId)?.value) || config.initialLng || 0;
        const initialZoom = (initialLat && initialLng && initialLat !== 0 && initialLng !== 0) ? 15 : 2;

        try {
            // Initialize the map - DO NOT set view yet
            map = L.map('map', {
                zoomControl: true,
                scrollWheelZoom: true,
                // Don't set center/zoom initially - wait for tiles to load
            });

            // Add tile layer
            const tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '© OpenStreetMap contributors',
                detectRetina: true
            });

            // Wait for tiles to start loading before setting view
            tileLayer.on('loading', function () {
                console.log('Tiles are loading...');
            });

            tileLayer.on('load', function () {
                console.log('Tiles loaded successfully');
            });

            tileLayer.addTo(map);

            // NOW set the view after tile layer is added
            map.setView([initialLat || 0, initialLng || 0], initialZoom);

            // Add marker if we have coordinates
            if (initialLat && initialLng && initialLat !== 0 && initialLng !== 0) {
                updateMapLocation(initialLat, initialLng);
            }

            // Add click handler to set location
            map.on('click', function (e) {
                updateCoordinates(e.latlng.lat, e.latlng.lng, 'map');
            });

            // Critical: Invalidate size AFTER the map is fully set up
            // Use requestAnimationFrame to ensure DOM has painted
            requestAnimationFrame(() => {
                setTimeout(() => {
                    if (map) {
                        console.log('Invalidating map size - first pass (after frame)');
                        map.invalidateSize(true);
                    }
                }, 0);
            });

            setTimeout(() => {
                if (map) {
                    console.log('Invalidating map size - second pass');
                    map.invalidateSize(true);
                }
            }, 200);

            setTimeout(() => {
                if (map) {
                    console.log('Invalidating map size - third pass');
                    map.invalidateSize(true);
                }
            }, 500);

            // Resolve after final invalidation
            setTimeout(() => {
                if (map) {
                    console.log('Map initialization complete');
                    map.invalidateSize(true);
                    resolve(map);
                } else {
                    reject(new Error('Map initialization failed'));
                }
            }, 600);

        } catch (error) {
            console.error('Error initializing map:', error);
            reject(error);
        }
    });
}

/**
 * Toggle map visibility
 */
async function toggleMap() {
    console.log('toggleMap() called');
    const mapSection = document.getElementById('map-section');
    const toggleBtn = document.getElementById('toggle-map-btn');

    console.log('mapSection:', mapSection);
    console.log('mapSection display:', mapSection?.style.display);

    if (!mapSection) {
        console.error('map-section element not found!');
        return;
    }

    const isVisible = mapSection.style.display !== 'none';
    console.log('isVisible:', isVisible);

    if (isVisible) {
        mapSection.style.display = 'none';
        if (toggleBtn) {
            toggleBtn.innerHTML = '<i class="fas fa-map me-2"></i>Select on Map';
        }
    } else {
        // Make map section visible FIRST
        mapSection.style.display = 'block';
        if (toggleBtn) {
            toggleBtn.innerHTML = '<i class="fas fa-times me-2"></i>Hide Map';
        }

        // Wait for the DOM to fully render the visible container before initializing map
        // This is crucial for Leaflet to calculate correct tile positions
        setTimeout(async () => {
            console.log('Container is now visible, initializing map...');

            try {
                // Wait for map initialization to complete
                await initMap();
                console.log('Map initialized successfully');

                // Now it's safe to perform operations on the map
                // Center on current location if available
                const latField = document.getElementById(config.latitudeFieldId);
                const lngField = document.getElementById(config.longitudeFieldId);

                if (latField?.value && lngField?.value) {
                    const lat = parseFloat(latField.value);
                    const lng = parseFloat(lngField.value);
                    console.log('Centering map on existing coordinates:', lat, lng);
                    if (map) {
                        // Wait a bit more for the map to settle
                        setTimeout(() => {
                            map.setView([lat, lng], 15);
                            updateMapLocation(lat, lng);
                        }, 100);
                    }
                } else if (navigator.geolocation && !locationPermissionGranted) {
                    // Try to get user's location for initial map view
                    console.log('Attempting to get user location for map centering...');
                    navigator.geolocation.getCurrentPosition(
                        function (position) {
                            if (map) {
                                console.log('Centering map on user location');
                                setTimeout(() => {
                                    if (map) {
                                        map.setView([position.coords.latitude, position.coords.longitude], 13);
                                    }
                                }, 100);
                            }
                        },
                        function (error) {
                            console.log('Could not get user location for map centering:', error.message);
                            // Silently fail - map will show default view
                        },
                        {
                            enableHighAccuracy: false,
                            timeout: 5000,
                            maximumAge: 300000
                        }
                    );
                }
            } catch (error) {
                console.error('Failed to initialize map:', error);
                showLocationStatus('Failed to load map. Please refresh the page.', 'danger');
            }
        }, 250); // Increased delay to ensure container is fully rendered
    }
}

/**
 * Initialize event listeners
 */
function initLocationFormListeners() {
    console.log('initLocationFormListeners() called');

    // Get location button
    const getLocationBtn = document.getElementById('get-location-btn');
    console.log('get-location-btn:', getLocationBtn);
    if (getLocationBtn) {
        getLocationBtn.addEventListener('click', function () {
            requestLocationPermission().then(success => {
                if (!success) {
                    // If location permission was denied, show the map as a fallback
                    const mapSection = document.getElementById('map-section');
                    if (mapSection && mapSection.style.display === 'none') {
                        toggleMap();
                    }
                }
            });
        });
        console.log('Event listener attached to get-location-btn');
    }

    // Map toggle button
    const toggleMapBtn = document.getElementById('toggle-map-btn');
    console.log('toggle-map-btn:', toggleMapBtn);
    if (toggleMapBtn) {
        toggleMapBtn.addEventListener('click', toggleMap);
        console.log('Event listener attached to toggle-map-btn');
    } else {
        console.error('toggle-map-btn element not found!');
    }

    // Clear location button
    const clearLocationBtn = document.getElementById('clear-location');
    console.log('clear-location:', clearLocationBtn);
    if (clearLocationBtn) {
        clearLocationBtn.addEventListener('click', clearLocationData);
        console.log('Event listener attached to clear-location');
    }
}

// Auto-initialize on DOM ready if configuration is provided
console.log('document.readyState:', document.readyState);
if (document.readyState === 'loading') {
    console.log('Adding DOMContentLoaded listener');
    document.addEventListener('DOMContentLoaded', initLocationFormListeners);
} else {
    console.log('DOM already loaded, calling initLocationFormListeners immediately');
    initLocationFormListeners();
}
