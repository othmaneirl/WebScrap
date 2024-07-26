# Ce script permet de modifier les dates de check-in et check-out dans les URLs des liens Airbnb.
import csv
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import json


def adjust_dates_in_url(url, months_delta):
    parsed_url = urlparse(url[0])
    query_params = parse_qs(parsed_url.query)

    if 'check_in' in query_params and 'check_out' in query_params:
        check_in_date = datetime.strptime(query_params['check_in'][0], '%Y-%m-%d')
        check_out_date = datetime.strptime(query_params['check_out'][0], '%Y-%m-%d')

        new_check_in_date = check_in_date + timedelta(days=months_delta * 30)
        new_check_out_date = check_out_date + timedelta(days=months_delta * 30-3)

        query_params['check_in'][0] = new_check_in_date.strftime('%Y-%m-%d')
        query_params['check_out'][0] = new_check_out_date.strftime('%Y-%m-%d')

        new_query_string = urlencode(query_params, doseq=True)
        new_url = urlunparse(parsed_url._replace(query=new_query_string))
        return new_url, url[1], url[2]
    else:
        return url[0], url[1], url[2]


def adjust_dates_in_csv(input_csv, output_csv, months_delta):
    with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            if row:
                updated_url = adjust_dates_in_url(row, months_delta)
                writer.writerow(updated_url)


input_csv = 'Liens/test2.csv'
output_csv = 'Liens/test3.csv'
months_delta = 3

adjust_dates_in_csv(input_csv, output_csv, months_delta)
