from bs4 import BeautifulSoup as bs
import requests

# Ask for name of movie 
movie = input("Enter your movie of choice:").replace(' ', '_')

# Create wikipedia link using movie name
link = "http://en.wikipedia.org/wiki/" + movie

# Fetch data from site with given link
r = requests.get(link)

# Specify lxml parser and retrieve content
soup = bs(r.content, features="lxml")
contents = soup.prettify()


try:
    # Find html elements under infobox vevent class
    infobox = soup.find(class_="infobox vevent")
    inforow = infobox.find_all("tr")
    infobox_exists = True

except:
    infobox_exists = False

if infobox_exists == True:
    # Create dictionary
    movie_info = {}

    def get_content_value(row_data):
        if row_data:
            return [li.get_text() for li in row.find_all("li")]
        else:
            return row_data.get_text()

    # Create dictionary with data from given indexes
    for index, row in enumerate(inforow):
        if index==0:
            movie_info['title'] = row.find("th").get_text()
        elif index==1:
            continue
        else:
            content_key = row.find("th").get_text()
            content_value = get_content_value(row.find("td"))
            movie_info[content_key] = content_value

    # Search dictionary for elements with key Starring 
    # to create list starring
    for key,value in movie_info.items():
        if key == 'Starring':
            starring = value

    # Isolate first element of list
    first = starring.pop(0)

    # Isolate last element of list
    last = starring.pop(-1)

    # Join middle elements of list with commas
    middle = ', '.join(starring)

    # Build final statement
    statement = movie.replace('_', " ") 
    statement += " stars " + first + ", "
    statement += middle + " and " + last + "."

else:
    statement = "The data for your input could not be found."

# Produce final statement
print(statement)

