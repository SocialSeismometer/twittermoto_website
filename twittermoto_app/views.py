from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
import io, base64




def index(request):
    X = np.random.rand(100)
    fig = plt.figure()
    plt.plot(X)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)

    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    buffer.close()


    return render(request       = request,
                  template_name = 'main/index.html',
                  context       = {'title': 'Hey CGD! Here are some random numbers. Refresh for more :)',
                                    'graphics':graphic})
