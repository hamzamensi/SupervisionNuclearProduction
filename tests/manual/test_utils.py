import os
import random
from datetime import datetime, timedelta
from unittest import TestCase

from core.utils import get_data


class Test(TestCase):
    def test_get_data(self):
        # normal use case
        start_date = '2023-01-01T00:00:00+01:00'
        end_date = '2023-01-11T00:00:00+01:00'
        resutl_df = get_data(start_date, end_date)
        start_time_object = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S%z')
        end_time_object = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S%z')
        diff = (end_time_object - start_time_object).total_seconds() // 60 // 60
        #assuer qu'on a récupére toutes les heures
        self.assertEquals(len(resutl_df), diff)
        self.assertEquals(resutl_df['start_date'].min(), start_date)
        self.assertEquals(resutl_df['start_date'].max(), (end_time_object + timedelta(hours=-1)).isoformat())
        # take random hour and test if we have data for this hour
        random_day = random.randint(1, 11)
        random_hour = random.randint(0, 24)
        random_date = datetime(2023, 1, random_day, random_hour).astimezone().isoformat(sep="T", timespec="seconds")
        random_date_df = resutl_df[resutl_df['start_date'] == random_date]
        self.assertGreater(len(random_date_df), 0)
        # date format is not correct
        start_date = '2022-12-01T00:00:00+01:00'
        end_date = '2022-12-11T00:00:0001:00'
        with self.assertRaises(ValueError):
            get_data(start_date, end_date)

        # token is not correct
        start_date = '2022-12-01T00:00:00+01:00'
        end_date = '2022-12-11T00:00:00+01:00'
        os.environ['ClientId'] = 'NOT OK'
        with self.assertRaises(Exception):
            resutl_df = get_data(start_date, end_date)

        #

