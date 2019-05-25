from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import io, base64

from django.conf import settings
from twittermoto import database
from datetime import datetime
from dateutil import parser
import requests
import pandas as pd



class text(object):
    title = 'Twittermoto'
    maintext = 'A Twitter-based earthquake detector'
    subtext = ''#'here is some subtext'
    pitch = '''Twittermoto is a disruptive, cloud-based, agile start-up aiming to
     delivering real-time earthquake detection based on social media trends. This is
     achieved through the use of deep convoluted neural networks, and block chain technology.
     Twittermoto utilizes the synergistic energy of big data and machine learning to deliver real-world solutions and other buzzwords.

    '''

def plot_tweetcount_vs_time(db, dt=600):
    the_query = 'SELECT STRFTIME(\'%s\', created_at)/{} as minute, COUNT(*) \
    FROM tweets GROUP BY minute'.format(dt)


    X, Y = [], []
    print(db.query(the_query))
    for i, row in enumerate(db.query(the_query)):
        X.append(datetime.utcfromtimestamp(row[0]*dt))
        Y.append(row[1])
    #
    fig = plt.figure()

    plt.plot(X, Y, 'k', lw=1.5)
    # plot historical seismic data
    url='https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.csv'
    response = requests.get(url)
    #
    data = response.content.decode()
    df = pd.read_csv(pd.compat.StringIO(data))
    for i, row in df.iterrows():
        time = parser.parse(row.time)
        if row.mag>5:
            plt.axvline(time, lw=1, ls='--', c='r')
        elif row.mag>4:
            plt.axvline(time, lw=0.5, ls='--', c='0.3')
    #
    # prettify date on x-axis
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%d-%b %H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)

    plt.ylabel('Earthquake tweet rate [tweets/10 min]')
    plt.xlim(min(X), max(X))
    plt.ylim(0, max(Y))

    # save to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)

    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    buffer.close()
    return graphic


def homepage(request):
    db = database.SQLite(settings.TWITTERMOTO_DB)
    graphic = plot_tweetcount_vs_time(db)
    db.close()

    return render(request=request,
    template_name='main/index.html',
    context={'text': text, 'graphics':graphic})
