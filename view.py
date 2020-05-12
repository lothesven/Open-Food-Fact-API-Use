# -*- coding: utf-8 -*

"""
This module receives data from "controler.py"
It works as View of an MVC patern
"""


def initial_display():
    menu = ["Install", "Uninstall", "Log In", "Register", "Exit program"]
    print("\nPlease enter a number between 1 and {} : \n".format(len(menu)))
    for element in menu:
        print(menu.index(element) + 1, " - ", element)
    return "\nyour choice : "

def categories_display(categories):
    print(categories)
    print("\nPlease enter a number between 1 and {} : \n".format(len(categories)))
    for category in categories:
        print(categories.index(category) + 1, " - ", category)
    return "\nyour choice : "

def products_display(products):
    print(products)
    print("\nPlease enter a number between 1 and {} : \n".format(len(products)))
    for product in products:
        print(products.index(product) + 1, " - ", product[0], " ", product[1], " ", product[2])
    return "\nyour choice : "

def substitute_display(substitute):
    print("\nPlease find below a suitable substitute : \n")
    for information in substitute.keys():
        print("Substitute {} : ".format(information), substitute[information])
    return "\nwould you like to save this substitute ? [y/n] : "

def save_display(product, substitute):
    print("\nYour initial product : \n")
    for information in product.keys():
        print("Product {} : ".format(information), product[information])
    
    print("\nYour properly saved substitute : \n")
    for information in substitute.keys():
        print("Product {} : ".format(information), substitute[information])

def next_display():
    return "\nTry another research ? [y/n] : "