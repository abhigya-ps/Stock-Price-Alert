import os
import smtplib
from email.message import EmailMessage

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

EMAIL_ADDRESS = os.environ.get('EMAIL_ID')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

def mailing(text):
    msg = EmailMessage() 
    msg['Subject'] = 'Stock Fluctuation Alert'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'abhigya.sa@gmail.com'
    msg.set_content(text)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


api_key = os.environ.get('ALPHA_API_KEY')

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_daily(symbol='FB', outputsize = 'full')    # Replace daily with weekly, monthly, or intraday for different timeframes.
print(data.head())

open_value = data.iloc[0][0]
close_value = data.iloc[0][3]

change = 100 * ((close_value-open_value)/open_value)
pct = '{0:.2%}'.format(abs(change)/100)

if abs(change) > 4:
    message = 'Your stock\'s price has changed by more than 4%!'

    if change > 0:
        msg_detail = (message + ' Your stock has gone up by ' + pct + '.')
        print(msg_detail)

    elif change < 0:
        msg_detail = (message + ' Your stock has gone down by ' + pct + '.')
        print(msg_detail)
    
elif change == 0:
    msg_detail = ('No change in your stock price.')
    print(msg_detail)

mailing(msg_detail)

