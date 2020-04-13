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

    def clean_datas(self):
        sparse_products = []
        valid_products = []
        for product in self.products:

            problems = 0

            # verify if code is a non empty and non all white space string
            if type(product.get('code')) != str :
                problems += 1
            elif product.get('code').strip() == "" :
                problems += 1

            # code must be a string representing a number, therfore we try to convert it
            try:
                int(product.get('code'))
            except:
                problems +=1

            # verify if name is a non empty and non all white space string
            if type(product.get('product_name_fr')) != str :
                problems += 1
            elif product.get('product_name_fr').strip() == "" :
                problems += 1

            # verify if brand(s) is(are) a non empty and non all white space string
            if type(product.get('brands')) != str :
                problems += 1
            elif product.get('brands').strip() == "" :
                problems += 1

            # verify if description is a non empty and non all white space string
            if type(product.get('ingredients_text_fr')) != str :
                problems += 1
            elif product.get('ingredients_text_fr').strip() == "" :
                problems += 1

            # verify if categories are a non empty list
            if type(product.get('categories_tags')) != list :
                problems += 1
            elif product.get('categories_tags') == [] :
                problems += 1

            # verify if healthyness is a non empty and non all white space string
            if type(product.get('nutrition_grade_fr')) != str :
                problems += 1
            elif product.get('nutrition_grade_fr').strip() == "" :
                problems += 1

            # verify if popularity is an integer
            if type(product.get('unique_scans_n')) != int :
                problems += 1

            # verify if store(s) is(are) a non empty and non all white space string
            if type(product.get('stores')) != str :
                problems += 1
            elif product.get('stores').strip() == "" :
                problems += 1

            # verify if url is a non empty and non all white space string
            if type(product.get('url')) != str :
                problems += 1
            elif product.get('url').strip() == "" :
                problems += 1

            # verify if any value is "Unknown" or "None" writen as string
            if "Unknown" in list(product.values()):
                problems += 1
            elif "None" in list(product.values()):
                problems += 1

            # if any verification raises a problem, copy product in sparse_products list
            if problems > 0:
                sparse_products.append(product)
                print("Products with lack of informations : ", len(sparse_products))
            # if everything is in order, copy product in valid_products list
            else:
                valid_products.append(product)
                print("Valid products : ", len(valid_products))

        # keep only valid products in class attribute
        self.products = valid_products 


class Product():

# Instances are individual products
# Informations must be of type dict and contains each criteria:
# code,product_name_fr,brands,ingredients_text_fr,nutrition_grade_fr,unique_scans_n,stores,url

    def __init__(self, category, informations):
        self.category = category
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
        return "code = " + str(self.code) + "\n" + "name = " + str(self.name) + "\n" + "brands = " + str(self.brand) + "\n" + "description = " + str(self.description) +  "\n" + "categories = " + str(self.categories) +  "\n" + "healthyness = " + str(self.healthyness) + "\n" + "popularity = " + str(self.popularity) + "\n" + "stores = " + str(self.stores) + "\n" + "url = " + str(self.url)


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

    """def insert_datas(self, informations):
        pass"""

    def fetch_datas(self, informations):
        pass

    def create_user(self, informations):
        # insert data in users table
        pass

    def verify(self, instructions):
        # Verifies if instructions are valid
        # Executes the intructions if so
        # Returns a string in either way describing result
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
        print(self.verify("self.connector.commit()"))

        # leave history by using self.insert_data() and self.history

        self.cursor.close()
        self.connector.close()

        if self.result == "OK":
            self.result = True


class Database():

    tables_created = False
    categories_inserted = False
    product_inserted = False

    @classmethod
    def create_tables(cls):
        if cls.tables_created == False:
            results = []
            for i in cf.TABLES:
                print(i)
                action = """self.create_table("{}, {}".format(i, cf.TABLES.get(i))"""
                i = DatabaseInterraction(action)
                results.append(i.result)
        
        for element in results:
            if element == "OK":
                cls.tables_created = True
            else:
                cls.tables_created = False
                break

    @classmethod
    def insert_product(cls, product):
        # product must be an instance of class Product
        action = """self.insert_datas("{}".format(product))"""
        ref = product.code
        ref = DatabaseInterraction(action)

        return ref.result

    @classmethod
    def get_off_datas(cls):
        for i in cf.categories:
            print(i)
            i = Category(i)
            i.clean_datas()
            for j in i.products:
                j = Product(i.name, j)
                print(j)
                print(Database.insert_product(j))
            # print(i.subcategories)
            # print(len(i.subcategories))

####################################################################################################

def install():
    """Database.create_tables()"""
    Database.get_off_datas()

def list_categories():
    # if DatabaseSetting.tables_created:
    # function to browse DB using class DatabaseInterraction and get main categories
    # must return a list
    pass

def list_products(category):
    # function to browse DB using class DatabaseInterraction and get products in a given category
    # must return a list
    pass

def substitute(user, login, product_code):
    # check if user exists in database. If not, create it.
    # check if a subtitute have already been found for given product
    # if so, jump next step
    # algorythm for substitute finding
    # must return a dict
    pass

def save_search(user, login, product_code, substitute_code):
    # inserts user searches in a special table
    # this must be a user choice
    pass

install()