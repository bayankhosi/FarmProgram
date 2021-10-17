import time
import statscalc
import datetime
import pandas as pd
import openpyxl as opx
from plyer import notification

# DataFrames

df = pd.read_excel('./Files/spread.xlsx',                       # all pigs
                   sheet_name='individual',
                   index_col=0)

df_month = pd.read_excel('./Files/spread.xlsx',                 # monthly data
                         sheet_name='2021')

df_alive = df.loc[df.slaughter_date.isnull()].filter(           # living pigs
    ['ID', 'slaughter_weight', 'breed', 'meds', 'sex'])
df_alive['age'] = statscalc.today_dt - pd.to_datetime(df.birth_date)

df_slaughtered = df.loc[df.slaughter_date.isnull() == False]    # slaughtered pigs


spread = opx.load_workbook('./Files/spread.xlsx')
individual = spread.worksheets[0]
pig_id = individual['M1'].value

optimal_Age = 120        # optimal age to slaughter. Shld be calculated in statscalc

today = datetime.datetime.now().date()
Time = datetime.datetime.now().hour


class notify():

    def daily():

        notification.notify(
            title="Update Pig Data",
            message="Remember to record New Feed",
            timeout=5  # display time in sec
        )
        time.sleep(7)

    def slaughter(pig_ID, days_left):  # notifies if a pig is close to optimal slaughter age

        days = str(days_left)
        pig_id = str(pig_ID)

        notification.notify(
            title="!!!Slaughter!!!",
            message="Slaughter Pig " + pig_id + " in " + days + " days",
            timeout=5  # display time in sec
        )
        time.sleep(7)


class check():

    def age():                         # checks if any pig is close to optimal slaughter age

        for id, row in df_alive.iterrows():
            age_prediction = statscalc.stats.optimum_age(id)[0]

            days_left = datetime.timedelta(days=age_prediction) - df_alive.age[id]

            if days_left <= datetime.timedelta(days=14):    # notify 2 wks b4 best age
                pig_ID = id
                notify.slaughter(pig_ID, days_left.days)

            elif days_left == datetime.timedelta(days=0):
                days_left = 'TODAY'
                pig_ID = id
                notify.slaughter(pig_ID, days_left)


            else:
                days_left = "OVERDUE by " + str(today - datetime.timedelta(days=age_prediction))


check.age()


while (1 == 1):

    if Time == 10 or 19 or 20 or 21:  # make daily notifacations during these hours
        notify.daily()
        check.age()

    if datetime.date.today().day == 30:
        statscalc.stats.average_age()
        print('avAge')

    time.sleep(30*60)                # pauses for 30 minutes
