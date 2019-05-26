from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import io, base64

from django.conf import settings
from twittermoto import plotter, database


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


class text(object):
    title = 'Twittermoto'
    maintext = 'A Twitter-based earthquake detector'
    subtext = ''#'here is some subtext'
    pitch = '''Twittermoto is a disruptive, cloud-based, agile start-up aiming to
     delivering real-time earthquake detection based on social media trends. This is
     achieved through the use of deep convoluted neural networks, and block chain technology.
     Twittermoto utilizes the synergistic energy of big data and machine learning to deliver real-world solutions and other buzzwords.

    '''




def homepage(request):

    fig = plotter.plot_detector_vs_time(settings.TWITTERMOTO_DB, dt=60)
    graphic = fig2buffer(fig)


    return render(request=request,
    template_name='main/index.html',
    context={'text': text, 'graphics':graphic})
