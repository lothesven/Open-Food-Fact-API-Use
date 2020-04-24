# Class InitialDisplay
def initial_display():
    menu = ["Install", "Uninstall", "Log In", "Register", "Exit program"]
    print("\nPlease enter a number between 1 and {} : \n".format(len(menu)))
    for element in menu:
        print(menu.index(element) + 1, " - ", element)
    return "\nyour choice : "

# Class CategoriesDisplay
def categories_display(categories):
    print(categories)
    print("\nPlease enter a number between 1 and {} : \n".format(len(categories)))
    for category in categories:
        print(categories.index(category) + 1, " - ", category)
    return "\nyour choice : "

# Class ProductsDisplay
def products_display(products):
    print(products)
    print("\nPlease enter a number between 1 and {} : \n".format(len(products)))
    for product in products:
        print(products.index(product) + 1, " - ", product[0], " ", product[1])
    return "\nyour choice : "

# Class SubstituteDisplay

# Class RegistrationDisplay

# Class HistoryDisplay