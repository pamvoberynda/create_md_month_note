# the stucture of the code
# 1. data
# 2. calendar creation
# 3. interface and output
# 4. main()

# ----- data -----
LANGUAGE = ("Украӣнська (максимовичēвка)", "Українська (сучасна)", "English")
LANG_IDX = 0
WEEKDAYS = (("Недѣля","Понедѣлокъ","Вōвторокъ",
            "Середа","Четверъ","Пятниця","Субота"),
            ("Неділя", "Понеділок", "Вівторок",
             "Середа", "Четвер", "Пʼятниця", "Субота"),
            ("Sunday", "Monday", "Tuesday",
             "Wednesday", "Thursday", "Friday", "Saturday"))
STARTWEEKDAY = (WEEKDAYS[0][0], WEEKDAYS[1][0], WEEKDAYS[2][0])
YEAR = 2026
FIRSTDAYYEAR = (WEEKDAYS[0][4],WEEKDAYS[1][4],WEEKDAYS[2][4])
COMMON_MONTHS = [31, 28, 31, 30,
              31, 30, 31, 31,
              30, 31, 30, 31]
LEAP_MONTHS = [31, 29, 31, 30,
              31, 30, 31, 31,
              30, 31, 30, 31]
MONTHS_NAME = (("Сѣчень", "Лютый", "Березень",
               "Квѣтень", "Травень", "Червень",
               "Липень", "Серпень", "Вересень", 
               "Жовтень", "Листопадъ", "Грудень"),
               ("Січень", "Лютий", "Березень",
               "Квітень", "Травень", "Червень",
               "Липень", "Серпень", "Вересень", 
               "Жовтень", "Листопад", "Грудень"),
               ("January", "February", "March",
                "April", "May", "June",
                "July", "August", "September",
                "October", "November", "December"))

STRUCTURE_NOTE = (("Очѣкування", "Розкладъ", "Пōдсумокъ"),
                  ("Очікування", "Розклад", "Підсумок"),
                  ("Expectations", "Schedule", "Summing up"))
WORD_WEEK = ("тыждень", "тиждень", "week")
def h_md(h: int, string: str) -> str: #format headers in markdown
    format = "#"*h
    string = f"{format} {string}"
    return string
# _____ end _____


# ----- creating calendar functions -----

# create list of tuples, where (x, y, z)
# x is day of month, y is day of week, z is month's index (starts at 0, ends at 11)
def create_calen(firstdayyear: str, year_type: int, lang: int) -> list:
    calendar = []
    month_num = 0
    startcountday = WEEKDAYS[lang].index(firstdayyear)
    while month_num < 12:
        current_day = 0
        while current_day < year_type[month_num]:
            dayindex = (startcountday+current_day)%7
            calendar.append((current_day, WEEKDAYS[lang][dayindex], month_num))
            current_day += 1
        startcountday = dayindex+1
        month_num+=1
    return calendar

# distribute days from create_calen() by weeks, acconting with chosen start day of week (sunday is default)
def distribute_weeks(calendar: list, startweekday: str) -> list:
    all_weeks = []
    firstweek_year = []
    week_count = 1
    calen_len = len(calendar)
    i = 0
    j = 0
    if calendar[0][1] != startweekday:
        while calendar[i][1] != startweekday:
            firstweek_year.append(calendar[i])
            i += 1
        all_weeks.append(firstweek_year)
    else:
        week_count = 0
    while week_count < 52:
        z = 0
        week_list = []
        while z%8 < 7 and j+i < calen_len:
            week_list.append(calendar[j+i])
            z += 1
            j += 1
        all_weeks.append(week_list)
        week_count+= 1
    return all_weeks

# consider one week and inform is there more days of current month or not. it helps to define to which month distribute a week (current or next)
def count_diff_days(week: list, kind: int) -> int:
    kind_count = 0
    for day in week:
        if day[2] == kind:
            kind_count+=1
    return kind_count

# recieve distribute_weeks() result and transform it to good-looking months note based on unity of week
def goodlike_months(all_weeks: list, minday: int = 3) -> list:
    goodlike_months_list = []
    month_num = 0
    while month_num < 12:
        month_list = []
        for week in all_weeks:
            if count_diff_days(week, month_num) > minday:
                month_list.append(week)
        goodlike_months_list.append(month_list)
        month_num += 1

    return goodlike_months_list

# additional func to get list of days of standard month. is not using in the code but is honorable mentioned
def get_month_weeks(calendar: list, month_num: int) -> list:
    month_list = [day for day in calendar if day[2] == month_num]
    return month_list

# _____ end _____

# ----- interface and output -----
def abs_val(num):
    if num < 0:
        num = -1*num
    return num

def sum_list(liste: list) -> int:
    sum = int()
    for elem in liste:
        sum += elem
    return sum

def def_type_year(year: int) -> int: #is it leap or common
    yeartype = 0
    if year%4 == 0:
        if year%400 == 0:
            yeartype = 29
        elif year%100 == 0:
            yeartype = 28
        else:
            yeartype = 29
    else:
        yeartype = 28
    return yeartype #28 for common, 29 for leap 

def create_output(month_num, lang=0, year=YEAR, startweekday=STARTWEEKDAY[0], firstdayyear=FIRSTDAYYEAR[0]) -> str:
    output = str()
    year_type = COMMON_MONTHS if def_type_year(year) == 28 else LEAP_MONTHS
    calendar = create_calen(firstdayyear, year_type, lang)
    distrib_weeks = distribute_weeks(calendar, startweekday)
    weeks = goodlike_months(distrib_weeks)
    month_week_count = 1
    if month_num == 0:
        previous_weeks_count = 0
    else:
        previous_weeks_count = sum_list([len(month_weeks) for month_weeks in weeks[:month_num]])
    
    label = h_md(1, f"{abs_val(month_num-12)} {MONTHS_NAME[lang][month_num]} {str(year)[2:]}")
    #output += label + "\n\n"
    output += label + "\n"
    for part in STRUCTURE_NOTE[lang]:
        #output += "\n" + h_md(3, part) + "\n\n"
        output += h_md(3, part) + "\n"
        if part == STRUCTURE_NOTE[lang][1]:
            for week in weeks[month_num]:
                global_week_count = month_week_count + previous_weeks_count
                #output += "\n" + h_md(4, f"{week_count} {WORD_WEEK[lang]} {week[0][0]+1}-{week[-1][0]+1}") + "\n\n"
                output += h_md(4, f"{month_week_count}/{global_week_count} {WORD_WEEK[lang]} {week[0][0]+1}-{week[-1][0]+1}") + "\n"
                for day in week:
                    #output += h_md(5, f"{day[1]} {day[0]+1}") + "\n\n"
                    output += h_md(5, f"{day[1]} {day[0]+1}") + "\n"
                month_week_count+= 1
    return output


def communication(): #get month, year, start of the week, 1st january day of week
    lang = 0
    year = YEAR
    startweekday = STARTWEEKDAY[0]
    firstdayyear = FIRSTDAYYEAR[0]
    print("""Default settings:

    Changable:
    - Start week day: SUNDAY
    - Year: 2026
    - 1st january of the year: THURSDAY
    - Language: Ukrainian (Maksymovychivka) 
   
    Unchangable: (for now)
    - Structure of note: label, expectations, schedule, summing up
    - Format type: MarkDown
          
Do you want to change settings?""")
    answer_set = int(input("Type 1 for \"yes\" and 0 for \"no\": "))
    if answer_set == 1:
        print(f"""1/4 Choose language:
    1 - {LANGUAGE[0]}
    2 - {LANGUAGE[1]}
    3 - {LANGUAGE[2]}""")
        lang = int(input(" "))-1
        print(f"""2/4 Choose what day will be start of weeks
    1 - {WEEKDAYS[lang][0]} 
    2 - {WEEKDAYS[lang][1]}
    3 - {WEEKDAYS[lang][2]}
    4 - {WEEKDAYS[lang][3]}
    5 - {WEEKDAYS[lang][4]}
    6 - {WEEKDAYS[lang][5]}
    7 - {WEEKDAYS[lang][6]}""")
        startweekday = WEEKDAYS[lang][int(input(" "))-1]
        print("3/4 Choose year (ex. 2026)")
        year = int(input(" "))
        print(f"""4/4 Name what week day is the 1st of january of {year}
1 - {WEEKDAYS[lang][0]} 
2 - {WEEKDAYS[lang][1]}
3 - {WEEKDAYS[lang][2]}
4 - {WEEKDAYS[lang][3]}
5 - {WEEKDAYS[lang][4]}
6 - {WEEKDAYS[lang][5]}
7 - {WEEKDAYS[lang][6]}""")
        firstdayyear = WEEKDAYS[lang][int(input(" "))-1]
    print("Choose what month you want to print")
    print(f"""    1 — {MONTHS_NAME[lang][0]}
    2 — {MONTHS_NAME[lang][1]}
    3 — {MONTHS_NAME[lang][2]}
    4 — {MONTHS_NAME[lang][3]}
    5 — {MONTHS_NAME[lang][4]}
    6 — {MONTHS_NAME[lang][5]}
    7 — {MONTHS_NAME[lang][6]}
    8 — {MONTHS_NAME[lang][7]}
    9 — {MONTHS_NAME[lang][8]}
    10 — {MONTHS_NAME[lang][9]}
    11 — {MONTHS_NAME[lang][10]}
    12 — {MONTHS_NAME[lang][11]}""")
    month_num = int(input("Type here: "))-1
    print("\n\nThanks. Here is your month note:\n")
    output = create_output(month_num, lang, year, startweekday, firstdayyear)
    with open(f"{MONTHS_NAME[lang][month_num]}.md", "w+") as md:
        md.write(output)
    print(output)
    return 0  

# _____ end _____

def main():
    print("Hello! This mini-app helps you to build your month notes")
    while True:
        print("""Use commands:
    /create -- for creating new month note
    /close -- for closing the program""")
        answer = input(" ")
        if answer == "/create":
            communication()
        if answer == "/close":
            print("The program is closed")
            break
    return 0

year_type = COMMON_MONTHS if def_type_year(YEAR) == 28 else LEAP_MONTHS
calendar = create_calen(FIRSTDAYYEAR[LANG_IDX], year_type, LANG_IDX)
distrib_weeks = distribute_weeks(calendar, STARTWEEKDAY[LANG_IDX])

#print(distrib_weeks)

main()