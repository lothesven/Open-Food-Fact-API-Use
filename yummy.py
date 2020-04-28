# Calls controller for initial display
# Waits for user choice

# For each user choice, calls the controler accordingly

import controler as ct

def main():

    choice = 0

    user = str()
    login = str()

    running = True
    logged_in = False
    chosen_category = False
    chosen_product = False

    while running:

        while not logged_in:

            try:
                choice = int(input(ct.ProgramOutput.initial_display()))
            except ValueError:
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
                print("Invalid input. Please follow instructions...")
                choice = 0

        while logged_in:
            
            ct.UserRequestHandler.call_categories()

            while not chosen_category:

                valid_choices = len(ct.ProgramOutput.categories)
                print("list of categories : ")

                try:
                    choice = int(input(ct.ProgramOutput.categories_display()))
                except ValueError:
                    choice = 0
                
                if 0 < choice <= valid_choices:
                    ct.UserRequestHandler.call_products(ct.ProgramOutput.categories[choice - 1])
                    chosen_category = True

            while not chosen_product:

                valid_choices = len(ct.ProgramOutput.products)
                print("list of products : ")

                try:
                    choice = int(input(ct.ProgramOutput.products_display()))
                except ValueError:
                    choice = 0
                
                if 0 < choice <= valid_choices:
                    print(ct.ProgramOutput.products[choice - 1][1])
                    ct.UserRequestHandler.call_substitute(ct.ProgramOutput.products[choice - 1][1])
                    chosen_product = True
            
            choice = input(ct.ProgramOutput.substitute_display())

            while choice != "y" and choice != "n":
                print("\nYou must choose between 'Yes' by pressing 'y' or 'No' by pressing 'n'.\n")
                choice = input(ct.ProgramOutput.substitute_display())

            if choice == "y":
                print("Register save")
            else:
                print("Choice between leave program or make another substitute search.")

            logged_in = False
            chosen_category = False
            chosen_product = False

        
    

main()