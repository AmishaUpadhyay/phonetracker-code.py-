import phonenumbers
import csv
import folium
import os
import webbrowser
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode

key ='2349bc5e0f6149c2b529e03f97de3db2'
geo = OpenCageGeocode(key)

map_folder = r"C:\Users\amish\OneDrive\Desktop\phone number tracker\maps"
os.makedirs(map_folder, exist_ok=True)

csv_file = os.path.join(map_folder, "results.csv")
with open(csv_file, mode='w', newline='') as file:
 writer = csv.writer(file)
 writer.writerow(["Phone Number", "Location", "Carrier", "Latitude", "Longitude", "Map File"])


while True:
    number = input("Enter phone number with country code (or 'exit' to stop):")
    if number.lower() == "exit":
        break

    try:
        pepnumber = phonenumbers.parse(number)
        location = geocoder.description_for_number(pepnumber, "en")
        sim = carrier.name_for_number(pepnumber, "en")
        print(f"Location: {location}")
        print(f"Carrier: {sim}")

        results = geo.geocode(location)

        if results:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            print(f"Coordinates: {lat}, {lng}")

            safe_number = number.replace("+", "").replace(" ", "")
            map_file = os.path.join(map_folder, f"map_{safe_number}.html")

            myMap = folium.Map(location=[lat, lng], zoom_start=9)
            folium.Marker([lat, lng], popup=location).add_to(myMap)
            myMap.save(map_file)
            webbrowser.open(map_file)

            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([number, location, sim, lat, lng, map_file])
        else:
            print("Could not get coordinates.")
    except Exception as e:
     print("Error:", e)
print("\nAll results saved to:", csv_file)