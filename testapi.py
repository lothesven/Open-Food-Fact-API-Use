# -*- coding: utf-8 -*

import requests
import json

url = "https://fr.openfoodfacts.org/cgi/search.pl?"

categories = [
    "Boissons-gazeuses", 
    "Biscuits-au-chocolat", 
    "Jus-de-fruit-pur-jus", 
    "Yaourts", 
    "Fromages", 
    "Chips", 
    "Pâtes-à-tartiner",
    "Céréales-pour-petit-déjeuner",
    "Pains", 
    "Soupes"
]

criterias = "categories,code,product_name_fr,brands,ingredients_text_fr,nutrition_grade_fr,unique_scans_n,stores,url"

class Category():

# Instances are objects that contains a list of individual products
# found in specified category on Open Food Facts

    def __init__(self, name):
        self.name = name
        self.products = self.get_products()

    def get_products(self):
        '''Use module requests to get products on Open Food Facts'''
        products = list()
        grades = ['A', 'B', 'C', 'D', 'E']
        for grade in grades:
            payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': self.name,
                'tagtype_1': 'nutrition_grade_fr',
                'tag_contains_1': 'contains',
                'tag_1': grade,
                'fields': criterias,
                'sort_by': 'unique_scans_n',
                'json': 'true',
                'page_size': '20'
            }
            print(payload)
            request = requests.get(url, params=payload)
            for product in request.json().get('products'):
                products.append(product)

        return products

class Product():

# Instances are individual products
# Informations must be of type dict and contains each criteria:
# code,product_name_fr,brands,ingredients_text_fr,nutrition_grade_fr,unique_scans_n,stores,url

    def __init__(self, informations):
        self.code = informations.get('code')
        self.name = informations.get('product_name_fr')
        self.brand = informations.get('brands')
        self.description = informations.get('ingredient_text_fr')
        self.categories = informations.get('categories')
        self.healthyness = informations.get('nutrition_grade_fr')
        self.popularity = informations.get('unique_scans_n')
        self.stores = informations.get('stores')
        self.url = informations.get('url')

    def __str__(self):
        return "name = " + str(self.code) + "\n" + "brand = " + str(self.name) + "\n" + "code = " + str(self.brand) + "\n" + "description = " + str(self.description) +  "\n" + "categories = " + str(self.categories) +  "\n" + "healthyness = " + str(self.healthyness) + "\n" + "popularity = " + str(self.popularity) + "\n" + "stores = " + str(self.stores) + "\n" + "url = " + str(self.url)

for i in categories:
    print(i)
    i = Category(i)
    for j in i.products:
        j = Product(j)
        print(j)