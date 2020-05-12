# -*- coding: utf-8 -*

"""
This module receives intructions from "controler.py"
It works as Model of an MVC patern
It uses "config.py" to access many constants

The module contains three classes:
- Category() and Product() that are regular OOP modelisations
- DatabaseProcedure() that contains only procedures

The module contains also many functions outside of classes.

Functions are accessed directly by controler
Classes aren't

This module is the core of the application and can:
- get datas from Open Food Facts' API
- refine these datas to remove incomplete informations
- create defined tables in defined database that must be created beforehand (cf Readme.md)
- insert new products, users or substitute searches in related tables
- get informations concerning a specific product stored in database
- get list of category and list of products stored in database
- verify registration of a user
- find a healthy substitute for any given product stored in database

"""

import json
from random import randrange
from math import floor
from datetime import date, datetime, timedelta

import requests
import mysql.connector as mc

import config as cf

class Category():
    """
    Instances are objects that contains a list of individual products
    found in specified category on Open Food Facts
    """

    def __init__(self, name):
        # name refer to a string defined in config.py

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
                'page_size': cf.SIZE
            }
            request = requests.get(cf.URL, params=payload)

            for product in request.json().get('products'):
                products.append(product)

        return products

    def clean_datas(self):
        """Removes from self.products any product with bad or missing informations"""

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

        # keep only valid products in class attribute
        self.products = valid_products

    def get_subcategories(self):
        '''Browse every valid product to find all the diferent subcategories'''

        subcategories = list()

        for product in self.products: 
            for subcategory in product.get('categories_tags'): 
                if subcategory not in subcategories: 
                    subcategories.append(subcategory)

        return subcategories


class Product():
    """
    Instances are individual products from Open Food Facts
    They are created using informations from Category() instances
    """

    def __init__(self, category, subcategories, informations):
        # category is a string refering to primary category name defined in config.py
        # subcategories is the related list of every possible subcategory found on OFF
        # informations must be of type dict and contains each criteria:
            # code
            # product_name_fr
            # brands
            # ingredients_text_fr
            # categories_tags
            # nutrition_grade_fr
            # unique_scans_n
            # stores
            # url

        self.informations = informations

        subcategories_booleans = list()
        for subcategory in subcategories:
            if subcategory in informations.get('categories_tags'):
                subcategories_booleans.append(1)
            else:
                subcategories_booleans.append(0)

        # subcategories_booleans have the same lenght as subcategories
        # it's therefore the same for every product of a given category
        # there is a "1" each time a subcategory from the list of subcategories is found

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
    """
    This class is not supposed to be instanciated
    It contains various procedures for database interactions
    """

    connection = None
    cursor = None

    @classmethod
    def connect(cls):
        """
        No argument. Initiate connection to database.
        Update class attributes.
        Returns mysql.connector connector and cursor objects.
        """

        try:
            print("Connecting to {}: ".format(cf.DB_NAME), end='')
            cls.connection = mc.connect(**cf.CREDENTIALS) # connexion handling instance
            cls.cursor = cls.connection.cursor()
        except mc.Error as err:
            if err.errno == mc.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mc.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print("OK")
        
        return cls.connection, cls.cursor
    
    @classmethod
    def disconnect(cls):
        """
        No argument. Closes connection to database.
        Returns None.
        """

        try:
            cls.cursor.close()
            cls.connection.close()
        except:
            print("An error occured for cursor and/or connexion closing.")
    
    @classmethod
    def create_tables(cls, table_list = cf.TABLES.keys()):
        """
        If specified, table_list argument must be a list of strings
        Each string must refer to a key in TABLES dictionary from config.py
        Might be usefull to create new tables if program gets bigger for content update
        """

        tables_created = 0
        
        cls.connect()
    
        for table_name in table_list:
            try:
                table_description = cf.TABLES[table_name]
            except KeyError: 
                # handle possible error when table_list contains strings not in cf.TABLES keys
                print("{} is not specified in config.py".format(table_name))
                continue

            try:
                print("Creating table {}: ".format(table_name), end='')
                cls.cursor.execute(table_description)
                tables_created += 1
            except mc.Error as err:
                if err.errno == mc.errorcode.ER_TABLE_EXISTS_ERROR:
                    print("this table already exists.")
                    tables_created += 1 
                    # created beforehand but created nonetheless
                else:
                    print(err.msg)
            else:
                print("OK")
    
        cls.disconnect()

        print("{} tables are created out of {} requested.".format(tables_created, table_list))  
    
        if tables_created == len(table_list):
            return True

    @classmethod
    def drop_tables(cls, table_list = cf.TABLES.keys()):
        """
        If specified, table_list argument must be a list of strings
        Each string must refer to a key in TABLES dictionary from config.py
        If tables have constraints, put them at the end of the list to be droped first
        """

        tables_deleted = 0
    
        cls.connect()

        for table_name in reversed(table_list):
            # drop last in the list first. On default drop table Substitutes first.
            
            try:
                print("Droping table {}: ".format(table_name), end='')
                cls.cursor.execute("DROP TABLE {}".format(table_name))
            except mc.Error as err:
                if err.errno == mc.errorcode.ER_BAD_TABLE_ERROR:
                    print("Table doesn't exist")
                    if table_name in cf.TABLES.keys():
                        tables_deleted += 1 
                        # deleted beforehand but deleted nonetheless
                else:
                    raise
            else:
                tables_deleted += 1
                print("OK")
        
        cls.disconnect()

        print("{} tables are deleted out of {} requested.".format(tables_deleted, table_list))  
    
        if tables_deleted == len(table_list):
            return True

    @classmethod
    def insert_products_from_category(cls, category):
        """
        Category argument refers to an instance of class Category
        Instanciates Product class objects using data from a Category instance
        Inserts attributes of Product instances in database
        """

        if isinstance(category, Category):
            cls.connect()

            for j in category.products:
                j = Product(category.name, category.subcategories, j)
                try:
                    print("Inserting product {}: ".format(j.informations['subcategories']), end='')
                    cls.cursor.execute(cf.PRODUCT_INSERT, j.informations)
                except mc.Error as err:
                    print(err)
                else:
                    print("OK")
            
            cls.connection.commit()

            cls.disconnect()
        else:
            print("Error: Argument specified must be an instance of class Category")

    @classmethod
    def get_off_datas(cls):
        """
        Instanciate Category class objects, 
        Then inserts theirs products in database
        """

        for i in cf.CATEGORIES:
            print("Downloading products of category :", i, "...")
            i = Category(i)
            print("Done.")
            cls.insert_products_from_category(i)

    @classmethod
    def check_user(cls, user, login):
        """
        Verifies if specified user and login are in database
        User and login arguments must be spaceless strings
        """

        user = "".join(str(user).split())
        login = "".join(str(login).split())
        # Extra protection against SQL injections

        cls.connect()

        query = "SELECT login, ID FROM Users WHERE name = '{}'".format(user)

        try:
            print("Checking login for user {}: ".format(user), end='')
            cls.cursor.execute(query)
        except mc.Error as err:
            print(err)
        else:
            try:
                result = cls.cursor.fetchone()
                registered_login = result[0]
            except TypeError:
                # cursor is empty and result is a NoneType object
                print("User not found")     
            else:
                if registered_login == login:
                    print("User name and login are correct")
                    return True
                elif registered_login != login:
                    print("Incorrect login")
        finally:
            cls.disconnect()

    @classmethod
    def create_user(cls, user, login):
        """
        Insert user and login in table Users
        User and login arguments must be spaceless strings
        """

        cls.connect()

        try:
            print("Creating user {}: ".format(user), end='')
            cls.cursor.execute(cf.USER_INSERT, {"user": user, "login": login})
        except mc.Error as err:
            if err.errno == 1062 and err.sqlstate == "23000":
                print("User already registered")
            else:
                print(err)
        else:
            cls.connection.commit()
            print("Creation ok")
            return True
        
        finally:
            cls.disconnect()
###
    @classmethod
    def product_informations(cls, product_code, informations = "code, name, healthyness, brands, description, stores, url"):
        """
        Get specified informations (2nd argument) provided a product code (1st argument)
        Any column content of table Products can be requested provided column name as a string
        If several columns are requested, specify names with this syntax: "columnname1, columnname2, ..."
        Information argument is optionnal. 
        If not specified, a default set of information will be retrieved.
        """

        cls.connect()

        query = "SELECT {} FROM Products WHERE code = '{}'".format(informations, product_code)

        try:
            print("Retrieving informations from product '{}': ".format(product_code), end='')
            cls.cursor.execute(query)
        except mc.Error as err:
            print(err)
        else:
            try:
                iter(cls.cursor)
            except TypeError:
                print("Cursor definition encountered an unknown issue causing it not to be iterable")
            else:
                product_informations = cls.cursor.fetchall()
                print("\n", product_informations)
                if len(product_informations) > 1:
                    return product_informations
                elif len(product_informations) == 1:
                    return product_informations[0]
                else:
                    print("Informations not found")
        finally:
            cls.disconnect()

    @classmethod
    def substitute(cls, product_code):
        """
        Main method taking as argument code of a single product.
        Tries to retrieve the substitute in table Substitutes.
        Find substitute and return it's code.
        """

        cls.connect()

        query = "SELECT substitute_code FROM Substitutes WHERE product_code = {}".format(product_code)

        cls.cursor.execute(query)
        result = cls.cursor.fetchone()

        try:
            cls.cursor.fetchall() # empties cursor if any entry have been found
        except mc.errors.InterfaceError:
            pass # cursor is already empty. Move on.

        cls.disconnect()

        # check if a subtitute have already been found for given product
        # if so, directly return it

        try:
            result[0]
        except TypeError:
            # cursor is empty and result is a NoneType object
            print("No substitute found for this product so far.")
        else:
            return result[0]
        
        # else process algorythm for substitute finding.
        # finds specified product's category, nutrition grade and subcategories

        category, healthyness, subcategories = DatabaseProcedures.product_informations(product_code, "category, healthyness, subcategories")
        
        subcategories = subcategories[1:-1].split(', ')
        # remove "[" and "]" in the string, then remove ', ' 
        # to keep only 0 and 1 as a list of strings
        
        print("category is: ", category)
        print("healthyness is: ", healthyness)
        print("subcategories are: ", subcategories)

        cls.connect()

        # gets every product that have:
        # - same category
        # - same or better healthyness
        # - different code

        query = ("SELECT code, subcategories, healthyness, popularity FROM Products WHERE category = '{}' AND healthyness <= '{}' AND code != '{}'".format(category, healthyness, product_code))

        cls.cursor.execute(query)
        result = cls.cursor.fetchall() 
        # each product found should be represented as a 4 elements tuple

        cls.disconnect()

        similar_products = []
        max_proximity = 0
        min_proximity = 999

        for product in result:

            proximity = 0
            # constructed indicator for each potential substitute based on subcategories comparison
            # if proximity is high, potential substitute is similar to initial product

            subcategory_list = product[1][1:-1].split(', ') 
            # remove "[" and "]" in the string, then remove ', ' 
            # to keep only 0 and 1 as a list of strings

            for index in range(len(subcategory_list)):
                if subcategory_list[index] == subcategories[index]:
                    proximity += 1
            # proximity is incremented every time a potential substitute have a subcategory 
            # in common with the initial product
            
            if proximity > max_proximity:
                max_proximity = proximity
            
            if proximity < min_proximity:
                min_proximity = proximity

            similar_products.append([product[0], proximity, product[2], product[3]])

        # similar_products is the list of every products of same category as initial product
        # with calculated proximity indicator replacing subcategories list

        indexes = []
        delta_proximity = max_proximity - min_proximity

        closeness = 0.95
        # arbitrary number between 0 and 1
        # higher leads to closer to max_proximity as minimum target for proximity

        proximity_target = floor(min_proximity + delta_proximity * closeness)

        print("proximity max is : ", max_proximity)
        print("proximity min is : ", min_proximity)
        print("delta is : ", delta_proximity)
        print("proximity target is : ", proximity_target)

        for index in range(len(similar_products)):
            if similar_products[index][1] < proximity_target:
                # if closeness is set to 1, proximity_target equals max_proximity
                # "<" keeps proximity_target "<=" would have led to discard all potential substitutes
                indexes.append(index)

        # indexes is a list of indexes in similar_poducts list
        # where proximity is below proximity_target

        for index_element in reversed(indexes): 
            # indexes is reversed to have indexes in descending order and avoid IndexError
            similar_products.pop(index_element)
            # removes every product with proximity lower than defined proximity

        similar_products.sort(key = lambda a : a[1], reverse = True)
        print("sorted and cleaned list : \n", similar_products)
        # this command sorts similar_products list based on proximity in descending order

        if healthyness == "A" or healthyness == "a": 
            print("already healthy")
            # sorting using healthyness is irrelevant here so we use popularity
            similar_products.sort(key = lambda a : a[3], reverse = True) 
            # on same popularity, proximity order is unchanged
            return similar_products[0][0] 

        else: 
            # for any other healthyness than "A" sorting healthyness is needed
            similar_products.sort(key = lambda a : a[2]) 
            # on same healthyness, proximity order remains unchanged
            
            equally_healthy_products = []

            for index in range(len(similar_products)):
                if similar_products[0][2] == similar_products[index][2]:
                    # check for equally healthy products in similar_products
                    equally_healthy_products.append(similar_products[index])
                    # this keeps only highest healthyness products with proximity order unchanged between them
            
            print("List of products with same healthyness :\n", equally_healthy_products)

            if len(equally_healthy_products) == 1: 
                # if the higher healthyness concerns only one similar_product
                return similar_products[0][0] 
                # then return this product's code 
            else: 
                # higher healthyness concerns many products so further sorting is needed
                equally_healthy_products.sort(key = lambda a : a[3], reverse = True)
                # products here are equally healthy
                # list is finaly sorted using popularity
                # on same popularity, proximity order remains unchanged

                equally_healthyandpopular_products = []

                for index in range(len(equally_healthy_products)):
                    if equally_healthy_products[0][3] == equally_healthy_products[index][3]:
                        # check for equally healthy and equally popular products
                        equally_healthyandpopular_products.append(equally_healthy_products[index])

                print("List of products with same healthyness and popularity :")
                print(equally_healthyandpopular_products)

                if len(equally_healthyandpopular_products) == 1:
                    # if the higher popularity on higher healthyness concerns only one product
                    return equally_healthy_products[0][0]
                    # then return this product's code
                else:
                    # higher healthyness and higher popularity may concern many products
                    random_index = randrange(0, len(equally_healthyandpopular_products))
                    # in such case, randomly pick one of them
                    return equally_healthyandpopular_products[random_index]

        # if healthyness is equal between products, choose highest popularity
        # if there is still equalities, choose highest popularity
        # if there is still equalities, then randomly choose

    @classmethod
    def record_substitute(cls, user_id, product_code, substitute_code):
        """
        Method to insert data in table "Subtitutes"
        Takes 3 arguments: user ID, product code and substitute code
        Each argument is a string representing an integer
        """
        
        cls.connect()

        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        try:
            print("Registering substitute {}: ".format(substitute_code), end='')
            values = {"user_ID": user_id, "date": date, "product_code": product_code, "substitute_code": substitute_code}
            cls.cursor.execute(cf.SUBSTITUTE_INSERT, values)
        except mc.Error as err:
            print(err)
        else:
            cls.connection.commit()
            print("Substitute saved")
            return True
        
        finally:
            cls.disconnect()



####################################################################################################

# Below are functions that are accessed by controler

def is_installed():
    """
    Procedure to check if database have already been installed
    Verifies if there is as many tables in database as tables specified in config.py
    Returns True if so
    """

    cnx, cursor = DatabaseProcedures.connect()

    query = "SHOW TABLES"

    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    cnx.close()

    if len(result) == len(cf.TABLES.keys()):
        return True

def install():
    """
    Creates every table specified in config.py, respecting order
    Fill table Products with Open Food Facts data
    Returns True if process is succesfull
    """

    result = DatabaseProcedures.create_tables()
    if result:
        print("Tables successfully created.")
        DatabaseProcedures.get_off_datas()
    else:
        print("Some tables were not successfully installed. Please contact assistance.")
    
    return result

def uninstall():
    """
    Drops every table begining by Substitutes as table has constraints
    Uses tables in config.py in reverse order
    Returns True if process is successfull
    """

    result = DatabaseProcedures.drop_tables()
    return result

def manage_user(name, login, action):
    """
    First two arguments "name" and "login" are user inputs
    Checks user inputs to prevent SQL injections
    Third argument is provided by controller as a result of user actions
    """

    str_name = str(name)
    str_login = str(login)

    # verify inputs for any devious attempts
    # removes all whitespace characters (space, tab, newline, and so on) 
    # compare result to user input to detect devious SQL injection

    if "".join(str_name.split()) == name and "".join(str_login.split()) == login:

        # check if user already exist
        if DatabaseProcedures.check_user(name, login):
            if action == "log": # if action is log, everything is fine
                print("Login successfull")
                return True
            else: 
                # user and login exists but action is "create"
                print("Error: user and login already exists")
        else: 
            # user and/or login are not found
            if action == "create": 
                # try to create user
                if DatabaseProcedures.create_user(name, login):
                    print("User registered")
                    return True
                else:
                    # upon creation failure
                    print("User not registered")
            else: 
                # action is "log" but user/login haven't been found
                print("Could not find user and login specified")

    else:
        # user input contains at least one whitespace caracter
        print("Whitespace caracters are not allowed")

def list_categories():
    """
    Retrieves categories in database
    Should return the same list as the one in config.py
    May still be usefull if program becomes more complex
    """

    cnx, cursor = DatabaseProcedures.connect()

    query = "SELECT category FROM Products"

    cursor.execute(query)
    result = cursor.fetchall()

    categories = []

    try:
        iter(result)
    except TypeError:
        print("Result is empty and not iterable")
    else:
        for category_tuple in result:
            category = category_tuple[0]
            if category not in categories:
                categories.append(category)
    finally:
        cursor.close()
        cnx.close()

    return categories

def list_products(category):
    """
    Argument category is a string representing a category that must be in database
    This function returns a list of products with name, brands and code
    """

    cnx, cursor = DatabaseProcedures.connect()

    query = ("SELECT name, brands, code FROM Products "
            "WHERE category = %s")

    cursor.execute(query, (category,))
    result = cursor.fetchall()

    products = []

    try:
        iter(result)
    except TypeError:
        print("Result is empty and not iterable")
    else:
        for (name, brands, code) in result:
            products.append((name, brands, code))
    finally:
        cursor.close()
        cnx.close()

    return products

def get_substitute(product_code):
    """
    Gets a string representing a product code as argument.
    Returns a suitable subtitute with many data to be shown to user.
    """

    substitute_code = DatabaseProcedures.substitute(product_code)
    sub = DatabaseProcedures.product_informations(substitute_code)
    substitute_informations = {
        "code": sub[0],
        "name": sub[1],
        "nutrition score": sub[2], 
        "brands": sub[3], 
        "description": sub[4], 
        "stores": sub[5],
        "url": sub[6]
        }
    return substitute_informations

def get_informations(product_code):
    """
    Gets a string representing a product code as argument.
    Returns many data related to this product to be shown to user.
    """

    prod = DatabaseProcedures.product_informations(product_code)
    product_informations = {
        "code": prod[0],
        "name": prod[1],
        "nutrition score": prod[2], 
        "brands": prod[3], 
        "description": prod[4], 
        "stores": prod[5],
        "url": prod[6]
        }
    return product_informations

def save_search(user, login, product_code, substitute_code):
    """
    Retrieves logged user's ID using first and second arguments (user, login)
    Inserts user's search results using third and fourth arguments (product code, substitute code)
    Insertion is done on table Substitutes
    Returns True if insertion is successfull
    """

    user_ID = manage_user(user, login, "log")
    if user_ID:
        if DatabaseProcedures.record_substitute(user_ID, product_code, substitute_code):
            return True
