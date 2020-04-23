# Constants used by the applications.
# 
# List of categories to get from Ope Food Facts
# List of key/value used for requests on OFF
# 

# -*- coding: utf-8 -*

CATEGORIES = [
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

GRADES = ['A', 'B', 'C', 'D', 'E']

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

DB_NAME = 'ratatouille'

CREDENTIALS = {
  'user': 'Pur',
  'password': 'Beurre',
  'host': 'localhost',
  'database': DB_NAME,
  'raise_on_warnings': True
}

TABLES = {
'History' : (
    "CREATE TABLE `History` ("
    "  `ID` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "  `user_ID` INT,"
    "  `date` TEXT NOT NULL,"
    "  `action` TEXT NOT NULL,"
    "  `result` TEXT NOT NULL"
    ") ENGINE=InnoDB"
    ),
'Products' : (
    "CREATE TABLE `Products` ("
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
    "CREATE TABLE `Users` ("
    "  `ID` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "  `name` VARCHAR(20) NOT NULL UNIQUE,"
    "  `login` VARCHAR(20) NOT NULL"
    ") ENGINE=InnoDB"
    ),
'Searches' : (
    "CREATE TABLE `Searches` ("
    "  `ID` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,"
    "  `user_ID` INT UNSIGNED NOT NULL,"
    "  `product_code` BIGINT NOT NULL,"
    "  `substitute_code` BIGINT NOT NULL,"
    "  CONSTRAINT `fk_searches_user_ID` FOREIGN KEY (`user_ID`) "         
    "     REFERENCES `Users` (`ID`),"
    "  CONSTRAINT `fk_searches_product_code` FOREIGN KEY (`product_code`) "         
    "     REFERENCES `Products` (`code`)"
    ") ENGINE=InnoDB"
    )
}

HISTORY_INSERT = ("INSERT INTO History "
              "(user_ID, date, action, result) "
              "VALUES (%(user_ID)s, %(date)s, %(action)s, %(result)s)")

PRODUCT_INSERT = ("INSERT INTO Products "
              "(code, name, brands, category, subcategories, description, healthyness, popularity, stores, url) "
              "VALUES (%(code)s, %(name)s, %(brands)s, %(category)s, %(subcategories)s, %(description)s, %(healthyness)s, %(popularity)s, %(stores)s, %(url)s)")

USER_INSERT = ("INSERT INTO Users "
              "(ID, name, login) "
              "VALUES (%(ID)s, %(user)s, %(login)s)")