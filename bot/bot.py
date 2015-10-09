# -*- coding: utf-8 -*-

from weppy import App
import urllib
import urllib2
from forecasts import Forecasts

app = App(__name__)


@app.expose("/")
def hello():
    forecasts = get_forecasts()
    return "Stamattina ci sarà ".decode('utf-8') + unicode(forecasts.today.morning.first_sub_period)


def get_forecasts():
    values = {
        'lat': 44.49,
        'lon': 11.34,
        'lang': 'it'
    }
    url = urllib.urlencode(values)
    response = urllib2.urlopen("http://webapp.arpa.emr.it/api/forecasts?" + url).read()
    forecasts = Forecasts(response)

    return forecasts


if __name__ == "__main__":
    app.run()
