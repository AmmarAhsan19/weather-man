''' Modules to import '''
import datetime
import argparse
import os
import re

# ======================================================================== >>
def get_months(choice):
    '''
    Function to get the month_names
    '''
    months_abriviation = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',\
                'Sep', 'Oct', 'Nov', 'Dec']
    month_full_form = ['January', 'February', 'March', 'April',\
                'May', 'June', 'July', 'August',\
                'September', 'October', 'November', 'December']

    if choice == 1:
        return months_abriviation
    elif choice == 2:
        return month_full_form
    else:
        return None

# ======================================================================== >>
def check_valid_date(date):
    '''
    Function to check if the date is valid
    '''
    try:
        parts = date.split('/')
        if len(parts) == 1:
            datetime.datetime.strptime(date, '%Y')
        elif len(parts) == 2:
            datetime.datetime.strptime(date, '%Y/%m')
        else:
            raise ValueError("Invalid date format")
    except ValueError:
        print("\n-------------------------------")
        print(" Invalid date format")
        print("-------------------------------\n")
        return False
    else:
        return True

# ======================================================================== >>
def check_valid_directory(path):
    '''
    Function to check the directory if there 
    is any file in formate 
    (<cityName>_weather_<year>_MMM<month>.txt)
    '''
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        print("\n-------------------------------")
        print(" Invalid directory")
        print("-------------------------------\n")
        return 0

    reg = r'(\w+)_weather_(\d{4})_(\w{3})\.txt'
    for name in files:
        if name.endswith('.txt'):
            match = re.search(reg, name)
            if match:
                return True
    print("\n----------------------------------------------")
    print("There is no any valid file in the directory")
    print("----------------------------------------------\n")

    return False

# ======================================================================== >>
def check_valid_file(file_name):
    '''
    Function to check if the file is valid
    '''
    reg = r'(\w+)_weather_(\d{4})_(\w{3})\.txt'
    match = re.search(reg, file_name)
    if match:
        return True
    return False

# ======================================================================== >>
def extract_data_from_list_of_lists(lists):
    '''
        Extract the date from the file name 
        (date, max temp, 
        avg temp, min temp, 
        max hum, avg hum, min hum)
    '''
    filtered_list = []
    for lst in lists:
        ls = lst.split(',')
        dt = ls[0]
        maxt = ls[1]
        avgt = ls[2]
        mint = ls[3]
        maxh = ls[7]
        avgh = ls[8]
        minh = ls[9]
        filtered_list.append([dt, maxt, avgt, mint, maxh, avgh, minh])
    # replace string with the float and date with the datetime object
    # handle invalid data and put -1 at that place
    for ls in filtered_list:
        y,m,d = ls[0].split('-')
        ls[0] = datetime.datetime(int(y), int(m), int(d))
        for i in range(1, 7):
            try:
                ls[i] = float(ls[i])
            except ValueError:
                ls[i] = -1
    return filtered_list

# ======================================================================== >>
def read_data_of_file(file_name):
    '''
    Function to read the data of a file
    '''
    check = check_valid_file(file_name)
    if not check:
        return False

    try:
        encoding_type = 'utf-8'
        with open(file_name, 'r', encoding=encoding_type) as file:
            data = file.readlines()
            # removing first header line
            data.pop(0)

            lists = [row for row in data if len(row.split(',')) == 23]

            filtered_list = extract_data_from_list_of_lists(lists)

            return filtered_list

    except FileNotFoundError as error:
        print("\n-------------------------------")
        print(" File not found")
        print("-------------------------------\n")
        print(error)
        return False

# ======================================================================== >>
def gen_data_for_year(path, year):
    '''
    Generator Funtion to get the all the files of a year from the 
    directory and yeild the list of list of data
    '''
    files = os.listdir(path)
    reg = r'(\w+)_weather_(\d{4})_(\w{3})\.txt'
    for name in files:
        if name.endswith('.txt'):
            match = re.search(reg, name)
            if match:
                # check if the year is same
                if match.group(2) == year:
                    file_name = os.path.join(path, name)
                    data = read_data_of_file(file_name)
                    if data:
                        yield data
                    else:
                        print("\n-------------------------------")
                        print(" Invalid file")
                        print("-------------------------------\n")
                        return False
    return True

# ======================================================================== >>
def gen_data_for_month(path, year, month):
    '''
    Generator Funtion to get the all the files of a month from the 
    directory and yeild the list of list of data
    '''
    files = os.listdir(path)
    reg = r'(\w+)_weather_(\d{4})_(\w{3})\.txt'
    for name in files:
        if name.endswith('.txt'):
            match = re.search(reg, name)
            if match:
                # check if the year and month is same
                if match.group(2) == year and match.group(3) == month:
                    file_name = os.path.join(path, name)
                    data = read_data_of_file(file_name)
                    if data:
                        yield data
                    else:
                        print("\n-------------------------------")
                        print(" Invalid file")
                        print("-------------------------------\n")
                        return False
    return True

# ======================================================================== >>
def excecute_exact_command(path, year):
    '''
    Function will calculate the for a given year 
    display the highest temperature and day, lowest
    temperature and day, most humid day and humidity.

    python3 weatherman.py -e 2005/6 /path/to/files

    Highest: 45C on June 23
    Lowest: 01C on December 22
    Humid: 95% on August 14
    '''
    count = 0
    highest_temperature = [-280, 0, 0] # temp, date, month
    lowest_temperature = [200, 0, 0] # temp, date, month
    highest_hum = [0, 0, 0] # hum, date, month

    for data in gen_data_for_year(path, year):
        for row in data:
            if row[1] > highest_temperature[0]:
                highest_temperature[0] = row[1]
                highest_temperature[1] = row[0].day
                highest_temperature[2] = row[0].month
            if row[3] < lowest_temperature[0]:
                lowest_temperature[0] = row[3]
                lowest_temperature[1] = row[0].day
                lowest_temperature[2] = row[0].month
            if row[4] > highest_hum[0]:
                highest_hum[0] = row[4]
                highest_hum[1] = row[0].day
                highest_hum[2] = row[0].month
            count += 1

    month_names = get_months(2)

    print("\n----------------------------------------------")
    if count == 0:
        print("There is no data for this year")
    else:
        print(f"Highest: {highest_temperature[0]}C on \
{month_names[highest_temperature[2]-1]} {highest_temperature[1]} ")
        print(f"Lowest: {lowest_temperature[0]}C on \
{month_names[lowest_temperature[2]-1]} {lowest_temperature[1]} ")
        print(f"Humid: {highest_hum[0]}% on \
{month_names[highest_hum[2]-1]} {highest_hum[1]} ")
    print("----------------------------------------------\n")

# ======================================================================== >>
def excecute_average_command(path, year, month):
    '''
    Function will calculate the For a given month display the 
    average highest temperature, average lowest temperature, average humidity
    
    python3 weatherman.py -a 2005/6 /path/to/files
    
    Highest Average: 39C
    Lowest Average: 18C
    Average Humidity: 71%
    '''

    month_names = get_months(1)

    highest_avg_temp = 0
    lowest_avg_temp = 0
    avg_hum = 0

    count = 0
    for data in gen_data_for_month(path, year, month_names[int(month)-1]):
        for row in data:
            highest_avg_temp += row[1]
            lowest_avg_temp += row[3]
            avg_hum += row[4]
            count += 1

    highest_avg_temp /= count
    lowest_avg_temp /= count
    avg_hum /= count

    print("\n----------------------------------------------")
    if count == 0:
        print("There is no data for this month and year")
    else:
        print(f"Highest Average: {highest_avg_temp:.2f}C")
        print(f"Lowest Average: {lowest_avg_temp:.2f}C")
        print(f"Average Humidity: {avg_hum:.2f}%")
    print("----------------------------------------------\n")

# ======================================================================== >>
def display_chart_command(path, year, month):
    '''
    Function for a given month to give 
    tuple of highest temperature, lowest temperature, count of data
    '''
    highest_temperature = []
    lowest_temperature = []
    count = 0
    month_names = get_months(1)
    for data in gen_data_for_month(path, year, month_names[int(month)-1]):
        for row in data:
            highest_temperature.append([row[0].day, row[1]])
            lowest_temperature.append([row[0].day, row[3]])
            count += 1

    highest_temperature.sort(key=lambda x: x[0])
    lowest_temperature.sort(key=lambda x: x[0])

    return ((highest_temperature, lowest_temperature, count))

# ======================================================================== >>
def display_bar(path, year, month):
    '''
    Function to draw two horizontal bar charts on the 
    console for the highest and lowest temperature on each day. 
    Highest in red and lowest in blue.

    python3 weatherman.py -c 2011/03 /path/to/files
    
    March 2011
    01 ++++++++++++++++++++++++ 25C
    01 +++++++++++ 11C
    02 +++++++++++++++++++++ 22C
    02 ++++++++ 08C
    '''
    tupl = display_chart_command(path, year, month)
    highest_temperature = tupl[0]
    lowest_temperature = tupl[1]
    count = tupl[2]

    print("\n----------------------------------------------")
    print(f"{get_months(2)[int(month)-1]} {year}\n")
    if count == 0:
        print("There is no data for this month and year")
    else:
        for i in enumerate(highest_temperature):
            print(f"{highest_temperature[i[0]][0]:02} \033[91m\
{'+'*int(highest_temperature[i[0]][1])} \033[0m{highest_temperature[i[0]][1]}C")
            print(f"{lowest_temperature[i[0]][0]:02} \033[94m\
{'+'*int(lowest_temperature[i[0]][1])} \033[0m{lowest_temperature[i[0]][1]}C")
    print("----------------------------------------------\n")

# ======================================================================== >>
def display_bar_bounus(path, year, month):
    '''
    Function for a given month draw one horizontal bar chart on the console 
    for the highest and lowest temperature on each day. Highest in red and 
    lowest in blue.

    python3 weatherman.py -c 2011/3 /path/to/files
    March 2011
    01 +++++++++++++++++++++++++++++++++++ 11C - 25C
    02 +++++++++++++++++++++++++++++ 08C - 22C
    '''

    tupl = display_chart_command(path, year, month)
    highest_temperature = tupl[0]
    lowest_temperature = tupl[1]
    count = tupl[2]

    print("\n----------------------------------------------")
    print(f"{get_months(2)[int(month)-1]} {year}\n")
    if count == 0:
        print("There is no data for this month and year")
    else:
        for i in enumerate(highest_temperature):
            print(f"{highest_temperature[i[0]][0]:02} \
\033[94m{'+'*int(lowest_temperature[i[0]][1])}\
\033[91m{'+'*int(highest_temperature[i[0]][1])}\
\033[0m {lowest_temperature[i[0]][1]:.0f}C - {highest_temperature[i[0]][1]:.0f}C ")
    print("----------------------------------------------\n")

# ======================================================================== >>
def main():
    '''
    main function 
    Description: Parse the arguments and do the main function
    '''
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--extract",
                        help="extract data for year",
                        action="store_true")
    group.add_argument("-a", "--average",
                        help="average data of a month",
                        action="store_true")
    group.add_argument("-c", "--chart",
                        help="display chart for the month",
                        action="store_true")

    parser.add_argument("year" ,
                        help="year/month of data <YYYY or YYYY/MM>")
    parser.add_argument("path",
                        help="path to data",)
    args = parser.parse_args()

    if not check_valid_date(args.year) or\
        not check_valid_directory(args.path):
        return None

    # Execute the command -e
    if args.extract:
        if args.year.find('/') == -1:
            excecute_exact_command(args.path, args.year)
        else:
            dat = args.year.split('/')
            year = dat[0]
            excecute_exact_command(args.path, year)

    # Execute the command -a
    if args.average:
        if args.year.find('/') == -1:
            print("\n-------------------------------")
            print(" Invalid command")
            print("-------------------------------\n")
            return None
        else:
            dat = args.year.split('/')
            year = dat[0]
            month = dat[1]
            excecute_average_command(args.path, year, month)

    # Execute the command -c
    if args.chart:
        if args.year.find('/') == -1:
            print("\n-------------------------------")
            print(" Invalid command")
            print("-------------------------------\n")
            return None
        else:
            dat = args.year.split('/')
            year = dat[0]
            month = dat[1]
            display_bar_bounus(args.path, year, month)


# ======================================================================== >>
if __name__ == "__main__":
    main()
