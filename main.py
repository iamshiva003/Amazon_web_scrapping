import json

import mysql.connector
import pandas as pd
import requests
from bs4 import BeautifulSoup


def save_json_file(products):
    """The function takes products (dictionary) as input and creates a json file using it"""
    # Serializing json
    # Writing to sample.json using the parameter encoding as "utf-8" since all the html data contains many characters
    with open("products.json", "w", encoding="utf-8") as outfile:
        json.dump(products, outfile, ensure_ascii=False)


def save_database(products):
    """The function takes the products dictionary as input and puts all the data in mysql database"""
    # Connecting to the mysql database
    # to connect to the mysql database there should be mysql installed in your pc
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )

    # creating the cursor
    mycursor = mydb.cursor()

    # creating the database
    mycursor.execute("CREATE DATABASE IF NOT EXISTS products")
    mycursor.execute("USE products")

    # creating the table
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS product_items (product_title VARCHAR(255), product_image_url VARCHAR(255), "
        "product_price VARCHAR(255), product_details VARCHAR(255))")

    sql = ("INSERT INTO product_items (product_title, product_image_url, product_price, product_details) VALUES (%s, "
           "%s, %s, %s)")
    values = []

    # creating the product_details dictionary into a string since mysql can not process dictionary as inout
    i = 0
    for product in products:
        details = ''
        for a, b in product.pop("product details").items():
            a = str(a)
            b = str(b)
            details += " " + a + ": " + b + ','

        values.append(list(product.values()))
        values[i].append(details)
        i += 1

    # inputting the values into table
    mycursor.executemany(sql, values)

    # saving the changes using commit
    mydb.commit()

    # closing the connection
    mydb.close()


def get_data(countries, asins):
    """The function takes the countries and asins (lists) as input and gets the data using the request module and
    later scrapes the html data using the beautiful soup module and saves the data as json file and also database"""

    products = []
    # iterating through each links
    for country, asin in zip(countries, asins):
        # creating the URL
        URL = f"https://www.amazon.{country}/dp/{asin}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/116.0.0.0 Safari/537.36'}

        # skipping the URL whose asin value is less than 10 since the standard asins value contains 10 digit and the
        # remaining asin vales throws error 404
        # if len(asin) != 10 or asin == '000004458X':
        #     print(f"URL: {URL} not available")
        #     continue

        # getting the response from requests module
        html_data = requests.get(URL, headers=headers).text
        # creating the soup instance and parsing the html_data
        soup = BeautifulSoup(html_data, 'html.parser')

        # scrapping the html using beautifulsoup4
        product_title = soup.find(id="productTitle")

        # checking if the element is present in the webpage and if not present then skip the URL (error 404)
        # optional since the above code where it checks the length of the asin also does the same but this is the actual
        # way to skip the error pages (we can use any one method)
        try:
            if not product_title or asin == '000004458X':
                raise AttributeError(URL)
        except AttributeError:
            print(f"ERROR 404 URL: {URL} not available")
            continue

        product_image_url = soup.select("#imgTagWrapperId #landingImage")
        # product_price = soup.select_one("#tmmSwatches > ul > li > span > span + span > span > span > a")

        product_price = soup.select_one("span .format").text.strip()
        # removing all the letters and getting the price
        price = ''
        for letter in product_price:
            if letter.isdigit():
                price += letter
        price += product_price[-1]

        # getting the details of the product
        details_heading = soup.select("span.a-list-item span.a-text-bold")
        details_content = soup.select("span.a-list-item span.a-text-bold + span")

        # cleaning the data since it contains white spaces in-between
        details_heading_res = []
        details_content_res = []

        # checking if the first item in the index 0 is empty space and deleting the item
        if details_heading[0].text.isspace():
            del details_heading[0]

        for item in details_heading:
            str_item = ''
            index = len(item.text)
            for letter in str(item.text)[-1::-1]:
                if not letter.isalnum():
                    index -= 1
                else:
                    break
            str_item += str(item.text)[:index:]
            details_heading_res.append(str_item)

        for item in details_content:
            details_content_res.append(item.text)

        # creating the dictionary for product_details
        product_details = {}
        for key, value in zip(details_heading_res, details_content_res):
            product_details.update({key: value})

        # appending all the items details into the products (dictionary)
        products.append({"product title": product_title.text.strip(),
                         "product image_url": product_image_url[0]['src'],
                         "product price": price,
                         'product details': product_details})

    # saving the result into json and database (mysql)
    save_json_file(products)
    save_database(products)


def main():
    """The function reads the .csv file and gets the countries and asins columns"""

    # reading the .csv file using the pandas module
    df = pd.read_csv("Amazon Scraping - Sheet1.csv")

    # creating the lists of the columns
    countries = df['country'].tolist()
    asins = df['Asin'].tolist()

    get_data(countries, asins)


if __name__ == '__main__':
    main()
