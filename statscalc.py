import datetime
from calendar import monthrange
import openpyxl as opx
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split


today = datetime.datetime.now()                          # date
month = int(datetime.datetime.now().strftime("%m"))             # month number
year = int(datetime.datetime.now().strftime("%Y"))              # Year

spread = opx.load_workbook('./Files/spread.xlsx')
individual = spread.worksheets[0]
whole = spread.worksheets[1]
population = int(whole.cell(column=2, row=month + 1).value)     # total number of pigs
pig_id = individual['H1'].value

df = pd.read_excel('./Files/spread.xlsx', 
                   sheet_name= 'individual')
df_month = pd.read_excel('./Files/spread.xlsx', 
                         sheet_name= '2021')
df_alive = df.loc[df.slaughter_date.isnull()].filter(
    ['ID', 'birth_date', 'purchase_price'])
df_slaughtered = df.loc[df.slaughter_date.isnull()==False]



class stats():
    # find how much food does a pig eat in its lifetime

    def mass_age():              # slaughter mass - age graph

        """ df_slaughtered.plot(kind= 'scatter',
        x= 'slaughter_age',
        y= 'slaughter_weight')
        plt.show() """
        plt.scatter(x=df_slaughtered.slaughter_age,
                    y=df_slaughtered.slaughter_weight,
                    )
        plt.gca().update(dict(title= "Mass-Age Graph",
                        xlabel= "Slaughter Age (days)",
                        ylabel= "Slaughter Mass (Kg)"))
        plt.show()


    def average_age(month):      # should be done ev half of month

        """df_alive['age'] = today - pd.to_datetime(df.birth_date)

        avAge = df_alive.age.mean()"""

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


        return avAge


    def optimum_age():
        # the use of decision tree regressor to estimate slaughter_age

        # Our target variable
        y = df_slaughtered.slaughter_age

        # Our features
        features = ['slaughter_weight']
        X = df_slaughtered[features]

        train_X, val_X, train_y, val_y = train_test_split(
            X, y, random_state=1)

        # calling model
        age_model = DecisionTreeRegressor(random_state=1)

        # fitting data into model
        age_model.fit(X, y)

        # prediction
        age_prediction = age_model.predict(val_X)

        return age_prediction

# print(stats.optimum_age())