import geocoder
from darksky import forecast
key='fec4067ea316595f4f8617530e8da1be'

g = geocoder.ip('me')

lat= g.latlng[0]
longi= g.latlng[1]

city=forecast(key,lat , longi, units='si')
print(city.temperature)

def print_temp():
    return city.temperature