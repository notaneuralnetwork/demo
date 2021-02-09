"""
Produces a KML file suitable for import into Google Earth showing current apartment listings in Montreal.

Listings are downloaded from a number of sources (currently Kijiji and Louer.ca), parsed, and saved in a standardized form into a CSV file.

The KML file is then generated from the CSV file by representing each apartment as a pin. This file can be imported into Google Earth, allowing apartment locations to be visualized with respect to major landmarks and amenities, such as Metro stations.

Known bugs:
- A small fraction of listings from Louer.ca do not have their prices parsed correctly.
"""

from bs4 import BeautifulSoup
import time,urllib.request
import pandas as pd

csv_file_path="./apartments.csv"

"""Downloads an object from the Internet. Set decode to 1 for HTML and other text-based content; set to 0 for binary data."""
def download(url,decode):
	user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
	request_delay=3
	#Requests object.
	print("Downloading "+url+"\n")
	request=urllib.request.Request(url,headers={"User-Agent":user_agent})
	online_object=urllib.request.urlopen(request)
	#Decodes object if text-based.
	if decode==0:
		content=online_object.read()
	elif decode==1:
		content=online_object.read().decode("utf8")
	online_object.close()
	#Delays to avoid crawler limitations.
	time.sleep(request_delay)
	#Returns downloaded content.
	return content

"""Scrapes apartment listings from Kijiji. Generally the number of listings pages will vary with price range and should be checked before running this function. Avoid including listings which are too stale."""
def scrape_kijiji(minimum_price,maximum_price):
	#Listing page URL parameters
	maximum_listings_pages=20
	default_listings_url="https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/page-!!!/c37l1700281?price="+str(minimum_price)+"__"+str(maximum_price)
	page_placeholder="!!!"
	#Downloads listings pages and extracts apartment URLs.
	apartment_urls=[]
	apartments=[]
	for i in range(1,maximum_listings_pages):
		#Downloads listings page.
		listings_url=default_listings_url.replace(page_placeholder,str(i))
		listings_page=download(listings_url,1)
		#Parses listings page to extract apartment URLs.
		apartment_urls_raw=listings_page.split("<div class=\"title\">")[1:-1]
		for i in range(0,len(apartment_urls_raw)):
			try:
				apartment_url="https://www.kijiji.ca"+apartment_urls_raw[i].split("<a href=\"")[1].split("\"")[0]
				#Downloads and parses each apartment page if URL not already encountered.
				if apartment_url not in apartment_urls:
					apartment_urls.append(apartment_url)
					#Downloads apartment page.
					apartment_page=download(apartment_url,1)
					#Parses apartment page to extract price and location data.
					latitude=apartment_page.split("og:latitude\" content=\"")[1].split("\"")[0]
					longitude=apartment_page.split("og:longitude\" content=\"")[1].split("\"")[0]
					price=apartment_page.split("<div class=\"priceWrapper-1165431705\"><span content=\"")[1].split("\"")[0]
					#Appends apartment record to the table.
					apartment_record=[latitude,longitude,price,apartment_url]
					apartments.append(apartment_record)
			except:
				continue
	#Writes apartment data to the CSV file.
	apartments_dataframe=pd.DataFrame(apartments)
	apartments_dataframe.to_csv(csv_file_path,mode="a",header=False,index=False)

"""Scrapes apartment listings from Louer.ca. Generally the number of listings pages will vary with price range and should be checked before running this function. Avoid including listings which are too stale."""
def scrape_louer(minimum_price,maximum_price):
	#Listing page URL parameters
	maximum_listings_pages=20
	default_listings_url="https://www.louer.ca/appartement+condo-a-louer-montreal-villes/!!!"
	page_placeholder="!!!"
	#Downloads listings pages and extracts apartment URLs.
	apartment_urls=[]
	apartments=[]
	for i in range(1,maximum_listings_pages):
		#Downloads listings page.
		listings_url=default_listings_url.replace(page_placeholder,str(i))
		listings_page=download(listings_url,1)
		#Parses listings page to extract apartment URLs.
		apartment_urls_raw=listings_page.split("class=\"details-button btn btn-warning btn-block view-more-btn\" href=\"")[1:-1]
		prices_raw=listings_page.split("<li class=\"price\">Loyer Mensuel  :                                        <span>")[1:-1]
		for i in range(0,len(apartment_urls_raw)):
			try:
				apartment_url=apartment_urls_raw[i].split("\"")[0]
				price_string=prices_raw[i].split("<")[0].split(" ")
				#Determines whether price range of apartment overlaps with user's desired price range.
				if len(price_string)==2:
					price=int(price_string[0])
					if ((price<minimum_price) or (price>maximum_price)):
						continue
				else:
					minimum_price_on_ad=int(price_string[0])
					maximum_price_on_ad=int(price_string[3])
					price=int((maximum_price_on_ad+minimum_price_on_ad)/2)
					if ((minimum_price_on_ad>maximum_price) or (maximum_price_on_ad<minimum_price)):
						continue
				#Downloads and parses each apartment page if URL not already encountered.
				if apartment_url not in apartment_urls:
					apartment_urls.append(apartment_url)
					#Downloads apartment page.
					apartment_page=download(apartment_url,1)
					#Parses apartment page to extract location data.
					address_raw=apartment_page.split("<h5 class=\"panel-title\">")[1].split("</h5>")[0].strip()
					address=" ".join(BeautifulSoup(address_raw,"html.parser").get_text().replace("\n"," ").split())
					address=address[:address.index("#LID")].strip()
					#Appends apartment record to the table.
					apartment_record=[address,"None",str(price),apartment_url]
					apartments.append(apartment_record)
			except:
				continue
	#Writes apartment data to the CSV file.
	apartments_dataframe=pd.DataFrame(apartments)
	apartments_dataframe.to_csv(csv_file_path,mode="a",header=False,index=False)

#Generates the KML file.
def generate_kml_file():
	#Loads the CSV file.
	apartments=pd.read_csv(csv_file_path)
	#Creates the KML file.
	kml_file=open("./apartments.kml","w",encoding="utf8")
	kml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n<Document>\n")
	#Writes apartment data to the KML file.
	for index,row in apartments.iterrows():
		price=int(row[2])
		url=row[3]
		if row[1]=="None":
			address=row[0]
			kml_file.write("<Placemark><name>"+str(price)+"</name><description>"+url+"</description><address>"+address+"</address></Placemark>\n")
		else:
			latitude=row[0]
			longitude=row[1]
			kml_file.write("<Placemark><name>"+str(price)+"</name><description>"+url+"</description><Point><coordinates>"+str(longitude)+","+str(latitude)+",0</coordinates></Point></Placemark>\n")
	#Closes the KML file.
	kml_file.write("</Document>\n</kml>")
	kml_file.close()

"""Validates all input. Returns False if an error is encountered, otherwise returns True."""
def validate_input(minimum_price,maximum_price):
	#Ensures minimum_price is an integer.
	if type(minimum_price)!=int:
		print("Error. minimum_price must be an integer.")
		return False
	#Ensures maximum_price is an integer.
	if type(maximum_price)!=int:
		print("Error. maximum_price must be an integer.")
		return False
	#Ensures minimum_price and maximum_price are greater than 0.
	if minimum_price<0:
		print("Error. minimum_price must be greater than 0.")
		return False
	elif maximum_price<0:
		print("Error. maximum_price must be greater than 0.")
		return False
	#Ensures minimum_price is lower than maximum_price.
	if minimum_price>=maximum_price:
		print("Error. minimum_price must be lower than maximum_price.")
		return False
	#Returns True if all input is valid.
	return True

"""Main. Define arguments here, then run in the command line: python ./apartment_mapper.py"""
def main():
	minimum_price=700
	maximum_price=1100
	#Validates input.
	if not validate_input(minimum_price,maximum_price):
		return -1
	#Downloads apartment listings from various online classifieds websites.
	scrape_kijiji(minimum_price,maximum_price)
	scrape_louer(minimum_price,maximum_price)
	#Generates the KML file.
	generate_kml_file()

if __name__=="__main__":
	main()
