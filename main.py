import pandas as pd
import requests


if __name__ == '__main__':

    r = requests.post('https://digital.iservices.rte-france.com/token/oauth/',
                      auth=('725d36cd-672f-4912-8026-4242ea07d122', '37c90719-4d57-42bd-a5fe-7762f866d10d'))
    if r.ok:
        access_token = r.json()['access_token']
        tokenlist_1D_type = r.json()['token_type']
    else:
        Warning("Authentication failed")
        access_token = None
        token_type = None

    print(token_type, access_token)
    gen_per_unit = requests.get(
        'https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_unit'
        , headers={
            'Authorization': f'{token_type} {access_token}'
        }
    ).json()['actual_generations_per_unit']
    values_by_unit = [val['values'] for val in gen_per_unit]
    all_values = [item for sub_list in values_by_unit for item in sub_list]
    df = pd.DataFrame(all_values)
