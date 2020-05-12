# -*- coding: utf-8 -*

""" 
This module contains only constants used by the application.
It is only accessed by module "Model" and contains:

- a list of categories to get from Open Food Facts (OFF)
- many important parameters used for requests on OFF
- informations for database handling
"""

CATEGORIES = [
    "Boissons-gazeuses", 
    "Biscuits-au-chocolat", 
    "Jus-de-fruit-pur-jus", 
    "Yaourts", 
    "Fromages", 
    "Chips", 
    "Pâtes-à-tartiner",
    "Céréales-pour-petit-déjeuner",
    "Céréales-en-grains",
    "Pains", 
    "Soupes",
    "Conserves",
    "Spaghetti",
    "Glaces",
    "Saucissons",
    "Huiles",
    "Jambons",
    "Beurres",
    "Chocolats",
    "Sauces"
]

GRADES = ['A', 'B', 'C', 'D', 'E']

SIZE = 20

CRITERIAS = (
    'categories_tags,'
    'code,'
    'product_name_fr,'
    'brands,'
    'ingredients_text_fr,'
    'nutrition_grade_fr,'
    'unique_scans_n,'
    'stores,'
    'url'
    )

URL = "https://fr.openfoodfacts.org/cgi/search.pl?"


##########################################################


DB_NAME = 'ratatouille'

CREDENTIALS = {
  'user': 'Pur',
  'password': 'Beurre',
  'host': 'localhost',
  'database': DB_NAME,
  'raise_on_warnings': True
}

TABLES = {
'Products' : (
    "CREATE TABLE IF NOT EXISTS `Products` ("
    "  `code` BIGINT NOT NULL PRIMARY KEY,"
    "  `name` TEXT NOT NULL,"
    "  `brands` TEXT NOT NULL,"
    "  `category` VARCHAR(50) NOT NULL,"
    "  `subcategories` TEXT NOT NULL,"
    "  `description` TEXT NOT NULL,"
    "  `healthyness` CHAR(1) NOT NULL,"
    "  `popularity` INT NOT NULL,"
    "  `stores` TEXT NOT NULL,"
    "  `url` TEXT NOT NULL"
    ") ENGINE=InnoDB"
    ),
'Users' : (
    "CREATE TABLE IF NOT EXISTS `Users` ("
    "  `ID` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "  `name` VARCHAR(20) NOT NULL UNIQUE,"
    "  `login` VARCHAR(20) NOT NULL"
    ") ENGINE=InnoDB"
    ),
'Substitutes' : (
    "CREATE TABLE IF NOT EXISTS `Substitutes` ("
    "  `ID` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "  `user_ID` INT UNSIGNED NOT NULL,"
    "  `date` TEXT NOT NULL,"
    "  `product_code` BIGINT NOT NULL,"
    "  `substitute_code` BIGINT NOT NULL,"
    "  CONSTRAINT `fk_searches_user_ID` FOREIGN KEY (`user_ID`) "         
    "     REFERENCES `Users` (`ID`),"
    "  CONSTRAINT `fk_searches_product_code` FOREIGN KEY (`product_code`) "         
    "     REFERENCES `Products` (`code`)"
    ") ENGINE=InnoDB"
    )
}

PRODUCT_INSERT = ("INSERT INTO Products "
              "(code, name, brands, category, subcategories, description, healthyness, popularity, stores, url) "
              "VALUES (%(code)s, %(name)s, %(brands)s, %(category)s, %(subcategories)s, %(description)s, %(healthyness)s, %(popularity)s, %(stores)s, %(url)s)")

USER_INSERT = ("INSERT INTO Users "
              "(name, login) "
              "VALUES (%(user)s, %(login)s)")

SUBSTITUTE_INSERT = ("INSERT INTO Substitutes "
              "(user_ID, date, product_code, substitute_code) "
              "VALUES (%(user_ID)s, %(date)s, %(product_code)s, %(substitute_code)s)")