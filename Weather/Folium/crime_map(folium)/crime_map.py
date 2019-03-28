#importing libraries 
import folium
import csv 

#making some empty list for store data
city=[]
data_lon=[]
data_lat=[]
crime_name=[]
y=0
with open("crime_map.csv") as crime:
    read=csv.reader(crime,delimiter=",")
    for i in read:
        if(y%2==0):
            city.append(i[0])
            crime_name.append(i[1])
            data_lon.append(i[8])
            data_lat.append(i[9])
        y+=1

#for skiping columns name
city=city[1:]
data_lon=data_lon[1:]
data_lat=data_lat[1:]

#lat-long of focus area and zoom start
map = folium.Map([20.5937,78.9629], zoom_start=5)

# Mapbox makes some nice map tiles,
# but the free versions only have limited levels of zoom available.
tile = folium.TileLayer('Mapbox Bright').add_to(map)

# Control Room is another set of MapBox tiles.
# Again there are only limited levels of zoom available for the free version, but they do look cool.
tile = folium.TileLayer('Mapbox Control Room').add_to(map)

# Stamen also produce some cool map tiles which typically work at all zoom levels.
tile = folium.TileLayer('Stamen Terrain').add_to(map)

# The Stamen toner map tiles produce a black and white map that both looks striking and
# would be more suitable for printing than some of the other Folium map tiles.
tile = folium.TileLayer('Stamen Toner').add_to(map)

# Stamen Watercolor
tile = folium.TileLayer('stamenwatercolor').add_to(map)

# The CartoDB folium map tiles are cool looking tiles and are in the lighter “positron”
tile = folium.TileLayer('cartodbpositron').add_to(map)

#The CartoDB Dark Matter tiles are essentially a darker version of the above positron tiles.
tile = folium.TileLayer('cartodbdark_matter').add_to(map)

#importing cluster marker for better look
from folium.plugins import MarkerCluster
#adding marker to map
marker_cluster = MarkerCluster().add_to(map)

#adding marker and popup of city and crime-name
for i in range(0,len(city)):
    folium.Marker([float(data_lon[i])  ,float(data_lat[i])],popup="city name ="+city[i]+"\n crime_of_city = "+crime_name[i]).add_to(marker_cluster)

#we can change tiles with help of LayerConrol
folium.LayerControl().add_to(map)

#saving map to a html file
map.save('crime_data.html')

#creating a html iframe
from IPython.display import HTML
HTML('<iframe src=plot_data.html width=300 height=200></iframe>')

