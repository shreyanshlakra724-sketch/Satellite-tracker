from re import search

from skyfield.api import load 
import math 



url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
satellites = load.tle_file(url)


sat_name = input("Enter the satellite name/ Norad ID you want to track:").strip().upper()

found = None 

for a in satellites:
    if sat_name in a.name.upper() or sat_name == str(a.norad_id):
        found = a
        break
    
    if search.isdigit():
        if int(search) == a.norad_id:
            found = a
            break
        

if found is None:
    print("Satellite not found.")
    exit()

ts=load.timescale()
t=ts.now()


subpoint = found.at(t).subpoint()

velocity = found.at(t).velocity.km_per_s

actual_velocity = math.sqrt(
    velocity[0]**2 +
    velocity[1]**2 +
    velocity[2]**2
) #the velocity that we are retrieving from the satellite is a vector quantity hence, we find it's magnitude.

print(f'Tracking satellite: {found.name} (NORAD ID: {found.norad_id})')
print(f"Satellite: {found.name}")
print(f"Latitude: {subpoint.latitude.degrees:.6f}°")
print(f"Longitude: {subpoint.longitude.degrees:.6f}°")
print(f"Altitude: {subpoint.elevation.m:.2f} meters")
print(f"Distance from Earth's surface: {found.at(t).distance().km - 6371:.2f} km")
print(f"Actual Velocity: {actual_velocity:.2f} km/s")
