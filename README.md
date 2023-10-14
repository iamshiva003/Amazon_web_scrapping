
# Amazon Web Scrapping

Scrapping the Amazon website with country code and asin values and getting the product details.




## Output Json format
```json
{
    "product title": "Short Story: cello and piano.",
    "product image_url": "https://m.media-amazon.com/images/I/41fD+K43LcL._SY445_SX342_.jpg",
    "product price": "2394€",
    "product details": {
      "Éditeur": "Schott (1 janvier 2000)",
      "Langue": "Français",
      "Partition": "10 pages",
      "ISBN-10": "000101742X",
      "ISBN-13": "978-0001017429",
      "Poids de l'article": "80 g"
    }
```
## Run project

* Install all the modules
* Save the .csv file in the same directory as the main.py file
* Run the project


```bash
  python main.py
```


## Features

- Scrapes unlimited pages
- Json file
- Database (mysql)
- Cross platform


## Prerequisite

Install the required modules using

```python
  pip install -r requirements.txt
```
    
## Explanation

* First the .csv file is read using the pandas module and getting the country and asin values as (lists).
```python
df = pd.read_csv("Amazon Scraping - Sheet1.csv")
```

* The request is made with the help of requests module and get the response as html_data.
```python
html_data = requests.get(URL, headers=headers).text
```

* The response (html_data) is parsed with the help of BeautifulSoup4 module.
```python
soup = BeautifulSoup(html_data, 'html.parser')
```

* Getting all the product details while iterating the countries and asin values .

* Saving all the details in the products {Dictionary}

* Save the details in the Json file 
```python
    with open("products.json", "w", encoding="utf-8") as outfile:
        json.dump(products, outfile, ensure_ascii=False)
```

* Saving the details in the MYSQL database
```python
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
```

## Google Colab link:
[Link to project](https://colab.research.google.com/drive/1stn-P91WmqaR7IZCPfCDqbCKZLQvLaHN?usp=sharing)


# Hi, I'm Shivakumar Patil! 👋


## Authors

- [@Shivakumar Patil](https://github.com/iamshiva003)


## 🚀 About Me
I'm a python full stack developer...


## 🛠 Skills
Python, HTML, CSS, Javascript, C...


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://iamshiva003.github.io/personal/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/iamshiva003/)


