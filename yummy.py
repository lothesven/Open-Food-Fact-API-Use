# -*- coding: utf-8 -*

"""
Main module of the application

- Calls controler for initial display
- Waits for user choices
- For each user choice, calls the controler accordingly
- Displays program responses fetched by controler
"""

import modules.controler as ct

def main():

    choice = 0

    user = str()
    login = str()

    running = True
    logged_in = False
    chosen_category = False
    chosen_product = False

    while running:
        # Main user choice waiting loop

        while not logged_in:
            # Secondary user choice waiting loop
            # Main menu display

            try:
                choice = int(input(ct.ProgramOutput.initial_display()))
            except ValueError:
                print("Choix invalide. Vous devez entrer un nombre entier positif, sans espaces.")
                choice = 0

            if choice == 1:
                if ct.UserRequestHandler.install():
                    print("\nInstallation complète")
                else:
                    print("\nErreur durant l'installation")
                choice = 0

            elif choice == 2:
                if ct.UserRequestHandler.uninstall():
                    print("\nDésinstallation terminée")
                else:
                    print("\nLa désinstallation n'a pu avoir lieu")
                choice = 0

            elif choice == 3:
                user = input("Entrez un nom d'utilisateur : ")
                login = input("Entrez un mot de passe : ")

                print("Tentative de connexion...")

                logged_in = ct.UserRequestHandler.log_in(user, login)

                if logged_in:
                    print("Connexion réussie. \n\nBienvenue {} !".format(user))
                    
                else:
                    print("Une erreur est survenue. La connexion a échoué.")
                    user = str()
                    login = str()

            elif choice == 4:
                user = input("Entrez un nom d'utilisateur : ")
                login = input("Entrez un mot de passe : ")

                print("Création de l'utilisateur ...")

                if ct.UserRequestHandler.register(user, login):
                    print("Création réussie. \nVous pouvez à présent vous connecter.")
                else:
                    print("Une erreur est survenue. L'utilisateur {} n'a pas pu être (re)créé".format(user))

                user = str()
                login = str()
                choice = 0

            elif choice == 5:
                running = False
                print("A bientôt pour allier le bon et le sain.")
                break

            else:
                print("Veuillez entrer un nombre entier parmi les choix disponibles.")
                choice = 0

        while logged_in:
            # Secondary user choice waiting loop
            # Contains the process for choosing which product to substitute

            try:
                choice = int(input(ct.ProgramOutput.logged_display()))
            except ValueError:
                print("Choix invalide. Vous devez entrer un nombre entier positif, sans espaces.")
                choice = 0
            
            if choice == 1:
            
                ct.UserRequestHandler.call_categories()

                while not chosen_category:
                    # Tertiary user choice waiting loop
                    # Ensures a valid category have been selected by user

                    valid_choices = len(ct.ProgramOutput.categories)

                    try:
                        choice = int(input(ct.ProgramOutput.categories_display()))
                    except ValueError:
                        print("Choix invalide. Vous devez entrer un nombre entier positif, sans espaces.")
                        choice = 0
                    
                    if 0 < choice <= valid_choices:
                        ct.UserRequestHandler.call_products(ct.ProgramOutput.categories[choice - 1])
                        chosen_category = ct.ProgramOutput.categories[choice - 1]
                        print("Vous avez choisi la catégorie suivante :", chosen_category)

                    else:
                        print("Veuillez entrer un nombre entier parmi les choix disponibles.")
                        choice = 0

                while not chosen_product:
                    # Tertiary user choice waiting loop
                    # Ensures a valid product have been selected by user

                    valid_choices = len(ct.ProgramOutput.products)

                    try:
                        choice = int(input(ct.ProgramOutput.products_display()))
                    except ValueError:
                        print("Choix invalide. Vous devez entrer un nombre entier positif, sans espaces.")
                        choice = 0
                    
                    if 0 < choice <= valid_choices:
                        chosen_product = ct.ProgramOutput.products[choice - 1][2]
                        print("Vous avez choisi le produit suivant :", chosen_product)
                        ct.UserRequestHandler.call_substitute(chosen_product)

                    else:
                        print("Veuillez entrer un nombre entier parmi les choix disponibles.")
                        choice = 0
                        
                
                choice = input(ct.ProgramOutput.substitute_display())
                # diplays found substitute and asks if user wants to save it

                while choice != "o" and choice != "n":
                    # Loop to handle incorrect user input

                    print("\nVous devez chosir entre 'Oui' ou 'Non' en entrant 'o' ou 'n'.\n")
                    choice = input(ct.ProgramOutput.substitute_display())

                if choice == "o":
                    substitute_code = ct.ProgramOutput.substitute["code"]
                    ct.UserRequestHandler.save_substitute(user, login, chosen_product, substitute_code)
                    ct.ProgramOutput.save_display()

                    print("\n************************************\n")

                chosen_category = False # Get boolean to initial setting for new substitute research
                chosen_product = False # Get boolean to initial setting for new substitute research
            
            elif choice == 2:
                ct.UserRequestHandler.past_substitutes(user, login)

                valid_choices = len(ct.ProgramOutput.past_substitutes) + 1

                try:
                    choice = int(input(ct.ProgramOutput.favorites_display()))
                except ValueError:
                    print("Choix invalide. Vous devez entrer un nombre entier positif, sans espaces.")
                    choice = 0
                
                if 0 < choice <= valid_choices - 1:
                    product = ct.ProgramOutput.past_substitutes[choice][0]
                    substitute = ct.ProgramOutput.past_substitutes[choice][1]
                    ct.UserRequestHandler.load_substitution(product, substitute)
                    ct.ProgramOutput.save_display()

                    print("\n************************************\n")

                elif choice == valid_choices:
                    pass

                else:
                    print("Veuillez entrer un nombre entier parmi les choix disponibles.")
                    choice = 0

            elif choice == 3:
                logged_in = False # Enables to get back to the begining of main loop
            
            else:
                print("Veuillez entrer un nombre entier parmi les choix disponibles.")
                choice = 0

    
main()