from bs4 import BeautifulSoup
import requests
import csv

# Hitting the URL to extract the source of a website
source_cd = requests.get("http://books.toscrape.com/").text
soup = BeautifulSoup(source_cd,'lxml')


with open('book_list.csv','w',newline = '') as f1:

    csv_writer = csv.writer(f1)
    csv_writer.writerow (['Book Title','Book Prize','Book Availability'])

    for article_ in soup.find_all('article',class_ = 'product_pod'):

        # Extracting the book title
        title_ = article_.find('h3')
        book_ = title_.find('a')['title']

        # Extracting the prize of the book
        prize_src = article_.find('div', class_='product_price')
        prize_ = prize_src.find('p', class_='price_color').text
        prize_ = prize_.replace(prize_[0],'')
      

        # Extracting stock details
        InStock = (prize_src.find('p', class_='instock availability').text).strip('\n" "')

        # Writing to CSV
        csv_writer.writerow([book_,prize_,InStock])
    print("For loop Completed")













