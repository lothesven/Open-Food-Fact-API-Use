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
def substitute_display(substitute):
    print("\nPlease find below a suitable substitute : \n")
    for information in substitute.keys():
        print("Substitute {} : ".format(information), substitute[information])
    return "\nwould you like to save this substitute ? [y/n] : "

# Class SaveDisplay
def save_display(product, substitute):
    print("\nYour initial product : \n")
    for information in product.keys():
        print("Product {} : ".format(information), product[information])
    
    print("\nYour properly saved substitute : \n")
    for information in substitute.keys():
        print("Product {} : ".format(information), substitute[information])

# Class NextDisplay
def next_display():
    return "\nTry another research ? [y/n] : "