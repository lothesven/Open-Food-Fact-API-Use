# -*- coding: utf-8 -*

"""
This module receives instructions related to user inputs from "Yummy.py"
It works as controler of an MVC patern

The module consists of two classes:
- ProgramOutput interacts with View
- UserRequestHandler interacts with Model
"""

import model
import view

class ProgramOutput():
    """
    This not to be instanciated class contains:
    - procedures to interact with module View
    - some class attributes to store information
    """

    categories = list()
    products = list()

    product = dict()
    substitute = dict()

    @classmethod
    def initial_display(cls):
        return view.initial_display()

    @classmethod
    def categories_display(cls):
        # cls.categories is a list
        return view.categories_display(cls.categories)

    @classmethod
    def products_display(cls):
        # cls.products is a list
        return view.products_display(cls.products)

    @classmethod
    def substitute_display(cls):
        # cls.substitute is a dictionary
        return view.substitute_display(cls.substitute)

    @classmethod
    def save_display(cls):
        # cls.product is a dictionary / cls.substitute is a dictionary
        return view.save_display(cls.product, cls.substitute)

    @classmethod
    def next_display(cls):
        return view.next_display()

class UserRequestHandler():
    """
    This not to be instanciated class contains:
    - procedures to interact with module Model
    - boolean attribute that verifies if database is installed
    """

    installed = model.is_installed()

    @classmethod
    def install(cls):
        if not cls.installed:
            try:
                model.install()
            except:
                print("Error while installing")
            else:
                cls.installed = True
                return True
        
        else:
            print("Already installed")
            return False

    @classmethod
    def uninstall(cls):
        if cls.installed:
            try:
                model.uninstall()
            except:
                print("Error while uninstalling")
            else:
                cls.installed = False
                return True
        
        else:
            print("Already uninstalled")
            return False

    @classmethod
    def log_in(cls, user, login):
        if cls.installed:
            if user and login:
                if model.manage_user(user, login, "log"):
                    return True
                else:
                    return False
            else:
                print("Empty user and/or login. Please retry and input something")
                return False
        else:
            print("You need to install, then register before trying to log in")
            return False

    @classmethod
    def register(cls, user, login):
        if cls.installed:
            if user and login:
                if model.manage_user(user, login, "create"):
                    return True
                else:
                    return False
            else:
                print("Empty user and/or login. Please retry and input something")
                return False
        else:
            print("You need to install first before trying to register")
            return False

    @classmethod
    def call_categories(cls):
        if cls.installed:
            ProgramOutput.categories = model.list_categories()

    @classmethod
    def call_products(cls, category):
        if cls.installed:
            ProgramOutput.products = model.list_products(category)

    @classmethod
    def call_substitute(cls, product_code):
        if cls.installed:
            print("Getting substitute for {} ...".format(product_code))
            ProgramOutput.substitute = model.get_substitute(product_code)
    
    @classmethod
    def save_substitute(cls, user, login, product_code, substitute_code):
        if cls.installed:
            if model.save_search(user, login, product_code, substitute_code):
                ProgramOutput.product = model.get_informations(product_code)
            else:
                print("Couldn't save substitute")
