# Constants used by the applications.
# 
# List of categories to get from Ope Food Facts
# List of key/value used for requests on OFF
# 

# -*- coding: utf-8 -*

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

grades = ['A', 'B', 'C', 'D', 'E']

criterias = (
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

url = "https://fr.openfoodfacts.org/cgi/search.pl?"

credentials = {
  'user': 'Pur',
  'password': 'Beurre',
  'host': 'localhost',
  'raise_on_warnings': True
}

DB_NAME = 'ratatouille'

TABLES = {}
TABLES['Products'] = (
    "CREATE TABLE `Products` ("
    "  `code` int NOT NULL,"
    "  `name` varchar(10) NOT NULL,"
    "  `brand` varchar(30) NOT NULL,"
    "  `categories` text NOT NULL,"
    "  `description` text NOT NULL,"
    "  `healthyness` varchar(1) NOT NULL,"
    "  `popularity` int NOT NULL,"
    "  `stores` varchar(30) NOT NULL,"
    "  `url` varchar(50) NOT NULL,"

    "  PRIMARY KEY (`code`)"
    ") ENGINE=InnoDB"
    )