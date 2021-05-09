import datetime
import openpyxl as opx

spread = opx.load_workbook('spread.xlsx')
individual = spread.worksheets[0]
whole = spread.worksheets[1]

today = datetime.datetime.now().date()   # date
month = int(datetime.datetime.now().strftime("%m"))  # month number
# total number of pigs
population = whole.cell(row=2, column=month + 1).value
print(population)


def buy_age():      # option to check current age
    age_bought = int(input("Age of piglet(weeks): "))
    date_born = purchase_date - datetime.timedelta(days=7 * age_bought)
    individual.cell(row=rw, column=2).value = date_born

    purchase_price = int(input("Enter purchase price: "))
    individual.cell(row=rw, column=3).value = purchase_price

    print("Population: ", population)  # , '\n', "Piglet born: ",date_born)

    return


def consumables():  # kak spent on well being
    """ Record:
            population each month
            average age each month
            feed each month """

    consumable_choice = int(input("1.Feed   2.Miscelleneous: "))
    if consumable_choice == 1:
        print("Enter amount of feed bought (Kg)")
        feed_weight = int(input())
        # record the amount
        # av feed per weeek
        # av feed per pig
        print(feed_weight)
    elif consumable_choice == 2:
        print("Enter price of item")
        misc_price = int(input())
        print(misc_price)
        # find average per quarter


def sale():
    # mark that number of pigs has decreased
    # make averages for that individual pig available
    # profit on the pig by subtracting av spend on it
    individual.cell(row=rw, column=5).value = slaughter_weight
    price_Kg = float(input("Price per Kg: "))
    sale_price = slaughter_weight * price_Kg
    individual.cell(row=rw, column=7).value = sale_price

    print("Population: ", population)


print("What action are you recording?", '\n',
      "1. Bought Piglet 2. Bought Consumable 3. Sale")

action = int(input())

if action == 1:
    population += 1     # add to number of pigs
    whole.cell(row=2, column=month + 1).value = population
    # to ensure nxt mnt pop not 0
    whole.cell(row=2, column=month + 2).value = population
    
    pig_id = int(input("Enter Pig ID: "))
    rw = pig_id + 1
    individual.cell(row=rw, column=1).value = pig_id

    purchase_date = today         # code to record date
    buy_age()

elif action == 2:
    consumables()

elif action == 3:
    population -= 1     # add to number of pigs
    whole.cell(row=2, column=month + 1).value = population
    # to ensure nxt mnt pop not 0
    whole.cell(row=2, column=month + 2).value = population

    pig_id = int(input("Enter Pig ID: "))
    rw = pig_id + 1

    slaughter_date = today
    individual.cell(row=rw, column=4).value = slaughter_date
    slaughter_weight = float(input("Slaughter Weight of pig: "))
    sale()

spread.save('spread.xlsx')