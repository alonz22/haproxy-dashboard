import requests
import csv

HAPROXY_STATS_URL = 'http://127.0.0.1:8080/;csv'

def fetch_haproxy_stats():
    try:
        response = requests.get(HAPROXY_STATS_URL)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return str(e)

def parse_haproxy_stats(stats_data):
    data = []
    # Remove the '#' character from the header row
    header_row = stats_data.splitlines()[0].replace('# ', '')
    reader = csv.DictReader(stats_data.splitlines(), fieldnames=header_row.split(','))
    next(reader)  # Skip the header row
    for row in reader:
        if row['svname'] != 'BACKEND':
            data.append({
                'frontend_name': row['pxname'],
                'server_name': row['svname'],
                '4xx_errors': row['hrsp_4xx'],
                '5xx_errors': row['hrsp_5xx'],
                'bytes_in_mb': f'{float(row["bin"]) / (1024 * 1024):.2f}',
                'bytes_out_mb': f'{float(row["bout"]) / (1024 * 1024):.2f}',
                'conn_tot': row['conn_tot'],
            })
    return data