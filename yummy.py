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
                print("Invalid input. Must be a positive integer")
                choice = 0

            if choice == 1:
                if ct.UserRequestHandler.install():
                    print("Installation completed")
                else:
                    print("Installation error")
                choice = 0

            elif choice == 2:
                if ct.UserRequestHandler.uninstall():
                    print("Uninstall process completed")
                else:
                    print("Could not uninstall")
                choice = 0

            elif choice == 3:
                user = input("Enter user name : ")
                login = input("Enter log in password : ")

                print("Try to log in with user : '{}' and password : '{}'.".format(user, login))
                try:
                    logged_in = ct.UserRequestHandler.log_in(user, login)
                except:
                    print("Encountered an error while trying to log in.")
                    user = str()
                    login = str()

            elif choice == 4:
                user = input("Enter user name : ")
                login = input("Enter log in password : ")

                print("Try to create new user : '{}' with password : '{}'.".format(user, login))
                if ct.UserRequestHandler.register(user, login):
                    print("Registration went well")

                user = str()
                login = str()
                choice = 0

            elif choice == 5:
                running = False
                print("Good bye :) ")
                break

            else:
                print("Please type an integer related to available choices.")
                choice = 0

        while logged_in:
            # Secondary user choice waiting loop
            # Contains the process for choosing which product to substitute
            
            ct.UserRequestHandler.call_categories()

            while not chosen_category:
                # Tertiary user choice waiting loop
                # Ensures a valid category have been selected by user

                valid_choices = len(ct.ProgramOutput.categories)
                print("list of categories : ")

                try:
                    choice = int(input(ct.ProgramOutput.categories_display()))
                except ValueError:
                    print("Invalid input. Must be a positive integer")
                    choice = 0
                
                if 0 < choice <= valid_choices:
                    ct.UserRequestHandler.call_products(ct.ProgramOutput.categories[choice - 1])
                    chosen_category = True

                else:
                    print("Please type an integer related to available choices.")
                    choice = 0

            while not chosen_product:
                # Tertiary user choice waiting loop
                # Ensures a valid product have been selected by user

                valid_choices = len(ct.ProgramOutput.products)
                print("list of products : ")

                try:
                    choice = int(input(ct.ProgramOutput.products_display()))
                except ValueError:
                    print("Invalid input. Must be a positive integer")
                    choice = 0
                
                if 0 < choice <= valid_choices:
                    chosen_product = ct.ProgramOutput.products[choice - 1][2]
                    print(chosen_product)
                    ct.UserRequestHandler.call_substitute(chosen_product)

                else:
                    print("Please type an integer related to available choices.")
                    choice = 0
                    
            
            choice = input(ct.ProgramOutput.substitute_display())
            # diplays found substitute and asks if user wants to save it

            while choice != "y" and choice != "n":
                # Loop to handle incorrect user input

                print("\nYou must choose between 'Yes' by pressing 'y' or 'No' by pressing 'n'.\n")
                choice = input(ct.ProgramOutput.substitute_display())

            if choice == "y":
                substitute_code = ct.ProgramOutput.substitute["code"]
                ct.UserRequestHandler.save_substitute(user, login, chosen_product, substitute_code)
                ct.ProgramOutput.save_display()

            choice = input(ct.ProgramOutput.next_display())
            # propose to try another search

            while choice != "y" and choice != "n":
                # Loop to handle incorrect user input

                print("\nYou must choose between 'Yes' by pressing 'y' or 'No' by pressing 'n'.\n")
                choice = input(ct.ProgramOutput.next_display())

            if choice != "y":
                logged_in = False # Enables to get back to the begining of main loop
            
            chosen_category = False # Get boolean to initial setting for new substitute research
            chosen_product = False # Get boolean to initial setting for new substitute research

    
main()