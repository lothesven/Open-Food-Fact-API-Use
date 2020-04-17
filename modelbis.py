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
        self.clean_datas()
        self.subcategories = self.get_subcategories()

    def get_products(self):
        '''Use module requests to get products on Open Food Facts'''
        products = list()
        for grade in cf.GRADES:
            payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': self.name,
                'tagtype_1': 'nutrition_grade_fr',
                'tag_contains_1': 'contains',
                'tag_1': grade,
                'fields': cf.CRITERIAS,
                'sort_by': 'unique_scans_n',
                'json': 'true',
                'page_size': '5'
            }
            print(payload)
            request = requests.get(cf.URL, params=payload)
            for product in request.json().get('products'):
                products.append(product)

        return products

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

            # verify if subcategories are a non empty list
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

            # if everything is in order, copy product in valid_products list
            else:
                valid_products.append(product)

        print("Products with lack of informations : ", len(sparse_products))
        print("Valid products : ", len(valid_products))

        # keep only valid products in class attribute
        self.products = valid_products

    def get_subcategories(self):
        '''Browse every product from get_products to find subcategories'''
        subcategories = list()
        for product in self.products: # browse list of products
            for subcategory in product.get('categories_tags'): # browse list of subcategories
                if subcategory not in subcategories: # keep any subcategory not in subcategories yet
                    subcategories.append(subcategory)
        return subcategories


class Product():

# Instances are individual products
# category is a string refering to primary category defined in config.py
# Informations must be of type dict and contains each criteria:
# code,product_name_fr,brands,ingredients_text_fr,categories_tags,nutrition_grade_fr,unique_scans_n,stores,url

    def __init__(self, category, subcategories, informations):

        self.informations = informations

        subcategories_booleans = list()
        for subcategory in subcategories:
            if subcategory in informations.get('categories_tags'):
                subcategories_booleans.append(1)
            else:
                subcategories_booleans.append(0)

        self.informations = {
            'code': informations.get('code'),
            'name': informations.get('product_name_fr'),
            'brands':informations.get('brands'),
            'category': category,
            'subcategories': str(subcategories_booleans),
            'description': informations.get('ingredients_text_fr'),
            'healthyness': informations.get('nutrition_grade_fr'),
            'popularity': informations.get('unique_scans_n'),
            'stores': informations.get('stores'),
            'url': informations.get('url')
        }

    def __str__(self):
        return str(self.informations)


class Procedures():

    all_tables_created = False
    all_products_inserted = False

    @classmethod
    def db_connexion(cls):
        # for later code factorisation
        pass
    
    @classmethod
    def create_tables(cls):
        if cls.all_tables_created == False:
            tables_created = 0
            
            try:
                print("Connecting to {}: ".format(cf.DB_NAME), end='')
                cnx = mysql.connector.connect(**cf.CREDENTIALS) # connexion handling instance
                cursor = cnx.cursor()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
            else:
                print("OK")
        
            for table_name in cf.TABLES.keys():
                table_description = cf.TABLES[table_name]
                try:
                    print("Creating table {}: ".format(table_name), end='')
                    cursor.execute(table_description)
                    tables_created += 1
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                        tables_created += 1 # created beforehand but created nonetheless
                    else:
                        print(err.msg)
                else:
                    print("OK")
        
            cursor.close()
            cnx.close()
        
        if tables_created == len(cf.TABLES):
            cls.all_tables_created = True
        
    @classmethod
    def drop_tables(cls):
        tables_deleted = 0
        
        try:
            print("Connecting to {}: ".format(cf.DB_NAME), end='')
            cnx = mysql.connector.connect(**cf.CREDENTIALS) # connexion handling instance
            cursor = cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("OK")

        for table_name in reversed(cf.TABLES.keys()):
            try:
                print("Droping table {}: ".format(table_name), end='')
                cursor.execute("DROP TABLE {}".format(table_name))
                tables_deleted += 1
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_BAD_TABLE_ERROR:
                    print("Table doesn't exist")
                    tables_deleted += 1 # deleted beforehand but deleted nonetheless
                else:
                    raise
            else:
                print("OK")
        
        cursor.close()
        cnx.close()
        
        if tables_deleted: # if even only one table have been droped
            cls.all_tables_created = False

    @classmethod
    def insert_products_from_category(cls, category):
        # category refer to an instance of class Category
        try:
            print("Connecting to {}: ".format(cf.DB_NAME), end='')
            cnx = mysql.connector.connect(**cf.CREDENTIALS) # connexion handling instance
            cursor = cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("OK")

        for j in category.products:
            j = Product(category.name, category.subcategories, j)
            try:
                print("Inserting product {}: ".format(j.informations['subcategories']), end='')
                cursor.execute(cf.PRODUCT_INSERT, j.informations)
            except mysql.connector.Error as err:
                print(err)
            else:
                print("Insertion ok")
        
        cnx.commit()

        cursor.close()
        cnx.close()

    @classmethod
    def get_off_datas(cls):
        for i in cf.CATEGORIES:
            print(i)
            i = Category(i)
            print("Number of different subcategories :", len(i.subcategories))
            Procedures.insert_products_from_category(i)

####################################################################################################

def install():
    # create every table begining by history, fill table products
    Procedures.create_tables()
    print("Tables created : ", Procedures.all_tables_created)
    Procedures.get_off_datas()

def uninstall():
    Procedures.drop_tables()

def manage_user(name, login, action):
    # when user launch the program leave choice: login or register
    # gather name and login using an input in either choice
    # if user try to log, action is log, else action is create
    # verify inputs for any devious attempts
    # check if user already exist
    # if action is log and user exist, return "login successfull"
    # elif action is create and user doesn't exist, create it and return "user registered"
    # else return an error message
    pass

def list_categories():
    try:
        print("Connecting to {}: ".format(cf.DB_NAME), end='')
        cnx = mysql.connector.connect(**cf.CREDENTIALS) # connexion handling instance
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("OK")

    query = "SELECT category FROM Products"

    cursor.execute(query)

    categories = []

    for category_tuple in cursor:
        category = category_tuple[0]
        if category not in categories:
            categories.append(category)

    cursor.close()
    cnx.close()

    return categories

def list_products(category):
    try:
        print("Connecting to {}: ".format(cf.DB_NAME), end='')
        cnx = mysql.connector.connect(**cf.CREDENTIALS) # connexion handling instance
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("OK")

    query = ("SELECT name, code FROM Products "
            "WHERE category = %s")

    cursor.execute(query, (category,))

    products = []

    for (name, code) in cursor:
        product = (name, code)
        products.append(product)

    cursor.close()
    cnx.close()

    return products

def substitute(user, login, product_code):
    # check if a subtitute have already been found for given product
    # if so, directly return it
    # else process algorythm for substitute finding
    # return a product with extended informations
    pass

def save_search(user, login, product_code, substitute_code):
    # inserts user searches in a special table
    # this must be a user choice
    pass

uninstall()
install()
print(list_categories())
print(list_products("Fromages"))