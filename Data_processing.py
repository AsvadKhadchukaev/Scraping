from scraper import KinoPoisk
import pandas as pd
import numpy as np
from currency_converter import CurrencyConverter
from datetime import date
import numpy as np
import pandas as pd

# This script doesn't work for now

class data_transformation(df=pd.read_csv('KinoPoisk.csv')):

    def __init__(self) -> None:
        print('Start')
    
    def dropping_columns(self):
        self.df_cleared = self.dropna(axis=1, thresh=189)
        self.df_cleared.info()
    
    def budget_transformation_to_usd(self, x):
        c = CurrencyConverter()
        currencies_signs = ['€', 'DEM', 'р.', '₽', '£', 'FRF', '¥', 'DKK']
        currencies = ['EUR', 'DEM', 'RUB', 'RUB', 'GBP', 'FRF', 'JPY', 'DKK']
        try:
            year = self.df_cleared.loc[self.df_cleared['Бюджет'] == x, 'Год производства'].values[0]
            for currency in currencies_signs:
                if type(x) == str:
                    if currency in x:
                        x = float(x.replace(currency, ''))
                        x = (c.convert(x, currencies[currencies_signs.index(currency)], 'USD', date=date(year, 1, 1)))
                    else:
                        continue
                elif type(x) != str:
                    x = str(x)
                    if currency in x:
                        x = float(x.replace(currency, ''))
                        x = (c.convert(x, currencies[currencies_signs.index(currency)], 'USD', date=date(year, 1, 1)))
                    else:
                        continue
            return x
        except:
            return x

    def budget_transformation(self):
        self.df_cleared['Бюджет'] = self.df_cleared['Бюджет'].str.replace(' ', '')
        self.df_cleared['Бюджет'] = self.df_cleared['Бюджет'].str.replace('$', '')
        self.df_cleared['Бюджет'] = self.df_cleared['Бюджет'].apply(lambda y: self.budget_transformation_to_usd(x=y))
        self.df_cleared['Бюджет'] = self.df_cleared['Бюджет'].apply(pd.to_numeric)

    def fees_usa_transformation(self):
        self.df_cleared['Сборы в США'] = self.df_cleared['Сборы в США'].str.replace(' ', '')
        self.df_cleared['Сборы в США'] = self.df_cleared['Сборы в США'].str.replace('$', '')
        self.df_cleared['Сборы в США'] = self.df_cleared['Сборы в США'].str.replace('nan', '0')
        self.df_cleared['Сборы в США'] = self.df_cleared['Сборы в США'].apply(pd.to_numeric)

    def fees_world_transformation(self):
        self.df_cleared['Сборы в мире'] = self.df_cleared['Сборы в мире'].str.replace(' ', '')
        self.df_cleared['Сборы в мире'] = self.df_cleared['Сборы в мире'].str.replace('$', '')
        self.df_cleared['Сборы в мире'] = self.df_cleared['Сборы в мире'].str.replace('+', '')
        self.df_cleared['Сборы в мире'] = self.df_cleared['Сборы в мире'].apply(lambda x: max(x.split('=')) if type(x) == str else x)
        self.df_cleared['Сборы в мире'] = self.df_cleared['Сборы в мире'].str.replace('nan', '0')
        self.df_cleared['Сборы в мире'] = self.df_cleared['Сборы в мире'].apply(pd.to_numeric)

    def views(self, x):
        list_of_symbols = [' ', 'млн.', 'тыс.', 'млн', 'тыс', 'nan']
        list_of_replacements = ['', '000000', '000', '000000', '000', '0']
        if type(x) != str:
            x = str(x)
        for symbol in list_of_symbols:
            if symbol in x:
                x = x.replace(symbol, list_of_replacements[list_of_symbols.index(symbol)])
        if '.' in x:
            x = x.replace('.', '')
            x = float(x) * (0.1)
            return int(x)
        else:
            return int(x)

    def views_transformation(self):
        self.df_cleared['Зрители'] = self.df_cleared['Зрители'].apply(self.views)
    
    def categorical_data_processing(self, column):
        all_categories = []
        for record in self.df_cleared[column]:
            new_record = record.split(',')
            for word in new_record:
                word = word.strip()
            all_categories.append(word)
        all_categories = list(set(all_categories))
        for category in all_categories:
            self.df_cleared[column + ': ' + category] = self.df_cleared[column].apply(lambda x: True if category in x else False)
            
    def categorical_data_transformation(self):
        self.categorical_data_processing(column='Жанр')
        self.categorical_data_processing(column='Страна')
        self.categorical_data_processing(column='Актеры')
        self.categorical_data_processing(column='Режиссер')
        self.categorical_data_processing(column='Сценарий')
    

    
    
    
    