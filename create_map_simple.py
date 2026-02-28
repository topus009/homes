import json
from bs4 import BeautifulSoup

def parse_existing_data():
    """
    Parse existing apartment data from homes.html
    """
    try:
        with open('homes.html', 'r', encoding='utf-8') as f:
            contents = f.read()
    except FileNotFoundError:
        print("Error: homes.html not found.")
        return {}

    soup = BeautifulSoup(contents, 'html.parser')
    apartments_data = {}

    for item in soup.find_all('div', class_='favorite-snippet-root-xE9AV'):
        link_tag = item.find('a', class_='styles-module-root-jiqsZ')
        if link_tag and link_tag.has_attr('href'):
            link = 'https://www.avito.ru' + link_tag['href']
            
            title_tag = item.find('strong', class_='styles-module-root-ZQ_IR')
            title = title_tag.text.strip() if title_tag else 'N/A'

            price_tag = item.find('h4', class_='styles-module-root-itN2x')
            price = price_tag.text.strip().replace('\xa0', ' ') if price_tag else 'N/A'
            
            address_tag = item.find('span', class_='location-addressLine-rCtB_')
            address = address_tag.text.strip() if address_tag else 'N/A'

            img_tag = item.find('img', class_='favorite-snippet-image-LYwCe')
            img_src = img_tag['src'] if img_tag else ''

            apartments_data[link] = {
                'title': title,
                'price': price,
                'address': address,
                'img_src': img_src
            }

    return apartments_data

def create_map_html():
    """
    Creates an HTML file with a map using provided coordinates.
    """
    
    # Coordinates from Yandex Maps (user provided)
    apartments = [
        {
            "url": "https://www.avito.ru/sochi/kvartiry/1-k._kvartira_35_m_2_krovati_4187170434",
            "lat": 43.631197,
            "lon": 39.723305,
            "address": "ул. Тимирязева, 34Б"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/1-k._kvartira_60_m_2_krovati_7314110887",
            "lat": 43.638740,
            "lon": 39.695681,
            "address": "СТ Экран, 58А"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_15_m_1_krovat_7420521129",
            "lat": 43.569341,
            "lon": 39.765804,
            "address": "Ясногорская ул., 16/2к1"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_158_m_1_krovat_2970972960",
            "lat": 43.616492,
            "lon": 39.717780,
            "address": "Клубничная ул., 1/17"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_17_m_1_krovat_7362114551",
            "lat": 43.568068,
            "lon": 39.767825,
            "address": "Ясногорская ул., 16/2к5"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_17_m_2_krovati_3298941260",
            "lat": 43.571569,
            "lon": 39.764834,
            "address": "Ясногорская ул., 16/8к2"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_17_m_2_krovati_4110914610",
            "lat": 43.569054,
            "lon": 39.765831,
            "address": "Ясногорская ул., 16/2"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_18_m_1_krovat_7346954022",
            "lat": 43.568564,
            "lon": 39.766918,
            "address": "Ясногорская ул., 16/2к3"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_18_m_1_krovat_7441092871",
            "lat": 43.635093,
            "lon": 39.700918,
            "address": "Полтавская ул., 21Ак1"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_18_m_2_krovati_7522770065",
            "lat": 43.568068,
            "lon": 39.767825,
            "address": "Ясногорская ул., 16/2к5"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_20_m_1_krovat_3449836577",
            "lat": 43.492002,
            "lon": 39.902419,
            "address": "ул. Искры, 66/9"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_20_m_1_krovat_7454213728",
            "lat": 43.568930,
            "lon": 39.768023,
            "address": "Ясногорская ул., 16/2к6"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_22_m_1_krovat_4446589620",
            "lat": 43.568564,
            "lon": 39.766918,
            "address": "Ясногорская ул., 16/2к3"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_22_m_1_krovat_4446885607",
            "lat": 43.567813,
            "lon": 39.768795,
            "address": "Ясногорская ул., 16/2к8"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_23_m_1_krovat_7365343666",
            "lat": 43.568068,
            "lon": 39.767824,
            "address": "Ясногорская ул., 16/2к5"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_24_m_1_krovat_7576248312",
            "lat": 43.568930,
            "lon": 39.768023,
            "address": "Ясногорская ул., 16/2к6"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_1_krovat_3248328432",
            "lat": 43.590396,
            "lon": 39.754440,
            "address": "ул. Яна Фабрициуса, 66/4"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_1_krovat_4062872622",
            "lat": 43.569341,
            "lon": 39.765804,
            "address": "Ясногорская ул., 16/2к1"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_1_krovat_7462473340",
            "lat": 43.492002,
            "lon": 39.902419,
            "address": "ул. Искры, 66/9"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_2_krovati_2684184213",
            "lat": 43.528792,
            "lon": 39.838657,
            "address": "Звёздная ул., 18А"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_25_m_2_krovati_7390608188",
            "lat": 43.492002,
            "lon": 39.902419,
            "address": "ул. Искры, 66/9"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_26_m_1_krovat_4414912393",
            "lat": 43.568930,
            "lon": 39.768023,
            "address": "Ясногорская ул., 16/2к6"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_29_m_3_krovati_3348707486",
            "lat": 43.493703,
            "lon": 39.899788,
            "address": "ул. Искры, 62"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_30_m_1_krovat_7294643260",
            "lat": 43.568518,
            "lon": 39.767153,
            "address": "Ясногорская ул., 16/2к3"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_30_m_1_krovat_7367602586",
            "lat": 43.423285,
            "lon": 40.009453,
            "address": "ул. Мира, 120/2"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_30_m_2_krovati_1051538363",
            "lat": 43.586445,
            "lon": 39.737210,
            "address": "ул. Докучаева, 8"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_32_m_2_krovati_3377425991",
            "lat": 43.493703,
            "lon": 39.899788,
            "address": "ул. Искры, 62"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_32_m_2_krovati_7233900703",
            "lat": 43.492002,
            "lon": 39.902419,
            "address": "ул. Искры, 66/9"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_38_m_2_krovati_2977636635",
            "lat": 43.493802,
            "lon": 39.900103,
            "address": "ул. Искры, 62"
        },
        {
            "url": "https://www.avito.ru/sochi/kvartiry/kvartira-studiya_v_apart-otele_17_m_1_krovat_7509877303",
            "lat": 43.567467,
            "lon": 39.768795,
            "address": "Ясногорская ул., 16/2к7"
        }
    ]

    # Get existing data from HTML
    existing_data = parse_existing_data()
    
    # Combine coordinates with existing data
    for apt in apartments:
        if apt["url"] in existing_data:
            apt.update(existing_data[apt["url"]])
        else:
            # Add manually collected data for specific apartments
            if "2970972960" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 15,8 м², 1 кровать",
                    "price": "2 100 ₽ за сутки",
                    "img_src": "https://60.img.avito.st/image/1/1.6nyCiba1RpX4IIid2vqYbOYrRJU8Ioid-CBElw.72e8Wp8lhu6FfZoXF6EJgw02CrdCt4NNwb2I3O29p6Y"
                })
            elif "7362114551" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 17 м², 1 кровать",
                    "price": "2 200 ₽ за сутки",
                    "img_src": "https://00.img.avito.st/image/1/1.uQYP2ra1Fe8ffLHoccDJFX57F--xcbHoH3wX7Q.2xxaW7gcTcqZb_KzGd5LXHEGnQ3adFzPktdNHQv8VPA"
                })
            elif "3298941260" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 17 м², 2 кровати",
                    "price": "2 000 ₽ за сутки",
                    "img_src": "https://70.img.avito.st/image/1/1.6iR5era1Rs0D04jFIV3hT2zYRM3H0YjFA9NEzw.LAEMlESzZL6elx81liskgilZXrZ96dwtZmfB6vzxNyg"
                })
            elif "4110914610" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 17 м², 2 кровати",
                    "price": "2 000 ₽ за сутки",
                    "img_src": "https://60.img.avito.st/image/1/1.1FOIxLa1eLqSY9a8rPfPF_9lero2b9a8kmN6uA.20ZHJz_XdEC-anhmjN0bck_-vvG-PXImD0f0gcELETI"
                })
            elif "7346954022" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 18 м², 1 кровать",
                    "price": "3 658 ₽ за сутки",
                    "img_src": "https://60.img.avito.st/image/1/1.WTR8lra19d1SN2_dQpNCKxs3993CPW_dUjf33w.ATKNzULIStUtdFmmdO_joGK1E8TJU_SrRlf7e1Qaxmc"
                })
            elif "3449836577" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 20 м², 1 кровать",
                    "price": "2 500 ₽ за сутки",
                    "img_src": "https://40.img.avito.st/image/1/1.W3bBMra195-7mzmX-xdhHLqQ9Z9_mTmXu5v1nQ.yOSfGq38aTO3Nhjw-MPENNHT53YMmy-ZHOwQSNTvAFE"
                })
            elif "4446885607" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 22 м², 1 кровать",
                    "price": "2 000 ₽ за сутки",
                    "img_src": "https://20.img.avito.st/image/1/1.D-Fulra1owh0MQ0OfNY8hGk3oQjQPQ0OdDGhCg.ZItdN3IFVD5RELwF8KiuGjUcZ-1Ph2NWzVVqkcuxv_I"
                })
            elif "7367602586" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 30 м², 1 кровать",
                    "price": "2 350 ₽ за сутки",
                    "img_src": "https://60.img.avito.st/image/1/1.CT2_sra1pdTFG2vcoep_WMATp9QBGWvcxRun1g.UyKYQtCLRgDPSxXPfCcCPQ6L9e8uSrD_WwAJ24Tmle4"
                })
            elif "1051538363" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 30 м², 2 кровати",
                    "price": "2 300 ₽ за сутки",
                    "img_src": "https://50.img.avito.st/image/1/1.PJGB_ra1kHiRWDR_9fY13eBckng_VTR_kViSeg.aYs0YF06NpMdU1s3SqHwqKo9szztMrzq9-5Bs1LBBts"
                })
            elif "2977636635" in apt["url"]:
                apt.update({
                    "title": "Квартира-студия, 38 м², 2 кровати",
                    "price": "2 500 ₽ за сутки",
                    "img_src": "https://00.img.avito.st/image/1/1.BeNWD7a1qQpMqAcMUA8C1mytqwropAcMTKirCA.FB5c8XRQ8VUMtXK2K10yXpnjK_jX0V8P-zWCLWfQlds"
                })
            else:
                apt["title"] = "Апартамент"
                apt["price"] = "Цена не указана"
                apt["img_src"] = ""

    apartments_json = json.dumps(apartments, ensure_ascii=False)

    # Create HTML content
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Карта апартаментов в Сочи</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
        }
        #map {
            height: 100vh;
            width: 70%;
        }
        #list {
            width: 30%;
            height: 100vh;
            overflow-y: auto;
            padding: 10px;
            box-sizing: border-box;
        }
        .apartment {
            border-bottom: 1px solid #ccc;
            padding: 10px;
            cursor: pointer;
        }
        .apartment:hover {
            background-color: #f0f0f0;
        }
        .apartment img {
            width: 413px;
            height: 413px;
            object-fit: cover;
            margin-bottom: 5px;
        }
        .apartment h3 {
            margin: 0 0 5px 0;
            font-size: 16px;
        }
        .apartment p {
            margin: 0;
            font-size: 14px;
        }
        .apartment .address {
            color: #666;
            font-size: 12px;
        }
        .apartment.highlighted {
            background-color: #fff3cd;
            border: 2px solid #ffc107;
        }
    </style>
</head>
<body>

    <div id="map"></div>
    <div id="list"></div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        const apartments = """ + apartments_json + """;

        const map = L.map('map').setView([43.5855, 39.7231], 12); // Default to Sochi center

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        const listContainer = document.getElementById('list');
        const markers = [];

        // Функции для работы с рейтингами
        function getRating(url) {
            return parseInt(localStorage.getItem(`rating_${url}`)) || 0;
        }

        function getRatingColor(rating) {
            switch (rating) {
                case 3: return '#28a745'; // зеленый
                case 2: return '#ffc107'; // желтый
                case 1: return '#dc3545'; // красный
                default: return '#6c757d'; // серый
            }
        }

        // Создаем кастомные иконки для маркеров в зависимости от рейтинга
        function createCustomIcon(rating) {
            const color = getRatingColor(rating);
            return L.divIcon({
                className: 'custom-marker',
                html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            });
        }

        apartments.forEach((apt, index) => {
            // Add marker with custom icon based on rating
            const rating = getRating(apt.url);
            const customIcon = createCustomIcon(rating);
            const marker = L.marker([apt.lat, apt.lon], { icon: customIcon }).addTo(map)
                .bindPopup(`<b>${apt.title}</b><br>${apt.address}<br><a href="${apt.url}" target="_blank">Подробнее</a>`);
            markers.push(marker);

            // Add to list
            const listItem = document.createElement('div');
            listItem.className = 'apartment';
            listItem.id = `apartment-${index}`;
            
            let imgHtml = '';
            if (apt.img_src) {
                imgHtml = `<img src="${apt.img_src}" alt="${apt.title}">`;
            }
            
            listItem.innerHTML = `
                ${imgHtml}
                <h3>${apt.title}</h3>
                <p>${apt.price}</p>
                <p class="address">${apt.address}</p>
            `;
            
            // Click on list item - center map and open popup
            listItem.addEventListener('click', () => {
                map.setView([apt.lat, apt.lon], 15);
                marker.openPopup();
                
                // Remove highlight from all apartments
                document.querySelectorAll('.apartment').forEach(item => {
                    item.classList.remove('highlighted');
                });
                
                // Add highlight to clicked apartment
                listItem.classList.add('highlighted');
                
                // Scroll to the apartment in sidebar
                listItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
            });
            
            // Click on marker - highlight and scroll to apartment in sidebar
            marker.on('click', () => {
                // Remove highlight from all apartments
                document.querySelectorAll('.apartment').forEach(item => {
                    item.classList.remove('highlighted');
                });
                
                // Add highlight to corresponding apartment
                listItem.classList.add('highlighted');
                
                // Scroll to the apartment in sidebar
                listItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
            });
            
            listContainer.appendChild(listItem);
        });
        
        if (apartments.length > 0) {
             const validCoords = apartments.filter(apt => apt.lat && apt.lon);
             if (validCoords.length > 0) {
                const bounds = L.latLngBounds(validCoords.map(apt => [apt.lat, apt.lon]));
                map.fitBounds(bounds);
             }
        }

    </script>
</body>
</html>"""

    with open('map_with_coords.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created map_with_coords.html with {len(apartments)} apartments")

if __name__ == '__main__':
    create_map_html()
