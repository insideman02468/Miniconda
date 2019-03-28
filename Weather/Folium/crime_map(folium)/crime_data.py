#for reading csv file importing csv library
import csv 
#making some empty list for saving data
city=[]
crime_name=[]
year2010=[]
year2011=[]
year2012=[]
year2013=[]
year2014=[]
avg=[]
with open("crime_data.csv") as crime:
    read=csv.reader(crime,delimiter=",")
    for i in read:
        city.append(i[0])
        crime_name.append(i[1])
        year2010.append(i[2])
        year2011.append(i[3])
        year2012.append(i[4])
        year2013.append(i[5])
        year2014.append(i[6])
        avg.append(i[7])
#for skiping columns name
city=city[1:]
crime_name=crime_name[1:]
avg=avg[1:]
year2010=year2010[1:]
year2011=year2011[1:]
year2012=year2012[1:]
year2013=year2013[1:]
year2014=year2014[1:]
#importing requests library for request of lat-long of cities
import requests
import json
data_lon=[]
data_lat=[]
url1 = "http://api.openweathermap.org/data/2.5/weather?q="
url2 = ""
url3 = "&appid=e9185b28e9969fb7a300801eb026de9c"
for i in range(0,len(city)):
    
    if(city[i]=="Durg-Bhilainagar"):
        data_lon.insert(i,"81.3509")
        data_lat.insert(i,"21.1938")
    elif(city[i]=="India"):
        data_lon.insert(i,"78.9629")
        data_lat.insert(i,"20.5937")
    elif(city[i]=="Indore"):
        data_lon.insert(i,"75.8333")
        data_lat.insert(i,"22.7179")
    else:
        url2=city[i]
        print(url2)
        url = url1 + url2 + url3
        response = requests.get(url)
        data= response.content
        new_data=json.loads(data)
        data_lon.insert(i,new_data["coord"]["lon"])
        data_lat.insert(i,new_data["coord"]["lat"])
#creating a new csv file of crime data with lat-long of cities  
row=["city","crime_name","2010","2011","2012","2013","2014","avg","Latitude","Longitude"]
with open("Crime_map.csv", "wt") as write_file:
    writer=csv.writer(write_file)
    writer.writerow(row)
    for i in range(0,len(city)):
        done=[city[i],crime_name[i],year2010[i],year2011[i],year2012[i],year2013[i],year2014[i],avg[i],data_lat[i],data_lon[i]] 
        print (done)
        writer.writerow(done)



