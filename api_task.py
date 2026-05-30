
import requests
import datetime
import sys

WTTR_URL = 'https://wttr.in/{loc}?format=j1'
OUTPUT_FILE = 'weather_output.txt'


def fetch_weather(location, timeout=10):
    url = WTTR_URL.format(loc=location)
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")
    except ValueError:
        raise RuntimeError("Failed to parse JSON response")


def parse_weather(data):
    # Safe extraction with fallbacks
    out = {}
    try:
        current = data.get('current_condition', [{}])[0]
        nearest = data.get('nearest_area', [{}])[0]
        area = nearest.get('areaName', [{}])[0].get('value', 'Unknown')
        region = nearest.get('region', [{}])[0].get('value', '')
        country = nearest.get('country', [{}])[0].get('value', '')

        out['location'] = ", ".join(filter(None, [area, region, country])) or 'Unknown'
        out['temp_C'] = current.get('temp_C')
        out['feelsLikeC'] = current.get('FeelsLikeC') or current.get('feelsLikeC')
        out['weatherDesc'] = current.get('weatherDesc', [{}])[0].get('value', '')
        out['humidity'] = current.get('humidity')
        out['wind_kmph'] = current.get('windspeedKmph')
        out['wind_dir'] = current.get('winddir16Point')
        out['precip_mm'] = current.get('precipMM')
        out['visibility_km'] = current.get('visibility')
        out['pressure_mb'] = current.get('pressure')
        # short forecast for today
        weather_list = data.get('weather', [])
        if weather_list:
            today = weather_list[0]
            out['maxtempC'] = today.get('maxtempC')
            out['mintempC'] = today.get('mintempC')
            out['avgtempC'] = today.get('avgtempC')
            # hourly summary pick midday
            hours = today.get('hourly', [])
            if hours:
                summary = hours[len(hours)//2]
                out['summary'] = summary.get('weatherDesc', [{}])[0].get('value', '')
        return out
    except Exception as e:
        raise RuntimeError(f"Unexpected JSON structure: {e}")


def format_output(parsed):
    lines = []
    lines.append(f"Location: {parsed.get('location')}")
    lines.append(f"Condition: {parsed.get('weatherDesc', 'N/A')}")
    lines.append(f"Temperature: {parsed.get('temp_C', 'N/A')} °C (feels like {parsed.get('feelsLikeC','N/A')} °C)")
    lines.append(f"High / Low / Avg: {parsed.get('maxtempC','N/A')}°C / {parsed.get('mintempC','N/A')}°C / {parsed.get('avgtempC','N/A')}°C")
    lines.append(f"Humidity: {parsed.get('humidity','N/A')} %")
    lines.append(f"Wind: {parsed.get('wind_kmph','N/A')} km/h {parsed.get('wind_dir','')}")
    lines.append(f"Precipitation (mm): {parsed.get('precip_mm','N/A')}")
    lines.append(f"Visibility (km): {parsed.get('visibility_km','N/A')}")
    lines.append(f"Pressure (mb): {parsed.get('pressure_mb','N/A')}")
    if parsed.get('summary'):
        lines.append(f"Today summary: {parsed.get('summary')}")
    return "\n".join(lines)


def save_output(text):
    ts = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{ts}]\n")
        f.write(text + "\n\n")


def main():
    if len(sys.argv) > 1:
        location = " ".join(sys.argv[1:])
    else:
        location = input('Enter location (city, region or leave blank for auto): ').strip() or ' '  # wttr.in handles empty

    try:
        data = fetch_weather(location)
        parsed = parse_weather(data)
        out = format_output(parsed)
        print('\n' + out + '\n')
        save_output(out)
    except RuntimeError as e:
        print('Error:', e)


if __name__ == '__main__':
    main()
