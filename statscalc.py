import datetime
from calendar import monthrange
import openpyxl as opx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

# Dates

today = datetime.date.today()
today_dt = datetime.datetime.fromordinal(today.toordinal())
month = today.month
year = int(today.year)

# Openpyxl

spread = opx.load_workbook('./Files/spread.xlsx')
individual = spread.worksheets[0]
whole = spread.worksheets[1]

population = int(whole.cell(column=2, row=month + 1).value)
pig_id = individual['J1'].value

# DataFrames

df = pd.read_excel('./Files/spread.xlsx',                       # all pigs
                   sheet_name='individual',
                   index_col=0)

df_month = pd.read_excel('./Files/spread.xlsx',                 # monthly data
                         sheet_name='2021')

df_alive = df.loc[df.slaughter_date.isnull()].filter(           # unslaughtered pigs
    ['ID', 'birth_date', 'purchase_price'])
df_alive['age'] = today_dt - pd.to_datetime(df.birth_date)

# slaughtered pigs
df_slaughtered = df.loc[df.slaughter_date.isnull() == False]


class stats():
    # find how much food does a pig eat in its lifetime

    def mass_age():              # slaughter mass - age graph

        sns.regplot(x=df_slaughtered.slaughter_age,
                    y=df_slaughtered.slaughter_weight
                    ).set_title('Mass - Age')
        plt.show()

    def average_age():      # should be done ev half of month

        month = today.month

        day = monthrange(2021, today.month)[1]//2

        mid_month = today - datetime.timedelta(days=today.day + day)

        df_alive['mid_month_age'] = (datetime.datetime.fromordinal(
            mid_month.toordinal()) - pd.to_datetime(df.birth_date))

        df_alive['mid_month_age'] = (df_alive['mid_month_age']).dt.days

        avAge = int(df_alive.mid_month_age.mean())

        whole.cell(column=6, row=month + 1).value = avAge
        spread.save('./Files/spread.xlsx')

    def optimum_age():
        # the use of decision tree regressor to estimate slaughter_age

        # Our target variable
        y = df_slaughtered.slaughter_age

        # Our features
        features = ['slaughter_weight', 'meds']
        X = df_slaughtered[features]

        train_X, val_X, train_y, val_y = train_test_split(
            X, y, random_state=1)

        # calling model
        age_model = XGBRegressor(random_state=1)

        # fitting data into model
        age_model.fit(X, y)

        # prediction
        age_prediction = age_model.predict(val_X)

        return age_prediction


# print(stats.optimum_age())

# print(stats.average_age())

# stats.mass_age()
