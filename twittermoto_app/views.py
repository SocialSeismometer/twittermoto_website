from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io, base64

from django.conf import settings
from twittermoto import plotter


def makeplot():
    time, tweet_freq, C_t, DAs, df = plotter.get_data(settings.TWITTERMOTO_DB)

    fig, axes = plt.subplots(2, 1, sharex=True)
    plotter.plot_detection_region(axes[0], DAs[0])
    plotter.plot_tweetcount_vs_time(axes[0], time, tweet_freq)
    plotter.plot_USGS(axes[0], df)

    plotter.plot_detection_vs_time(axes[1], time, C_t)
    plotter.plot_USGS(axes[1], df)

    axes[1].set_ylim(0, 2)
    axes[1].set_xlim(min(time), max(time))
    axes[1].legend()
    fig.autofmt_xdate()
    myFmt = mdates.DateFormatter('%d-%b %H:%M')
    axes[1].xaxis.set_major_formatter(myFmt)

    return fig



class text(object):
    title = 'Twittermoto'
    maintext = 'A Twitter-based earthquake detector'
    subtext = ''#'here is some subtext'
    pitch = '''Twittermoto is a disruptive, cloud-based, agile start-up aiming to
    delivering real-time earthquake detection based on social media trends. This is
    achieved through the use of deep convolutional neural networks, and block chain technology.
    Twittermoto utilizes the synergistic energy of big data and machine learning to deliver real-world solutions and other buzzwords.

    '''




def homepage(request):
    fig = makeplot()
    graphic = fig2buffer(fig)


    return render(request=request,
    template_name='main/index.html',
    context={'text': text, 'graphics':graphic})



def fig2buffer(fig):
    # save to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=200)
    plt.close(fig)

    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    buffer.close()
    return graphic
