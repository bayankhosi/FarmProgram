from calendar import monthrange
import datetime
import openpyxl as opx
import pandas as pd
import upload
import statscalc

date_format = '%d/%m/%Y'
today = datetime.datetime.now().date()
month = datetime.datetime.now().month                           # month number
year = datetime.datetime.now().year                             # year

spread = opx.load_workbook('./Files/spread.xlsx')

# opens current year sheet
individual = spread.worksheets[0]
whole = spread.worksheets[year - 2020]
# total number of pigs
population = int(whole.cell(column=2, row=month + 1).value)
pig_id = individual['M1'].value


def buy_age(population, pig_id):                                 # recording new piglets

    population += 1     # add to number of pigs
    whole.cell(column=2, row=month + 1).value = population
    # to ensure nxt mnt pop not 0
    whole.cell(column=2, row=month + 2).value = population

    pig_id += 1
    individual['M1'].value = pig_id
    rw = pig_id + 1
    individual.cell(row=rw, column=1).value = pig_id
    print("\nThe pig's ID is: ", pig_id)

    sex = int(input("\nEnter sex of piglet \nMale(1), Female(0): \n"))
    individual.cell(row=rw, column=12).value = sex
    age_bought = int(input("\nEnter Age of piglet (weeks): "))
    purchase_date = today         # code to record date
    date_born = purchase_date - datetime.timedelta(days=7 * age_bought)
    individual.cell(row=rw, column=11).value = purchase_date
    individual.cell(row=rw, column=2).value = date_born

    purchase_price = int(input("\nEnter purchase price: "))
    individual.cell(row=rw, column=3).value = purchase_price

    breed = str(input("""
        Choose Breed:
            n = Ncane
            m = Mngometulu
            t = Motjane
        """))
    individual.cell(row=rw, column=8).value = breed

    individual.cell(row=rw, column=10).value = 0


def consumables():                                               # resources spent on well being
    """ Record:
            population each month
            average age each month
            feed each month """

    consumable_choice = int(
        input("\nWhich Consumable are you recording?\n1.Feed\n2.Miscelleneous\n3.Medicine\n"))

    if consumable_choice == 1:
        print("\nEnter mass of feed bought (Kg)")
        feed_weight = int(input()) + whole.cell(column=3, row=month+1).value
        # record the amount
        whole.cell(column=3, row=month+1).value = feed_weight

        print("\nEnter price of feed bought (E)")
        feed_price = int(input()) + whole.cell(column=4, row=month+1).value
        whole.cell(column=4, row=month+1).value = feed_price

        FeedPerPig = whole.cell(column=3, row=month + 1).value / \
            whole.cell(column=2, row=month + 1).value
        whole.cell(column=5, row=month + 1).value = FeedPerPig

    elif consumable_choice == 2:
        print("\nEnter price of item (E)")
        misc_price = int(input()) + whole.cell(column=5, row=month+1).value
        whole.cell(column=5, row=month+1).value = misc_price

    elif consumable_choice == 3:
        pig_id = int(input("Enter ID of pig medicating: "))
        rw = pig_id + 1
        med = float(input("Enter amount of medication (ml): "))

        individual.cell(row=rw, column=9).value = med


def sale(population):                                            # info on slaughter and sale
    # make averages for that individual pig available
    # profit on the pig by subtracting average spend on it

    pig_id = int(input("\nEnter ID of Pig Slaughtered: "))
    rw = pig_id + 1

    # check if there is non recorded slaughter for pig_id

    if individual.cell(row=rw, column=4).value == None:

        # subtract from number of pigs
        population -= 1
        whole.cell(column=2, row=month + 1).value = population
        # to ensure nxt mnt pop not 0
        whole.cell(column=2, row=month + 2).value = population
        print("\nNew Population: ", population)

        # record date of slaughter
        slaughter_date = today
        individual.cell(row=rw, column=4).value = slaughter_date

        # record slaughter age
        date_born = datetime.datetime.date(
            individual.cell(row=pig_id + 1, column=2).value)
        slaughter_age = int((today - date_born).days)
        print("\nEnter Slaughter Age of pig: ", slaughter_age, "days")
        individual.cell(row=rw, column=6).value = int(slaughter_age)

        # record slauhgter mass
        slaughter_weight = float(input("\nEnter Slaughter Weight of pig: "))
        individual.cell(row=rw, column=5).value = slaughter_weight
        price_Kg = float(input("\nPrice per Kg: "))
        sale_price = slaughter_weight * price_Kg
        individual.cell(row=rw, column=7).value = sale_price

        # estimate of total food mass eaten
        purchase_date = individual.cell(row=rw, column=11).value
        month_bought = purchase_date.month - 1
        month_slaughtered = today.month

        # don't count month feed if bought after mid-month
        if purchase_date.day > 15:
            month_bought += 1

        # don't count month feed if slaughtered before mid-month
        if today.day < 15:
            month_slaughtered -= 1

        df_month = pd.read_excel('./Files/spread.xlsx',
                                 sheet_name='2021',
                                 index_col=0)
        df_month['feed_per_pig'] = df_month.feed_mass / df_month.population

        feed_eaten = df_month[month_bought: month_slaughtered]['feed_per_pig'].sum(
        )
        individual.cell(row=rw, column=10).value = feed_eaten

    else:
        print("\nThis ID is for a pig that has already been slaughtered.\nTry again.")


def monitor():                                                   # view collected data

    View = int(
        input("""
            View data for: 
                1. Individual Pig   
                2. Whole Month Data
                3. Statistics 
        """))

    if View == 1:       # individual pig data
        pig_id = int(input("\nEnter ID of pig you want to view: "))

        purchase_date = datetime.datetime.date(individual.cell(
            row=pig_id + 1, column=2).value)

        date_born = datetime.datetime.date(
            individual.cell(row=pig_id + 1, column=2).value)

        print("\nDate Born: ", purchase_date)

        print("\nPurchase Price: E", individual.cell(
            row=pig_id + 1, column=3).value)

        if individual.cell(row=pig_id + 1, column=6).value == None:
            currAge = (today-date_born).days
            print("\nAge:  ", currAge, "days")
        else:
            print("\nSlaughter Age:  ", individual.cell(
                row=pig_id + 1, column=6).value, "days")
            print("\nSlaughter Weight:  ", individual.cell(
                row=pig_id + 1, column=5).value, "Kg")
            print("\nSale Price:  E", individual.cell(
                row=pig_id + 1, column=7).value)
            print("\nFeed Eaten: ", individual.cell(
                row=pig_id + 1, column=10).value)

    elif View == 2:     # month data
        month = int(input("\nEnter month number you want to view: "))

        avAge = whole.cell(column=6, row=month + 1).value

        Population = whole.cell(column=2, row=month + 1).value

        FeedMass = whole.cell(column=3, row=month + 1).value

        FeedPerPig = whole.cell(column=3, row=month + 1).value / population

        FeedPrice = whole.cell(column=4, row=month + 1).value

        print("\nData for", whole.cell(column=1, row=month + 1).value)

        print("\nPopulation:   ", Population)

        print("\nAverage Age:   ", avAge)

        print("\nFeed Mass Bought:   ", FeedMass, "Kg")

        print("\nAverage feed per pig: ", FeedPerPig, "Kg/pig")

        print("\nPrice of feed:  E", FeedPrice)
        
    elif View == 3:     # statistics
        graph = int(input(("""
            Choose a graph
                1. Mass-Age
        """)))
        if graph == 1:
            statscalc.stats.mass_age()

        """ if graph == 2:
            statscalc.stats.feed_age() """

loop = 2
while loop == 2:
    action = int(input("""************************************************************************
            These are the operations that can be performed\n
            [1] - Record New Piglet
            [2] - Record Bought Consumable(s)
            [3] - Record Slaughter and Sale
            [4] - View Data
        """))

    if action == 1:

        buy_age(population, pig_id)

    elif action == 2:
        consumables()

    elif action == 3:

        sale(population)

    elif action == 4:
        monitor()

    elif action == 5:
        try:
            upload.main()
        except:
            print("Couldn't upload")

    spread.save('./Files/spread.xlsx')
    loop = int(input("\n1. Exit, 2. For Other Operation: ",))
    print("************************************************************************")


try:
    upload.main()
except:
    print("Couldn't upload")
