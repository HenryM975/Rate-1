import matplotlib.pyplot as plt
from matplotlib.widgets import Button #test
import pylab
import time
import random
#from datetime import *
import requests as rqs
from bs4 import BeautifulSoup as bs
"""def fetchHTMLFromUrl(url):
    global fetchHTMLFromUrl
    sourse = rqs.get(url)
    soursetext = sourse.text
    soup = bs(soursetext, 'html.parser')
    return soup"""


def getCountreFromHTML(rqs, plt, bs, url):
    try:
        global soup
        sourse = rqs.get(url)
        soursetext = sourse.text
        soup = bs(soursetext, 'html.parser')
    except:
        print("error in getCountreFromHTML")


def CBR(num):
    try:
        global Dollar_USA_CBR_rate
        url = 'https://www.cbr.ru/currency_base/daily/'
        getCountreFromHTML(rqs, plt, bs, url)
        CBR_crude_table = soup.findAll('td')

        """#ratePageHTML = fetchHTMLFromUrl('...')
        countryName = getCountreFromHTML(ratePageHTML)
        currencyRate = getCountryRate(countryName, ratePageHTML)"""

        #Countryname1 = CBR_crude_table[53]
        #USA = CBR_crude_table[54]
        #numlist = []
        clear_CBR_rate_list = []
        for i in CBR_crude_table:
            j = str(i)
            j = j[4:-5]
            clear_CBR_rate_list.append(j)
        Countryname1 = clear_CBR_rate_list[53]
        Dollar_USA_CBR_rate = clear_CBR_rate_list[54]
        Dollar_USA_CBR_rate = float(Dollar_USA_CBR_rate.replace(',', '.'))
        print("$:")
        print(Dollar_USA_CBR_rate)
    except:
        print("error in CBR")


def Localbitcoins(num):
    try:
        global finalbitnum
        global firstbitseller
        url = 'https://localbitcoins.net/instant-bitcoins/?action=buy&country_code=RU&amount=&currency=RUB&place_country=RU&online_provider=SPECIFIC_BANK&find-offers=%D0%BE%D0%B8%D1%81%D0%BA'
        getCountreFromHTML(rqs, plt, bs, url)
        table = soup.findAll('td', {'class': "column-price"})
        part = str(table)
        partlist2 = part.replace('</td>, <td class="column-price">', ' ')
        partlist3 = part.replace('[<td class="column-price">', ' ')
        list = partlist3.split('</td>, <td class="column-price">')
        clearlist = []
        list = list[0:-1]
        for k in list:
            k = k[35:-34]
            k = k.replace(' ', '')
            k = k.replace(',', '')
            k = float(k)
            clearlist.append(k)
        finalbitnum = ((clearlist[0] + clearlist[1] + clearlist[4] + clearlist[5] + clearlist[6] + clearlist[7]) / 7)
        finalbitnum = finalbitnum / 10000  # 100000satoshi
        firstbitseller = clearlist[0] / 10000  ############################
        print("medium bit rate:")
        print(finalbitnum)
        print("bit rate of first seller")
        print(firstbitseller)
    except:
        print("error in Localbitcoins")

def Monero(num):
    try:
        global monero_last_rate
        url = 'https://www.calc.ru/kurs-XMR-RUB.html'
        getCountreFromHTML(rqs, plt, bs, url)
        monero_html_table = soup.findAll('td', {'height': "25"})
        monero_html_table_str = str(monero_html_table)
        monero_first_clearing_list = monero_html_table_str.split('</td>, <td align="center" height="25">')
        monero_second_clearing_list = []
        for part in monero_first_clearing_list:
            part = part.replace('<font color="green">↑</font> </td>, <td align="center" height="25">', '')
            part = part.replace('<font color="green">↑</font>', '')
            part = part.replace('</td>, <td align="center" bgcolor="#F5F5F5" height="25">\r\n ', '')
            part = part.replace(' ', '')
            part = part.replace('\r\n', '')
            part = part.replace('[<tdalign="center"height="25">', '')
            monero_second_clearing_list.append(part)
        monero_last_rate = float(monero_second_clearing_list[1])
        monero_last_rate = monero_last_rate / 100  # адаптация к графику
        print("monero: ")
        print(monero_last_rate)
    except:
        print("error in Monero")


def Append_Rates_in_final_lists(Dollar_USA_CBR_rate, num, random_num, finalbitnum, firstbitseller, monero_last_rate):
    try:
        Dollar_USA.append(Dollar_USA_CBR_rate)  # usa
        Dollar_USA_time.append(num)

        test_rate.append(random_num)
        test_rate_time.append(num)

        Medium_bitcoin_rate.append(finalbitnum)  # finalbitnum
        Medium_bitcoin_rate_time.append(num)

        First_bitcoin_seller_rate.append(firstbitseller)
        First_bitcoin_seller_rate_time.append(num)

        Monero_daily_rate.append(monero_last_rate)
        Monero_daily_rate_time.append(num)

    except:
        print("error in Append_Rates_in_final_lists")


def Schedule(Dollar_USA, Dollar_USA_time, test_rate, test_rate_time, Medium_bitcoin_rate, Medium_bitcoin_rate_time, First_bitcoin_seller_rate, First_bitcoin_seller_rate_time, Monero_daily_rate, Monero_daily_rate_time):#Dollar_USA_CBR_rate, num, finalbitnum, firstbitseller, monero_last_rate):
    try:

        plt.xlabel("time")  # ось абсцис
        plt.ylabel("Руб")  # ось ординат
        #plt.grid()
        plt.plot(Dollar_USA_time, Dollar_USA, "g:", color = 'b')
        plt.plot(test_rate_time, test_rate, color = 'green')
        plt.plot(Medium_bitcoin_rate_time, Medium_bitcoin_rate, color = 'r')
        plt.plot(First_bitcoin_seller_rate_time, First_bitcoin_seller_rate, "g--", color = 'r')
        plt.plot(Monero_daily_rate_time, Monero_daily_rate, color='orange')
        #####No handles with labels found to put in legend. #in legend
        Schedule_legend()
        """
        str_USA = str(Dollar_USA[-1])
        str_num = str(num)
        str_finalbitnum = str(Medium_bitcoin_rate[-1])
        str_firstbitseller = str(First_bitcoin_seller_rate[-1])
        str_monero_last_rate = str(Monero_daily_rate[-1])
        pylab.legend(loc='upper right')
        pylab.legend(bbox_to_anchor=(10, 10))####вынесение?
        pylab.legend(("$ " + str_USA + "Руб", "test " + str_num, "middleBit/10000 " + str_finalbitnum, "first on lb/10000 " + str_firstbitseller, "monero daly rate/100: " + str_monero_last_rate))
        """
        ########
        ##button_add = button(axes_button_add, 'Добавить')/кнопка выключения
        #fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.2)#shedule position
        ##axes_button_add = pylab.axes([0.7, 0.05, 0.25, 0.075])
        ##button_add = Button(axes_button_add, 'Добавить')

        ###BUTTTON
        #fig = plt.figure()
        #fig.patch.set_facecolor('xkcd:mint green')
        ###
        plt.draw()  # new
        plt.minorticks_on()
        plt.grid(which='major',
                  color = 'k',
                  linewidth = 1)
        plt.grid(which='minor',
                 color='k',
                 linestyle=':')
        plt.pause(1)
        time.sleep(1)
        plt.ioff()  # new
        #pylab.plot(xlist, ylist1, "b-")
        #pylab.plot(xlist, ylist2, "g--")
        pass
    except:
        print("Error in Schedule")


def Schedule_legend():
    str_USA = str(Dollar_USA[-1])
    str_num = str(num)
    str_finalbitnum = str(Medium_bitcoin_rate[-1])
    str_firstbitseller = str(First_bitcoin_seller_rate[-1])
    str_monero_last_rate = str(Monero_daily_rate[-1])
    #fig.legend(loc = 'upper right')
    #fig.legend(bbox_to_anchor = (2, 2))  ####вынесение?
    fig.legend(("$ " + str_USA + "Руб", "test " + str_num, "middleBit/10000 " + str_finalbitnum,
                  "first on lb/10000 " + str_firstbitseller, "monero daly rate/100: " + str_monero_last_rate), loc = 'lower left', borderaxespad = 0, mode='expand', ncol=3)
    pass


def Schedule_style():
    global fig
    fig = plt.figure(figsize=(8.5 , 6.5))
    fig.patch.set_facecolor('xkcd:beige')
    ax = fig.add_subplot(1, 1, 1)  # nrows, ncols, index
    ax.set_facecolor('xkcd:wheat')
    #fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.2)  # shedule position
    #ax.set_facecolor((1.0, 0.47, 0.42))
    #axes_button_add = pylab.axes([0.7, 0.05, 0.25, 0.075])
    #button_add = Button(axes_button_add, 'Добавить')
    pass


def SaveTextData( USA, num, random_num, finalbitnum, firstbitseller, monero_last_rate):#вывод данных для предварительного заполнения таблицы
    try:
        f = open('mtpl2data.txt', 'a')
        txtUSA = str(USA)
        txtnum = str(num)
        txtfinalbitnum = str(finalbitnum)
        txtfirstbitseller = str(firstbitseller)
        txtrandom_num = str(random_num)
        txtmonero_last_rate = str(monero_last_rate)
        f.write("$: " + "|" + txtUSA  + "|" + " finalbitnum: " + "|" + txtfinalbitnum + "|" + " firstbitseller: " + "|" + txtfirstbitseller + "|" + "monero_last_rate: " + "|" + txtmonero_last_rate + "|" + " num: " + "|" + txtnum + "|" + "random_num: " + "|" +txtrandom_num  +  "\n" )
        pass
    except:
        print("error in SaveTextData")


def Append_Saved_Text_Data():   # + last time
    try:
        global time_float
        text_file = open('mtpl2data.txt', 'r')
        #crude_text_list = f.split('.')
        for line in text_file:
            #if line in text_file:
                #sys.exit
                print(line)
                print("*")
                line_list = line.split("|")
                #####################
                time_float = float(line_list[9])
                #$
                Dollar_USA_float = float(line_list[1])
                Dollar_USA.append(Dollar_USA_float)
                Dollar_USA_time.append(time_float)
                #test
                random_num_float = float(line_list[-1])
                test_rate.append(random_num_float)
                test_rate_time.append(time_float)
                #mediumBitRate
                Medium_bitcoin_rate_float = float(line_list[3])
                Medium_bitcoin_rate.append(Medium_bitcoin_rate_float)
                Medium_bitcoin_rate_time.append(time_float)
                #FirsBitSeller
                First_bitcoin_seller_rate_float = float(line_list[5])
                First_bitcoin_seller_rate.append(First_bitcoin_seller_rate_float)
                First_bitcoin_seller_rate_time.append(time_float)
                #Monero
                Monero_daily_rate_float = float(line_list[7])
                Monero_daily_rate.append(Monero_daily_rate_float)
                Monero_daily_rate_time.append(time_float)
            #else:
                #print("list is not full")
        pass
    except:
        print("error in Append_Saved_Text_Data")


Schedule_style()

Dollar_USA = []
Dollar_USA_time = []
test_rate = []
test_rate_time = []
Medium_bitcoin_rate = []
Medium_bitcoin_rate_time = []
First_bitcoin_seller_rate = []
First_bitcoin_seller_rate_time = []
Monero_daily_rate = []
Monero_daily_rate_time = []

Append_Saved_Text_Data()#don't work

num = time_float
timelist =[]
StopNum = 0
while True:
    print("START__________________________________________________________________________________________________________")
    starttime = time.time()
    random_num = random.uniform(10, 20)
    num += 1
    Schedule(Dollar_USA, Dollar_USA_time, test_rate, test_rate_time, Medium_bitcoin_rate, Medium_bitcoin_rate_time, First_bitcoin_seller_rate, First_bitcoin_seller_rate_time, Monero_daily_rate, Monero_daily_rate_time)
    CBR(num)
    Localbitcoins(num)
    Monero(num)
    #num += 1
    #num = dt.combine(time)
    print(num)
    SaveTextData(Dollar_USA_CBR_rate, num, random_num, finalbitnum, firstbitseller, monero_last_rate)
    Append_Rates_in_final_lists(Dollar_USA_CBR_rate, num, random_num, finalbitnum, firstbitseller, monero_last_rate)
    #Schedule(Dollar_USA, Dollar_USA_time, test_rate, test_rate_time, Medium_bitcoin_rate, Medium_bitcoin_rate_time, First_bitcoin_seller_rate, First_bitcoin_seller_rate_time, Monero_daily_rate, Monero_daily_rate_time)
    print(Dollar_USA_time)
    print(Dollar_USA)
    print(test_rate_time)
    print(test_rate)
    print(Medium_bitcoin_rate_time)
    print(Medium_bitcoin_rate)
    print(First_bitcoin_seller_rate_time)
    print(First_bitcoin_seller_rate)
    print(Monero_daily_rate_time)
    print(Monero_daily_rate)

    print("time: ")
    stime = (time.time() - starttime)
    print("--- %s seconds ---" % stime )
    if StopNum == 1:
        False

#plt.ioff()#new
#plt.show()