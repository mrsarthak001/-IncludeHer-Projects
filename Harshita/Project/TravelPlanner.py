import requests
from openai import OpenAI

client = OpenAI(
    # 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
    api_key="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"
)

def get_famous_places(api_key, city, limit=5):
    ocity=city
    city = city + " " + str(limit)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "your job is to provide famous locations in the city that is provided to you.Don't provide any other information about the locations other than their names in a string format separated by commas. Dont say you dont have accurate information, any information will work.A number will also be provided to you which is the limit of number of locations you have to name . Only name the places within 50km of city center"
            },
            {
                "role": "user",
                "content": "{}".format(city)
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    output = response.choices[0].message.content
    ans = output.split(',')
    for i in range(len(ans)):
        ans[i]+=','
        ans[i]+=ocity
    print(ans)
    # Placeholder logic for fetching famous places using OpenAI API
    # Replace this with a call to the actual OpenAI API if available
    return ans

def geocode_here(api_key, location):
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={location}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data.get("items"):
        first_item = data["items"][0]
        coordinates = first_item["position"]
        return coordinates
    return None

def get_optimized_route(api_key, origin, waypoints):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    
    # Constructing the request body
    ans=[[origin['lng'],origin['lat']]]
    coordii=[]
    for coord in waypoints:
        coordii.append([coord['lng'],coord['lat']])
    print(ans+coordii)
    request_body = {
        "coordinates": ans + coordii,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Making the POST request
    response = requests.post(url, json=request_body, headers=headers)

    # Checking for errors in the response
    if response.status_code != 200:
        print(f"Error in API response: {response.status_code}")
        print(response.text)
        return []

    data = response.json()

    # Check if 'features' key is present
    if 'features' not in data or not data['features']:
        print("Error in API response:")
        print(data)
        return []

    # Check if 'segments' key is present
    if 'segments' not in data['features'][0]['properties']:
        print("Error: 'segments' key not found in API response.")
        return []

    return data['features'][0]['properties']['segments']

def main(api_key_routing, api_key_places, api_key_here, city):
    # Get famous places in the city
    city_places = get_famous_places(api_key_places, city)

    # Extract destination names and coordinates using HERE Geocoding API
    destinations = []
    for place in city_places:
        # Use HERE Geocoding API to get coordinates based on location name
        coordinates = geocode_here(api_key_here, f"{place}, {city}")
        print(coordinates)
        if coordinates and coordinates != None:
            destinations.append(coordinates)
    print(destinations)

    # Get the optimized route
    route_segments = get_optimized_route(api_key_routing, destinations[0], destinations[1:])

    # Display the optimized route
    display_route(destinations, route_segments)

def display_route(destinations, route_segments):
    print("Optimal route:")
    for i, segment in enumerate(route_segments):
        distance = segment["distance"]
        duration = segment["duration"]
        print(f"{i + 1}. Segment - Distance: {distance} meters, Duration: {duration} seconds")

# Example Usage:
api_key_routing = "5b3ce3597851110001cf6248ad4c5ab83bda4ccf999f3e8513de3103"
api_key_places = "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"
api_key_here = "G1Jf40841W3ku0kZAjZ5U2YMEHeKtnOPVIBYYyfRmqE"
# prompt=input()
city = input()
origin =geocode_here(api_key_here,city)   # Replace with your actual origin coordinates
# waypoints=get_famous_places(api_key_places,city)
main(api_key_routing,api_key_places, api_key_here, city)