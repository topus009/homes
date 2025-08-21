import json
from bs4 import BeautifulSoup
import requests

def get_coords(address):
    """
    Geocode an address using Nominatim API.
    """
    try:
        url = 'https://nominatim.openstreetmap.org/search'
        params = {'q': address, 'format': 'json', 'limit': 1}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        results = response.json()
        if results:
            return float(results[0]['lat']), float(results[0]['lon'])
    except requests.exceptions.RequestException as e:
        print(f"Error geocoding address '{address}': {e}")
    return None, None

def parse_apartments():
    """
    Parses the homes.html file to extract apartment data.
    """
    try:
        with open('homes.html', 'r', encoding='utf-8') as f:
            contents = f.read()
    except FileNotFoundError:
        print("Error: homes.html not found.")
        return []

    soup = BeautifulSoup(contents, 'html.parser')
    apartments = []

    for item in soup.find_all('div', class_='favorite-snippet-root-xE9AV'):
        title_tag = item.find('strong', class_='styles-module-root-ZQ_IR')
        title = title_tag.text.strip() if title_tag else 'N/A'

        price_tag = item.find('h4', class_='styles-module-root-itN2x')
        price = price_tag.text.strip().replace('\xa0', ' ') if price_tag else 'N/A'
        
        address_tag = item.find('span', class_='location-addressLine-rCtB_')
        address = address_tag.text.strip() if address_tag else 'N/A'

        img_tag = item.find('img', class_='favorite-snippet-image-LYwCe')
        img_src = img_tag['src'] if img_tag else ''

        link_tag = item.find('a', class_='styles-module-root-jiqsZ')
        link = 'https://www.avito.ru' + link_tag['href'] if link_tag and link_tag.has_attr('href') else '#'

        lat, lon = get_coords(address)

        apartments.append({
            'title': title,
            'price': price,
            'address': address,
            'img_src': img_src,
            'link': link,
            'lat': lat,
            'lon': lon
        })

    return apartments

def create_map_html(apartments):
    """
    Creates an HTML file with a map and a list of apartments.
    """
    
    apartments_json = json.dumps([apt for apt in apartments if apt['lat'] is not None and apt['lon'] is not None], ensure_ascii=False)

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Карта апартаментов в Сочи</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
        }}
        #map {{
            height: 100vh;
            width: 70%;
        }}
        #list {{
            width: 30%;
            height: 100vh;
            overflow-y: auto;
            padding: 10px;
            box-sizing: border-box;
        }}
        .apartment {{
            border-bottom: 1px solid #ccc;
            padding: 10px;
            cursor: pointer;
        }}
        .apartment:hover {{
            background-color: #f0f0f0;
        }}
        .apartment img {{
            max-width: 100%;
            height: auto;
            margin-bottom: 5px;
        }}
        .apartment h3 {{
            margin: 0 0 5px 0;
            font-size: 16px;
        }}
        .apartment p {{
            margin: 0;
            font-size: 14px;
        }}
    </style>
</head>
<body>

    <div id="map"></div>
    <div id="list"></div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        const apartments = {apartments_json};

        const map = L.map('map').setView([43.5855, 39.7231], 12); // Default to Sochi center

        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }}).addTo(map);

        const listContainer = document.getElementById('list');
        const markers = [];

        apartments.forEach((apt, index) => {{
            // Add marker
            const marker = L.marker([apt.lat, apt.lon]).addTo(map)
                .bindPopup(`<b>${{apt.title}}</b><br>${{apt.address}}<br><a href="${{apt.link}}" target="_blank">Подробнее</a>`);
            markers.push(marker);

            // Add to list
            const listItem = document.createElement('div');
            listItem.className = 'apartment';
            listItem.innerHTML = `
                <img src="${{apt.img_src}}" alt="${{apt.title}}">
                <h3>${{apt.title}}</h3>
                <p>${{apt.price}}</p>
                <p>${{apt.address}}</p>
            `;
            listItem.addEventListener('click', () => {{
                map.setView([apt.lat, apt.lon], 15);
                marker.openPopup();
            }});
            listContainer.appendChild(listItem);
        }});
        
        if (apartments.length > 0) {{
             const validCoords = apartments.filter(apt => apt.lat && apt.lon);
             if (validCoords.length > 0) {{
                const bounds = L.latLngBounds(validCoords.map(apt => [apt.lat, apt.lon]));
                map.fitBounds(bounds);
             }}
        }}

    </script>
</body>
</html>
    """

    with open('map.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    apartments_data = parse_apartments()
    if apartments_data:
        create_map_html(apartments_data)
        print(f"Successfully processed {{len(apartments_data)}} apartments and created map.html")
