# -*- coding: utf-8 -*

"""
This module receives data from "controler.py"
It works as View of an MVC patern
"""


def initial_display():

    menu = ["Installer", "Désinstaller", "Se connecter", "Créer utilisateur", "Quitter le programme"]
    print("")

    for element in menu:
        print(menu.index(element) + 1, " - ", element)
    
    print("\nVeuillez entrer un chiffre entre 1 et {}".format(len(menu)))

    return "\nVotre choix : "

def logged_display():

    menu = ["Remplacer un aliment", "Mes aliments substitués", "Retour au menu principal"]
    print("")
    
    for element in menu:
        print(menu.index(element) + 1, " - ", element)

    print("\nVeuillez entrer un chiffre entre 1 et {}".format(len(menu)))

    return "\nVotre choix : "

def categories_display(categories):

    print("Liste des catégories disponibles : \n")

    for category in categories:
        print(categories.index(category) + 1, " - ", category)

    print("\nVeuillez entrer un chiffre entre 1 et {}".format(len(categories)))

    return "\nVotre choix : "

def products_display(products):

    print("Liste des produits dans la catégorie : \n")

    for product in products:
        print(products.index(product) + 1, " - ", product[0], " ", product[1], " ", product[2])
    
    print("\nVeuillez entrer un chiffre entre 1 et {}".format(len(products)))

    return "\nVotre choix : "

def substitute_display(substitute):

    print("\nVeuillez trouver ci dessous un substitut adapté : \n")

    for information in substitute.keys():
        print("Substitut {} : ".format(information), substitute[information])

    return "\nVoulez vous enregistrer ce substitut ? [o/n] : "

def save_display(product, substitute):

    print("\nVotre produit initial : \n")
    for information in product.keys():
        print(information, "-", product[information])
    
    print("\nVotre produit substitué et enregistré : \n")
    for information in substitute.keys():
        print(information, "-", substitute[information])
    
    return input("\nAppuyez sur entrée pour continuer")

def favorites_display(substitutions):

    print("\nVos substitutions enregistrées : \n")
    for choice in substitutions.keys():
        p_code = substitutions[choice][0]["code"]
        p_name = substitutions[choice][0]["name"]
        s_code = substitutions[choice][1]["code"]
        s_name = substitutions[choice][1]["name"]
        print(choice, " - ", "(", p_code, ")", " ", p_name, " = ", "(", s_code, ")", " ", s_name)
    
    last_choice = len(substitutions) + 1
    print(last_choice, " - ", "Retour au menu précédent")

    return "\nEntrez le numéro d'une des substitutions pour avoir plus d'informations. \nVotre choix : "