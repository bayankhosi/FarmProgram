import time
import statscalc
import datetime
import openpyxl as opx
from plyer import notification

spread = opx.load_workbook('./Files/spread.xlsx')
individual = spread.worksheets[0]
pig_id = individual['L1'].value

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
            message="Slaughter Pig " + pig_id + " in " + days,
            timeout=5  # display time in sex
        )
        time.sleep(7)


class check():

    def age():                         # checks if any pig is close to optimal slaughter age
        ro = 1

        rec_days = datetime.timedelta(days=optimal_Age)

        for Row in individual.iter_rows(min_row=2, max_row=pig_id+1):
            ro += 1

            date_born = datetime.datetime.date(
                individual.cell(row=ro, column=2).value)

            best_day = date_born + rec_days

            y = Row[5].value

            if y == None:                                       # checks if pig alive
                days_left = best_day - today


                if days_left <= datetime.timedelta(days=14):    # notify 2 wks b4 best age
                    pig_ID = individual.cell(row=ro, column=1).value
                    notify.slaughter(pig_ID, days_left)

                elif days_left == datetime.timedelta(days=0):
                    days_left = 'TODAY'
                    pig_ID = individual.cell(row=ro, column=1).value
                    notify.slaughter(pig_ID, days_left)

                else:
                    days_left = "OVERDUE by " + str(today - best_day)



a = 1

while a == 1:

    if Time == 10 or 19 or 20 or 21:  # make daily notifacations during these hours
        notify.daily()
        check.age()

    if datetime.date.today().day == 30:
        statscalc.stats.average_age()
        print('avAge')

    time.sleep(30*60)                # pauses for 30 minutes


# daily noty
