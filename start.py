from datetime import datetime
import requests 
from skyfield.api import load 
import math 
import time
import os



url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

satellites = load.tle_file(url)


sat_name = input("Enter the satellite name/ Norad ID you want to track:").strip().upper()

found = None 

for a in satellites:
    if sat_name in a.name.upper():
        found = a
        break
    
    if sat_name.isdigit() and int(sat_name) == a.model.satnum:
        found = a
        break
        



if found is None:
    print("Satellite not found.")
    exit()

ts=load.timescale()

try:
    while True:
        t = ts.now()


        subpoint = found.at(t).subpoint()

        velocity = found.at(t).velocity.km_per_s

        actual_velocity_ms = math.sqrt(
        velocity[0]**2 +
        velocity[1]**2 +
        velocity[2]**2
)       #the velocity that we are retrieving from the satellite is a vector quantity hence, we find it's magnitude.

        actual_velocity_kmh = actual_velocity_ms * 3.6 

        print(f'Tracking satellite: {found.name} (NORAD ID: {found.model.satnum})')
        print(f"Latitude: {subpoint.latitude.degrees:.6f}°")
        print(f"Longitude: {subpoint.longitude.degrees:.6f}°")
        print(f"Altitude: {subpoint.elevation.km:.2f} km")
        print(f"Actual Velocity: {actual_velocity_kmh:.2f} km/h")
        print(f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")


        time.sleep(1)
except KeyboardInterrupt:
    print("\nTracking stopped.")
    exit()
