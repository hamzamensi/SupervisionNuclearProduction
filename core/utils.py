from datetime import datetime, timedelta

import pandas as pd
import pytz
import requests
import urllib.parse
import os


def get_token():
    r = requests.post('https://digital.iservices.rte-france.com/token/oauth/',
                      # auth=('725d36cd-672f-4912-8026-4242ea07d122', '37c90719-4d57-42bd-a5fe-7762f866d10d')
                      auth=(os.environ['ClientId'], os.environ['SecretId'])
                      )
    if r.ok:
        access_token = r.json()['access_token']
        token_type = r.json()['token_type']
    else:
        Warning("Authentication failed")
        access_token = None
        token_type = None
        raise Exception('Authentication failed')
    return token_type, access_token


def get_sum_value_by_hour(df):
    try:
        sum_per_hour = df['value'].sum()
        mean_by_hour = df['value'].mean()
        df = pd.DataFrame(columns=['start_date', 'Sum_per_hour', 'mean_by_hour'], data=[[df.iloc[0]['start_date'], sum_per_hour, mean_by_hour]])
    except KeyError:
        print('Wrong dataframe in input')
        raise KeyError('Wrong dataframe in input')
        return
    return df


def get_nuclear_data(data):
    try:
        values_by_unit = [val['values'] for val in data if val['unit']['production_type'] == 'NUCLEAR']
        all_values = [item for sub_list in values_by_unit for item in sub_list]
        df = pd.DataFrame(all_values)
        df = df.groupby(['start_date']).apply(lambda x: get_sum_value_by_hour(x))
        return df
    except KeyError:
        raise KeyError()
        print('le format de données est incorrect')


def request_data(start_date, end_date):
    try:
        startdateObject = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S%z')
        enddateObject = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        raise ValueError()
        print("Incorrect data format, should be YYYY-MM-DDTHH:MM:SS+HH:MM")
    token_type, access_token = get_token()
    if token_type is None or access_token is None:
        raise Exception('Erreur de récupérartion le token')
    params = {'start_date': start_date, 'end_date': end_date}
    url = f'https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_unit?{urllib.parse.urlencode(params, doseq=True)}'
    request_data = requests.get(
        url
        , headers={
            'Authorization': f'{token_type} {access_token}'
        }
    )
    if request_data.ok:
        if 'actual_generations_per_unit' not in request_data.json():
            raise Exception('Wrong format of data')
        return request_data.json()['actual_generations_per_unit']
    else:
        if request_data.status_code == 400:
            raise Exception('Veuillez vérifier les parametres')
        else:
            raise Exception("il y a un problème avec l'api")


def get_data_from_api(start_date, end_date):
    try:
        start_time_object = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S%z')
        end_time_object = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S%z')
        data = []
        if (end_time_object - start_time_object).days > 7:
            ok = False
            while not ok:
                provisoire_end_date = start_time_object + timedelta(days=7)
                prov_date = provisoire_end_date.isoformat()
                if provisoire_end_date >= end_time_object:
                    ok = True
                    prov_date = end_time_object.isoformat()
                data.extend(request_data(start_date, prov_date))
                start_time_object = provisoire_end_date
                start_date = start_time_object.isoformat()
            return data
        else:
            return request_data(start_date, end_date)
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DDTHH:MM:SS+HH:MM")


def get_data(start_date, end_date):
    data_per_unit = get_data_from_api(start_date, end_date)
    df = get_nuclear_data(data_per_unit)
    return df
