import datetime
from calendar import monthrange
import openpyxl as opx
import numpy as np
import matplotlib.pyplot as plt

today = datetime.datetime.now().date()                          # date
month = int(datetime.datetime.now().strftime("%m"))             # month number
year = int(datetime.datetime.now().strftime("%Y"))              # Year

spread = opx.load_workbook('./Files/spread.xlsx')
individual = spread.worksheets[0]
whole = spread.worksheets[1]
population = int(whole.cell(row=2, column=month + 1).value)     # total number of pigs
pig_id = individual['L1'].value



class stats():
    # how much food does a pig eat in its lifetime

    def mass_age():         # slaughter mass - age graph

        mass = []
        age = []

        for row in individual.rows:
            y = row[5].value
            age.append(y)

            x = row[4].value
            mass.append(x)

        age.pop(0)
        age = list(filter(None, age))
        age.sort()

        mass.pop(0)
        mass = list(filter(None, mass))
        mass.sort()

        plt.scatter(age, mass, c='blue', marker='x', s=100)
        plt.plot(age, mass, color='red', linewidth=2)
        plt.xlabel('Age')
        plt.ylabel('Mass')
        plt.title('Mass - Age')
        plt.show()                   # Display the plot """

    def feed_age():         # mass of population * feed against average age
        popu_feed = []
        age = []

        for col in whole.columns:
            y = col[5].value
            age.append(y)

            x = col[7].value
            popu_feed.append(x)

        age.pop(0)
        age = list(filter(None, age))
        age.sort()
        age_arr = np.array(age)

        popu_feed.pop(0)
        popu_feed = list(filter(None, popu_feed))
        popu_feed.sort()
        popu_feed_arr = np.array(popu_feed)

        plt.scatter(age, popu_feed, c='blue', marker='x', s=100)
        plt.plot(age, popu_feed, color='red', linewidth=2)
        plt.xlabel('Average Age (Days)')
        plt.ylabel('popu_feed (Kg/Age/Pig)')
        plt.title('popu_feed - Age')
        plt.show()                   # Display the plot """

    def average_age(month):      # should be done ev half of month

        mnth = str(monthrange(2021, month)[1]//2)
        monthEnd = "2021/0" + str(month) + "/" + mnth
        monthEnd = datetime.datetime.strptime(monthEnd, '%Y/%m/%d')
        monthEnd = datetime.datetime.date(monthEnd)

        ro = 0
        totAge = 0

        for row in individual.iter_rows(min_row=0, max_row=pig_id + 1):
            y = row[5].value
            ro += 1

            if y == None:
                date_born = datetime.datetime.date(
                    individual.cell(row=ro, column=2).value)
                currAge = (monthEnd-date_born).days
                totAge += currAge

        avAge = totAge/population
        whole.cell(row=6, column=month + 1).value = avAge

        """ FeedPerAgePig = whole.cell(
            row=2, column=month + 1).value * whole.cell(row=3, column=month + 1).value/avAge
        whole.cell(row=8, column=month + 1).value = FeedPerAgePig """

        return avAge
