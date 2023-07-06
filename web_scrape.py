from selenium import webdriver
from urllib.parse import urljoin
from lxml import html
from time import sleep
import pandas as pd
driver = webdriver.Chrome()
Name = []
Price = []
Reviews = []
Ratings = []
a_tags = []
for i in range(0,21):
    driver.get(f"https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1")
    sleep(1)
    base_url = driver.current_url
    tree = html.fromstring(driver.page_source)
    for element in tree.xpath('(.//div[@class="sg-col-inner"])[3]'):
        names = element.xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]')
        for name in names:
            Name.append(name.text)
        price = element.xpath('.//span[@class="a-price-whole"]')
        for prc in price:
            Price.append(prc.text)
        links = element.xpath('.//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
        for link in links:
            l = link.get('href')
            full_url = urljoin(base_url,l)
            a_tags.append(full_url)
        number_of_reviews = element.xpath('.//span[@class="a-size-base s-underline-text"]')
        for number_of_review in number_of_reviews:
            Reviews.append(number_of_review.text)
        ratings = element.xpath('.//span[@class="a-icon-alt"]')
        for rating in ratings:
            Ratings.append(rating.text)


#Creating dataFrame
# if the arrays are not having the same length
max_length = max(len(Name),len(Price),len(a_tags),len(Reviews),len(Ratings))
# Adding nan values if the length of the arrays are not equal
Name += [None] * (max_length - len(Name))
Price += [None] * (max_length - len(Price))
a_tags += [None] * (max_length - len(a_tags))
Reviews += [None] * (max_length - len(Reviews))
Ratings += [None] * (max_length - len(Ratings))

df = pd.DataFrame({'Product Name': Name, 'Price': Price,'Links': a_tags, 'Reviews':Reviews,'Ratings':Ratings})
df.to_csv('Amazon products.csv',index=False)




# Close the driver
driver.close()







