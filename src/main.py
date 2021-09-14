import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

csv = pd.read_csv(r"C:\Users\Korisnik\PycharmProjects\ThreeMovingAverages\src\SPY.xls")
df = csv.set_index(pd.DatetimeIndex(csv['Date'].values))

#plt.figure(figsize=(12.2, 4.5))
#plt.title('Open Price', fontsize=18)
#plt.plot(df['Open'])
#plt.xlabel('Date', fontsize = 18)
#plt.ylabel('Open price', fontsize = 18)
#plt.show()

#Calculate the short/fast exponential moving average
ShortEMA = df.Open.ewm(span=5, adjust = False).mean()

#Calculate the middle/medium exponential moving average
MiddleEMA = df.Close.ewm(span=21, adjust = False).mean()

#Calculate the long/slow exponential moving average
LongEMA = df.Open.ewm(span=63, adjust = False).mean()

#Visualise open price and exponential moving averages
#plt.figure(figsize=(20, 8))
#plt.title('Open price', fontsize = 18)
#plt.plot(df['Open'], label = 'Close price', color = 'blue')
#plt.plot(ShortEMA,  label = 'Short/Fast EMA', color = 'pink')
#plt.plot(MiddleEMA, label = 'Middle/Medium EMA', color = 'green')
#plt.xlabel('Date', fontsize = 18)
#plt.ylabel('Open price', fontsize = 18)
#plt.show()

df['Short'] = ShortEMA
df['Middle'] = MiddleEMA
df['Long'] = LongEMA
#1/open
df['revOpen'] = 1 / df['Open']
#sum of 1/open
k = df['revOpen'].sum()
#normalized
df['weights'] = k * df['revOpen']


def decide(data):
    buy_list = []
    sell_list = []
    flag_long = False
    flag_short = False

    for i in range (0, len(data)):
        if (data['Middle'][i] < data['Long'][i]
            and data['Short'][i] < data['Middle'][i]
            and flag_long == False):
            buy_list.append(data['Open'][i])
            sell_list.append(np.nan)
            flag_short = True
        elif (flag_short == True
              and data['Short'][i] > data['Middle'][i]):
            sell_list.append(data['Open'][i])
          #  data['weights'][i] = - data['weights'][i]
            buy_list.append(np.nan)
            flag_short = False
        elif (data['Middle'][i] > data['Long'][i]
              and data['Short'][i] > data['Middle'][i]
              and flag_long == False):
            sell_list.append(np.nan)
            buy_list.append(data['Open'][i])
            flag_long = True
        elif (flag_long == True
              and data['Short'][i] < data['Middle'][i]):
            sell_list.append(data['Open'][i])
            #data['weights'][i] = - data['weights'][i]
            buy_list.append(np.nan)
            flag_long = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)

    return (buy_list, sell_list)



df['Buy'] = decide(df)[0]
df['Sell'] = decide(df)[1]


plt.figure(figsize=(20, 8))
plt.title('Buy and sell plot', fontsize = 10)
plt.plot(df['Open'], label = 'Close price', color = 'blue', alpha = 1, linewidth = 1)
plt.plot(ShortEMA,  label = 'Short/Fast EMA', color = 'red', alpha = 1, linewidth = 1)
plt.plot(MiddleEMA, label = 'Middle/Medium EMA', color = 'black', alpha = 1, linewidth = 1)
plt.plot(LongEMA,  label = 'Long/Slow EMA', color = 'green', alpha = 1, linewidth = 1)
plt.scatter(df.index, df['Buy'], color = 'green', marker = "^", alpha=1)
plt.scatter(df.index, df['Sell'], color = 'red', marker = "v", alpha=1)
plt.xlabel('Date', fontsize = 10)
plt.ylabel('Open price', fontsize = 10)
plt.show()

print(df['weights'])