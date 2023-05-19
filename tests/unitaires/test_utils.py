import random
from unittest import TestCase
from core.utils import get_sum_value_by_hour, get_nuclear_data, request_data

import pandas as pd


class Test(TestCase):

    def test_get_sum_value_by_hour(self):
        generate_random_values = random.sample(range(15), 5)
        input_data = [['2022-01-12T00:00:00+01:00', value] for value in generate_random_values]
        input_df = pd.DataFrame(columns=['start_date', 'value'], data=input_data)
        result_df = get_sum_value_by_hour(input_df)
        expected_df = pd.DataFrame(
            columns=['start_date', 'Sum_per_hour', 'mean_by_hour'],
            data=[['2022-01-12T00:00:00+01:00', sum(generate_random_values),
                   sum(generate_random_values) / len(generate_random_values)]]
        )
        self.assertTrue(expected_df.equals(result_df))
        generate_random_values = random.sample(range(15), 5)
        input_data = [['2022-01-12T00:00:00+01:00', value] for value in generate_random_values]
        input_df = pd.DataFrame(columns=['start_date', 'valuetest'], data=input_data)
        with self.assertRaises(Exception):
            result_df = get_sum_value_by_hour(input_df)

    def test_request_data(self):
        # Nomral use case
        start_date = '2022-01-10T00:00:00+01:00'
        end_date = '2022-01-12T00:00:00+01:00'
        result = request_data(start_date, end_date)
        min_start_date_result = min([res['start_date'] for res in result])
        self.assertEquals(start_date, min_start_date_result)
        max_end_date_result = max([res['end_date'] for res in result])
        self.assertEquals(end_date, max_end_date_result)
        # wrong format of date
        start_date = '2022-01-10T00:0'
        end_date = '2022-01-12T00:00:00+01:00'
        with self.assertRaises(ValueError):
            result = request_data(start_date, end_date)


    def test_get_nuclear_data(self):
        # first case normal use case
        input_value = [
            {'start_date': '2022-12-01T00:00:00+01:00', 'end_date': '2022-12-08T00:00:00+01:00', 'unit': {'eic_code': '17W100P100P00016', 'name': 'Pont-sur-Sambre', 'production_type': 'FOSSIL_GAS'}, 'values': [{'start_date': '2022-12-01T00:00:00+01:00', 'end_date': '2022-12-01T01:00:00+01:00', 'updated_date': '2022-12-04T15:40:19+01:00', 'value': 408.5}]},
            {'start_date': '2022-12-01T00:00:00+01:00', 'end_date': '2022-12-08T00:00:00+01:00',
             'unit': {'eic_code': '17W100P100P00016', 'name': 'Pont-sur-Sambre', 'production_type': 'NUCLEAR'},
             'values': [{'start_date': '2022-12-01T00:00:00+01:00', 'end_date': '2022-12-01T01:00:00+01:00',
                         'updated_date': '2022-12-04T15:40:19+01:00', 'value': 408.5}]}

        ]
        result_df = get_nuclear_data(input_value)
        expected_df = pd.DataFrame(columns=['start_date', 'Sum_per_hour', 'mean_by_hour'], data=[['2022-12-01T00:00:00+01:00', 408.5, 408.5]])
        self.assertTrue(expected_df.equals(result_df.reset_index(drop=True)))
        # second case no nuclear data
        input_value = [
            {'start_date': '2022-12-01T00:00:00+01:00', 'end_date': '2022-12-08T00:00:00+01:00',
             'unit': {'eic_code': '17W100P100P00016', 'name': 'Pont-sur-Sambre', 'production_type': 'FOSSIL_GAS'},
             'values': [{'start_date': '2022-12-01T00:00:00+01:00', 'end_date': '2022-12-01T01:00:00+01:00',
                         'updated_date': '2022-12-04T15:40:19+01:00', 'value': 408.5}]},
            {'start_date': '2022-12-01T00:00:00+01:00', 'end_date': '2022-12-08T00:00:00+01:00',
             'unit': {'eic_code': '17W100P100P00016', 'name': 'Pont-sur-Sambre', 'production_type': 'FOSSIL_GAS'},
             'values': [{'start_date': '2022-12-01T00:00:00+01:00', 'end_date': '2022-12-01T01:00:00+01:00',
                         'updated_date': '2022-12-04T15:40:19+01:00', 'value': 408.5}]}

        ]
        with self.assertRaises(Exception):
            result_df = get_nuclear_data(input_value)
