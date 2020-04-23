# Class InitialDisplay
initial_display = ("\nPlease enter a number between 1 and 5 related to following choices : \n"
        "\n"
        "1 - Install \n"
        "2 - Uninstall \n"
        "3 - Log In \n"
        "4 - Register \n"
        "5 - Exit program \n"
        "\n"
        "your choice : ")

# Class CategoriesDisplay
def categories_display(categories):
    print(categories)
    print("\nPlease enter a number between 1 and {} : \n".format(len(categories)))
    for category in categories:
        print(categories.index(category) + 1, " - ", category, "\n")
    return "your choice : "

# Class ProductsDisplay
def products_display(products):
    print(products)
    print("\nPlease enter a number between 1 and {} : \n".format(len(products)))
    for product in products:
        print(products.index(product) + 1, " - ", product[0], " ", product[1], "\n")
    return "your choice : "

# Class SubstituteDisplay

# Class RegistrationDisplay

# Class HistoryDisplay