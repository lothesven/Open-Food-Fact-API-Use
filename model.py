# Class definition to :
# 
# - make some requests on OFF and store raw datas
# Set here criteria (Categories / nutrition_grades)
#
# - clean a JSON
# Define here what informations are usefull
# Isolate and/or modify then store them with any needed methods

######

# Procedure that check local database for existence of tables "Foods" and "Categories"
# If no such tables exists, creates them

# Procedure that check if Local database contains datas
# If not, gets data from OFF and clean them

######

# Class definition to insert cleaned datas in local database

######

# Class with many methods to: 
# 
# - get the list of categories from database
# - get the list of products in a given category from database
# - find substitute of any given product in Local Database
# (Define here sorting principles and priorities)
# - get the list of database requests (history)
# - get the list of products / subtitute pairs

# -*- coding: utf-8 -*

from __future__ import print_function

import json
from datetime import date, datetime, timedelta

import requests
import mysql.connector
from mysql.connector import errorcode

import config as cf

class Category():

# Instances are objects that contains a list of individual products
# found in specified category on Open Food Facts

    def __init__(self, name):
        self.name = name
        self.products = self.get_products()
        self.subcategories = self.get_subcategories()

    def get_products(self):
        '''Use module requests to get products on Open Food Facts'''
        products = list()
        for grade in cf.grades:
            payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': self.name,
                'tagtype_1': 'nutrition_grade_fr',
                'tag_contains_1': 'contains',
                'tag_1': grade,
                'fields': cf.criterias,
                'sort_by': 'unique_scans_n',
                'json': 'true',
                'page_size': '5'
            }
            print(payload)
            request = requests.get(cf.url, params=payload)
            for product in request.json().get('products'):
                products.append(product)

        return products
    
    def get_subcategories(self):
        '''Browse every product from get_products to find subcategories'''
        subcategories = list()
        for product in self.products:
            temp_list = product.get('categories_tags') # get list of subcategories for each product
            if type(temp_list) is list:
                for subcategory in temp_list:
                    if subcategory not in subcategories: # keep only those not in subcategories yet
                        subcategories.append(subcategory)

        return subcategories

class Product():

# Instances are individual products
# Informations must be of type dict and contains each criteria:
# code,product_name_fr,brands,ingredients_text_fr,nutrition_grade_fr,unique_scans_n,stores,url

    def __init__(self, informations):
        self.code = informations.get('code')
        self.name = informations.get('product_name_fr')
        self.brand = informations.get('brands')
        self.description = informations.get('ingredients_text_fr')
        self.categories = informations.get('categories_tags')
        self.healthyness = informations.get('nutrition_grade_fr')
        self.popularity = informations.get('unique_scans_n')
        self.stores = informations.get('stores')
        self.url = informations.get('url')

    def __str__(self):
        return "name = " + str(self.code) + "\n" + "brand = " + str(self.name) + "\n" + "code = " + str(self.brand) + "\n" + "description = " + str(self.description) +  "\n" + "categories = " + str(self.categories) +  "\n" + "healthyness = " + str(self.healthyness) + "\n" + "popularity = " + str(self.popularity) + "\n" + "stores = " + str(self.stores) + "\n" + "url = " + str(self.url)

class DatabaseInterraction():
    # Handles interractions with database
    # Every function call leaves an history
    # Whennever connector is closed, write history in database just before

    def __init__(self, action):
        # action is a string refering to one specific operation
        self.action = action

        self.informations = None
        self.result = None
        self.connector = None
        self.cursor = None

        self.history = {}

        self.verify("self.connector = mysql.connector.connect(cf.credentials)")
        self.verify("self.cursor = self.connector.cursor()")
        self.verify("""self.cursor.execute("USE {}".format(cf.DB_NAME))""")

        exec(self.action)

        self.leave_history() # Do not forget to create Table History

    def create_table(self, name, informations):
        # Create a table, provided name and informations
        self.informations = informations

        self.action = "Attempt to create table {} with following instructions {}".format(name, self.informations)

        print("Creating table {}: ".format(name), end='')
        self.result = self.verify("self.cursor.execute(self.informations)")
        print(self.result)
        # Verify with creation instructions in self.informations

        self.history[self.action] = self.result
        self.action = None
        self.result = None

    def insert_datas(self, informations):
        pass

    def fetch_datas(self, informations):
        pass

    def create_user(self, informations):
        # insert data in users table
        pass

    def verify(self, instructions):
        # Verifies if instructions are valid
        # Executes the intructions if so
        # Returns a string if an error occured
        try:
            exec(instructions)
            return "OK"
        except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    return "Something is wrong with user name or password. Please check 'config.py'."
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    return "Database {} does not exists. Please follow instructions in 'Readme.md'".format(cf.DB_NAME)
                elif err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    return "Table already exists."
                else:
                    return err.msg
        else:
            return "Unknown error"
    
    def leave_history(self):

        print("Commiting ...")
        self.verify("self.connector.commit()")

        # leave history by using self.insert_data() and self.history

        self.cursor.close()
        self.connector.close()

def get_off_datas():
    for i in cf.categories:
        print(i)
        i = Category(i)
        for j in i.products:
            j = Product(j)
            print(j)
        print(i.subcategories)
        print(len(i.subcategories))

def create_tables():
    for i in cf.TABLES:
        print(i)
        action = """self.create_table("{}, {}".format(i, cf.TABLES.get(i))"""
        i = DatabaseInterraction(action)

def main():
    get_off_datas()
    create_tables()

main()