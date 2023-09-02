import textwrap
from urllib.parse import urlencode
import os
from pathlib import Path

if os.getenv('ENVIRONMENT') == 'k8s':
    STATION_NAME_LENGTH = int(Path('/etc/worker-config-vol/nrel.stationnamelength').read_text())
    POST_SIZE = int(Path('/etc/worker-config-vol/masto.postsize').read_text())
else:
    STATION_NAME_LENGTH = 30
    POST_SIZE = 500

def get_connector_types(connectors):
    """
    🅐 🅑 🅒 🅓 🅔 🅕 🅖 🅗 🅘 🅙 🅚 🅛 🅜 🅝 🅞 🅟 🅠 🅡 🅢 🅣 🅤 🅥 🅦 🅧 🅨 🅩
    Ⓐ Ⓑ Ⓒ Ⓓ Ⓔ Ⓕ Ⓖ Ⓗ Ⓘ Ⓙ Ⓚ Ⓛ Ⓜ Ⓝ Ⓞ Ⓟ Ⓠ Ⓡ Ⓢ Ⓣ Ⓤ Ⓥ Ⓦ Ⓧ Ⓨ Ⓩ
    ⓪ ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬ ⑭ ⑮ ⑯ ⑰ ⑱ ⑲ ⑳ ㉑ ㉒ ㉓ ㉔ ㉕ ㉖ ㉗ ㉘ ㉙ ㉚ ㉛ ㉜ ㉝ ㉞ ㉟ ㊱ ㊲ ㊳ ㊴ ㊵ ㊶ ㊷ ㊸ ㊹ ㊺ ㊻ ㊼ ㊽ ㊾ ㊿
    """
    
    for i in range(len(connectors)):
        connectors[i] = connectors[i] \
            .replace('NEMA1450', 'Ⓝ⑭-㊿') \
            .replace('NEMA515', 'Ⓝ⑤-⑮') \
            .replace('NEMA520', 'Ⓝ⑤-⑳') \
            .replace('J1772COMBO', 'ⒸⒸⓈ') \
            .replace('J1772', 'Ⓙ') \
            .replace('CHADEMO', 'ⒸⒽⒶ') \
            .replace('TESLA', 'Ⓣ') 
    
    return '  '.join(connectors).strip()

def form_list_of_stations(fuel_stations):
    results = []

    if fuel_stations:
        for station in fuel_stations:
            params = {
                'sll': f"{station.get('latitude')},{station.get('longitude')}",
                'q': station.get('street_address')
                }
            params_encoded = urlencode(params)
            url = f"https://maps.apple.com/?{params_encoded}"
            
            results.append([
                '🔌' + get_connector_types(station.get('ev_connector_types')),  
                textwrap.shorten(station.get('station_name'), width=STATION_NAME_LENGTH, placeholder="..."), 
                url
                ])

    return results

def split_text_into_chunks(text, chunk_size=POST_SIZE):
    chunks = []
    current_chunk = ""

    lines = text.split("\n")
    for line in lines:
        if len(current_chunk) + len(line) + 1 <= chunk_size:  # +1 for the newline character
            # fits in the current chunk
            if current_chunk:
                current_chunk += "\n" + line
            else:
                current_chunk = line
        else:
            # doesn't fit in the current chunk, start a new one
            chunks.append(current_chunk)
            current_chunk = line

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
