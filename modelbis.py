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


class DatabaseProcedures():
    # This class is not supposed to be instanciated
    # Contains various procedure for database interactions

    all_tables_created = False
    all_products_inserted = False

    connection = None
    cursor = None

    @classmethod
    def connect(cls):
        try:
            print("Connecting to {}: ".format(cf.DB_NAME), end='')
            cls.connection = mysql.connector.connect(**cf.CREDENTIALS) # connexion handling instance
            cls.cursor = cls.connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("OK")
        
        return cls.connection, cls.cursor
    
    @classmethod
    def disconnect(cls):
        try:
            cls.cursor.close()
            cls.connection.close()
        except:
            print("An error occured for cursor and/or connexion closing.")
    
    @classmethod
    def create_tables(cls, table_list = cf.TABLES.keys()):
        # if specified, table_list argument must be a list of strings
        # might be usefull if program gets bigger for content update
        if cls.all_tables_created == False:
            tables_created = 0
            
            cls.connect()
        
            for table_name in table_list:
                try:
                    table_description = cf.TABLES[table_name]
                except: # handle possible error when table_list contains strings not in cf.TABLES keys
                    continue

                try:
                    print("Creating table {}: ".format(table_name), end='')
                    cls.cursor.execute(table_description)
                    tables_created += 1
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                        tables_created += 1 # created beforehand but created nonetheless
                    else:
                        print(err.msg)
                else:
                    print("OK")
        
            cls.disconnect()
        
        if tables_created == len(cf.TABLES):
            cls.all_tables_created = True
        
        return tables_created

    @classmethod
    def drop_tables(cls, table_list = cf.TABLES.keys()): # maybe for specific table ?
        # if specified, table_list argument must be a list of strings
        tables_deleted = 0
    
        cls.connect()

        for table_name in reversed(table_list):
            try:
                print("Droping table {}: ".format(table_name), end='')
                cls.cursor.execute("DROP TABLE {}".format(table_name))
                tables_deleted += 1
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_BAD_TABLE_ERROR:
                    print("Table doesn't exist")
                    if table_name in cf.TABLES.keys():
                        tables_deleted += 1 # deleted beforehand but deleted nonetheless
                else:
                    raise
            else:
                print("OK")
        
        cls.disconnect()
    
        if tables_deleted: # if even only one table have been droped
            cls.all_tables_created = False
        
        return tables_deleted

    @classmethod
    def insert_products_from_category(cls, category):
        # category refer to an instance of class Category

        cls.connect()

        for j in category.products:
            j = Product(category.name, category.subcategories, j)
            try:
                print("Inserting product {}: ".format(j.informations['subcategories']), end='')
                cls.cursor.execute(cf.PRODUCT_INSERT, j.informations)
            except mysql.connector.Error as err:
                print(err)
            else:
                print("Insertion ok")
        
        cls.connection.commit()

        cls.disconnect()

    @classmethod # Still to be tested
    def check_user(cls, user, login):
        # Verifies if specified user and login are in database
        cls.connect()

        query = "SELECT login FROM Users WHERE name = '{}'".format(user)

        try:
            print("Checking login for user {}: ".format(user), end='')
            cls.cursor.execute(query)
        except mysql.connector.Error as err:
            print(err)
        else:
            try:
                iter(cls.cursor)
            except TypeError:
                print("Cursor definition encountered an unknown issue causing it not to be iterable")
            else:
                registered_login = cls.cursor.fetchone()
                if registered_login:
                    if registered_login == login: # cursor content equals login
                        print("User name and login are correct")
                        return True
                    elif registered_login != login: # cursor content doesn't match
                        print("Incorrect login")
                else: # cursor is empty
                    print("User not found")
        finally:
            cls.disconnect()

    @classmethod # Still to be tested
    def create_user(cls, user, login):

        cls.connect()
        ID = "NULL"

        try:
            print("Creating user {}: ".format(user), end='')
            cls.cursor.execute(cf.USER_INSERT, (ID, user, login))
        except mysql.connector.Error as err:
            print(err)
            return False
        else:
            cls.connection.commit()
            print("Creation ok")
            return True
        
        finally:
            cls.disconnect()

    @classmethod
    def record_history(cls, user, action, result):
        # procedure to store any action done on database when a user is logged in
        pass

####################################################################################################

def is_installed():
    # check if database have already been installed
    # should be so if every table in config already exist

    cnx, cursor = DatabaseProcedures.connect()

    query = "SHOW TABLES"

    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    cnx.close()

    if len(result) == len(cf.TABLES.keys()):
        return True
    else:
        return False

def install():
    # create every table begining by history and fill table products
    DatabaseProcedures.create_tables()
    print("Tables created : ", DatabaseProcedures.all_tables_created)
    get_off_datas()

def uninstall():
    result = DatabaseProcedures.drop_tables()
    return result

def get_off_datas():
    for i in cf.CATEGORIES:
        print(i)
        i = Category(i)
        print("Number of different subcategories :", len(i.subcategories))
        DatabaseProcedures.insert_products_from_category(i)

def manage_user(name, login, action):
    # verify inputs for any devious attempts
    str_name = str(name)
    str_login = str(login)

    if "".join(str_name.split()) == name and "".join(str_login.split()) == login:
        # removes all whitespace characters (space, tab, newline, and so on) 
        # compare to user input to detect devious SQL injection
        # check if user already exist
        if DatabaseProcedures.check_user(name, login):
            if action == "log": # if action is log, everything is fine
                print("Login successfull")
                return True
            else: # user and login exists but action is create
                print("Error: user and login already exists")
        else: # user and/or login are not found
            if action == "create": # if action is create, then try to create user
                if DatabaseProcedures.create_user(name, login):
                    print("User registered")
                    return True
                else:
                    print("User not registered")
            else: # action is log but user/login haven't been found
                print("Could not find user and login specified")
    else:
        print("Whitespace caracters are not allowed")
    # if user try to log, action is log, else action is create
    
    # if action is log and user exist, return "login successfull"
    # elif action is create and user doesn't exist, create it and return "user registered"
    # else return an error message

def list_categories():

    cnx, cursor = DatabaseProcedures.connect()

    query = "SELECT category FROM Products"

    cursor.execute(query)
    result = cursor.fetchall()

    try:
        iter(result)
    except TypeError:
        print("Result is empty and not iterable")

    categories = []

    for category_tuple in result:
        category = category_tuple[0]
        if category not in categories:
            categories.append(category)

    cursor.close()
    cnx.close()

    return categories

def list_products(category):

    cnx, cursor = DatabaseProcedures.connect()

    query = ("SELECT name, code FROM Products "
            "WHERE category = %s")

    cursor.execute(query, (category,))

    result = cursor.fetchall()

    try:
        iter(result)
    except TypeError:
        print("Result is empty and not iterable")

    products = []

    for (name, code) in result:
        products.append((name, code))

    cursor.close()
    cnx.close()

    return products

def substitute(user, login, product_code):
    return user, login, product_code # for now...
    # check if a subtitute have already been found for given product
    # if so, directly return it
    # else process algorythm for substitute finding:

    # find specified product's category and get every product that have:
    # - same category
    # - same or better healthyness
    # - different code

    # for each product compare subgategories list
    # use a variable "proximity" to quantify how much lists are similar
    # each time elements of same index matches, increment "proximity"

    # weight proximity and healthyness to choose between products which one to return
    # proximity should be quite a high integer while healthyness have only 5 possible values
    # discard any product that has a proximity lower than half maximum proximity
    # let's try to select the product with highest healthyness from top 5 proximity products

    # when product is identified, check database to get extended informations about it
    # if nothing matches return same product and congratulate user for already using best choice.

def save_search(user, login, product_code, substitute_code):
    # inserts user searches in a special table
    # this must be a user choice
    pass