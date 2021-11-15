from calendar import monthrange
import datetime
import openpyxl as opx
import pandas as pd
import upload
import statscalc

fmt = '%d/%m/%Y'
today = datetime.datetime.now().date()
month = datetime.datetime.now().month                           # month number
year = datetime.datetime.now().year                             # year

Crops = opx.load_workbook('./Files/crops.xlsx')

# opens current year sheet
crops = Crops.worksheets[0]
#fields = Crops.worksheets[year - 2020]

class veggie():

    def planting():

        crop = str(input("Enter name of crop (small letters):\n\t"))
        crops.cell(row=2, column=1).value = crop

        field = str(input("Enter field number:\n\t"))
        crops.cell(row=2, column=2).value = field

        # date
        crops.cell(row=2, column=3).value = today.strftime(fmt)

        age = int(input("Enter seedling age in weeks:\n\t"))
        crops.cell(row=2, column=4).value = 7*age


    def harvest():

        field = int(input("Enter field number harvested:\n\t"))
        for i in crops.rows:
            if (crops.cell(row=2, column=2).value == field) and (crops.cell(row=2, column=9).value == None):
                print('kak')


class field():

    def work():
        type = int(input("""            1. Fertilization
            2. Tillage\n"""))

        if type == 1:
            print('Fert')
            
        elif type == 2:
            print('Till')


# harvest()
#print(crops.cell(row=2, column=9).value)
field.work()
#veggie.planting()
Crops.save('./Files/crops.xlsx')
