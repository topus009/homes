import json
import requests
from bs4 import BeautifulSoup
import time
import random

def get_random_user_agent():
    """
    Returns a random User-Agent string from a list of popular browsers.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0'
    ]
    return random.choice(user_agents)

def get_coords(address):
    """
    Geocode an address using Nominatim API.
    """
    try:
        url = 'https://nominatim.openstreetmap.org/search'
        params = {'q': address, 'format': 'json', 'limit': 1}
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        results = response.json()
        if results:
            return float(results[0]['lat']), float(results[0]['lon'])
    except requests.exceptions.RequestException as e:
        print(f"Error geocoding address '{address}': {e}")
    return None, None

def parse_apartment_page(url):
    """
    Parse individual apartment page to extract data.
    """
    try:
        headers = {
            'User-Agent': get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title - try multiple selectors
        title = 'N/A'
        title_selectors = [
            'h1[data-marker="item-view/title-info"]',
            'h1.title-info-title',
            'h1',
            '.title-info-title'
        ]
        for selector in title_selectors:
            title_tag = soup.select_one(selector)
            if title_tag:
                title = title_tag.text.strip()
                break
        
        # Extract price - try multiple selectors
        price = 'N/A'
        price_selectors = [
            'span[data-marker="item-view/item-price"]',
            '.price-value-string',
            '.price-value',
            '.price'
        ]
        for selector in price_selectors:
            price_tag = soup.select_one(selector)
            if price_tag:
                price = price_tag.text.strip()
                break
        
        # Extract address - try multiple selectors
        address = 'N/A'
        address_selectors = [
            'span[data-marker="item-view/item-address"]',
            '.item-address',
            '.address',
            '.location'
        ]
        for selector in address_selectors:
            address_tag = soup.select_one(selector)
            if address_tag:
                address = address_tag.text.strip()
                break
        
        # Extract image - try multiple selectors
        img_src = ''
        img_selectors = [
            'img[data-marker="item-view/item-gallery-image"]',
            '.gallery-img img',
            '.item-gallery img',
            'img'
        ]
        for selector in img_selectors:
            img_tag = soup.select_one(selector)
            if img_tag and img_tag.has_attr('src'):
                img_src = img_tag['src']
                if not img_src.startswith('http'):
                    img_src = 'https:' + img_src
                break
        
        return {
            'title': title,
            'price': price,
            'address': address,
            'img_src': img_src,
            'link': url
        }
        
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return None

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

    with open('map_from_links.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    """
    Main function to process all apartment URLs.
    """
    urls = [
        "https://www.avito.ru/sochi/kvartiry/1-k._kvartira_35_m_1_krovat_3315076458",
        "https://www.avito.ru/sochi/kvartiry/1-k._kvartira_35_m_2_krovati_4187170434",
        "https://www.avito.ru/sochi/kvartiry/1-k._kvartira_60_m_2_krovati_7314110887",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_15_m_1_krovat_7420521129",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_158_m_1_krovat_2970972960",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_17_m_1_krovat_7362114551",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_17_m_2_krovati_3298941260",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_17_m_2_krovati_4110914610",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_18_m_1_krovat_7346954022",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_18_m_1_krovat_7441092871",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_18_m_2_krovati_7522770065",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_20_m_1_krovat_3449836577",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_20_m_1_krovat_7454213728",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_22_m_1_krovat_4446589620",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_22_m_1_krovat_4446885607",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_23_m_1_krovat_2851633711",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_23_m_1_krovat_7365343666",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_24_m_1_krovat_7576248312",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_1_krovat_3248328432",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_1_krovat_4062872622",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_1_krovat_7462473340",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_2_krovati_2684184213",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_2_krovati_7390608188",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_26_m_1_krovat_4414912393",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_29_m_3_krovati_3348707486",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_30_m_1_krovat_7294643260",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_30_m_1_krovat_7367602586",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_30_m_2_krovati_1051538363",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_32_m_2_krovati_3377425991",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_32_m_2_krovati_7233900703",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_38_m_2_krovati_2977636635",
        "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_v_apart-otele_17_m_1_krovat_7509877303"
    ]
    
    apartments = []
    
    print(f"Processing {len(urls)} apartment URLs...")
    
    for i, url in enumerate(urls, 1):
        print(f"Processing {i}/{len(urls)}: {url}")
        
        apartment_data = parse_apartment_page(url)
        if apartment_data:
            # Get coordinates for the address
            lat, lon = get_coords(apartment_data['address'])
            apartment_data['lat'] = lat
            apartment_data['lon'] = lon
            
            apartments.append(apartment_data)
            print(f"  ✓ {apartment_data['title']} - {apartment_data['address']}")
        else:
            print(f"  ✗ Failed to parse")
        
        # Add delay to avoid overwhelming the server
        time.sleep(10)
    
    print(f"\nSuccessfully processed {len(apartments)} apartments")
    
    if apartments:
        create_map_html(apartments)
        print("Created map_from_links.html")
    else:
        print("No apartments were processed successfully")

if __name__ == '__main__':
    main()
