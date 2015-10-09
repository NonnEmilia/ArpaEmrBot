# -*- coding: utf-8 -*-

import json
import datetime


class Forecast:
    IDX_DAYS = 'days'
    IDX_DESCRIPTION = 'wstrings'
    IDX_TEMPERATURE = 'temperature'
    IDX_HUMIDITY = 'humidity'
    IDX_WIND = 'wind'
    IDX_PRECIPITATION = 'precipitation'

    IDX_NIGHT = 0
    IDX_MORNING = 1
    IDX_AFTERNOON = 2
    IDX_EVENING = 3

    IDX_WIND_DIRECTION = 'd'
    IDX_WIND_VELOCITY = 'v'

    SUB_PERIOD_DESCRIPTIONS = {
        0: '0/3',
        1: '3/6',
        2: '6/9',
        3: '9/12',
        4: '12/15',
        5: '15/18',
        6: '18/21',
        7: '21/24',
    }

    forecasts_raw_data = {}

    def __init__(self, raw_data):
        self.forecasts_raw_data = raw_data
        self.load_data()

    def load_data(self):
        # Method to override
        pass

    @staticmethod
    def get_first_sub_period_idx(period_idx):
        return period_idx * 2

    @staticmethod
    def get_second_sub_period_idx(period_idx):
        return (period_idx * 2) + 1


class Forecasts(Forecast):
    IDX_YESTERDAY = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    IDX_TODAY = datetime.datetime.now().strftime('%Y%m%d')
    IDX_TOMORROW = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y%m%d')
    IDX_AFTER_TOMORROW = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y%m%d')

    today = None
    yesterday = None
    tomorrow = None
    after_tomorrow = None

    def __init__(self, json_response):
        response = json.loads(json_response)
        if response['status'] != 'OK':
            raise ValueError('Status is not OK. Cannot load forecasts.')
        self.forecasts_raw_data = response['data']
        self.load_data()

    def load_data(self):
        self.yesterday = DailyForecast(self.forecasts_raw_data[self.IDX_DAYS][self.IDX_YESTERDAY])
        self.today = DailyForecast(self.forecasts_raw_data[self.IDX_DAYS][self.IDX_TODAY])
        self.tomorrow = DailyForecast(self.forecasts_raw_data[self.IDX_DAYS][self.IDX_TOMORROW])
        if self.IDX_AFTER_TOMORROW in self.forecasts_raw_data[self.IDX_DAYS]:
            self.after_tomorrow = DailyForecast(self.forecasts_raw_data[self.IDX_DAYS][self.IDX_AFTER_TOMORROW])


class DailyForecast(Forecast):
    night = None
    morning = None
    afternoon = None
    evening = None

    def load_data(self):
        self.night = PeriodForecast(self.forecasts_raw_data, self.IDX_NIGHT)
        self.morning = PeriodForecast(self.forecasts_raw_data, self.IDX_MORNING)
        self.afternoon = PeriodForecast(self.forecasts_raw_data, self.IDX_AFTERNOON)
        self.evening = PeriodForecast(self.forecasts_raw_data, self.IDX_EVENING)


class PeriodForecast(Forecast):
    period_idx = None

    description = ''
    wind_direction = ''
    wind_velocity = 0
    precipitation = 0

    first_sub_period = None
    second_sub_period = None

    def __init__(self, daily_raw_data, period_idx):
        self.forecasts_raw_data = daily_raw_data
        self.period_idx = period_idx
        self.load_data()

    def load_data(self):
        self.description = self.forecasts_raw_data[self.IDX_DESCRIPTION][self.period_idx]
        self.wind_direction = self.forecasts_raw_data[self.IDX_WIND][self.period_idx][self.IDX_WIND_DIRECTION]
        self.wind_velocity = self.forecasts_raw_data[self.IDX_WIND][self.period_idx][self.IDX_WIND_VELOCITY]
        self.precipitation = self.forecasts_raw_data[self.IDX_PRECIPITATION][self.period_idx]

        first_period_idx = self.get_first_sub_period_idx(self.period_idx)
        second_period_idx = self.get_second_sub_period_idx(self.period_idx)
        self.first_sub_period = HourlyForecast(self.forecasts_raw_data, first_period_idx)
        self.second_sub_period = HourlyForecast(self.forecasts_raw_data, second_period_idx)

    def __unicode__(self):
        return self.description


class HourlyForecast(Forecast):
    sub_period_idx = None

    description = ''
    temperature = None
    humidity = None

    def __init__(self, period_raw_data, sub_period_idx):
        self.forecasts_raw_data = period_raw_data
        self.sub_period_idx = sub_period_idx
        self.load_data()

    def load_data(self):
        self.description = self.SUB_PERIOD_DESCRIPTIONS[self.sub_period_idx]
        self.temperature = self.forecasts_raw_data[self.IDX_TEMPERATURE][self.sub_period_idx]
        self.humidity = self.forecasts_raw_data[self.IDX_HUMIDITY][self.sub_period_idx]

    def __unicode__(self):
        return self.description + ': ' + str(self.temperature) + ' °C, '.decode('utf-8') + str(self.humidity) + ' %'
