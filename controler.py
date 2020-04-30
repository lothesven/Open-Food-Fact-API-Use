# Get initial display using View
# Launch requests to OFF in Model
import model
import view

class ProgramOutput():

    categories = list()
    products = list()

    product = dict()
    substitute = dict()

    @classmethod
    def initial_display(cls):
        return view.initial_display()

    @classmethod
    def categories_display(cls):
        # categories is a list
        return view.categories_display(cls.categories)

    @classmethod
    def products_display(cls):
        # products is a list
        return view.products_display(cls.products)

    @classmethod
    def substitute_display(cls):
        # substitute is a dictionary
        return view.substitute_display(cls.substitute)

    @classmethod
    def save_display(cls):
        # substitute is a dictionary
        return view.save_display(cls.product, cls.substitute)

    @classmethod
    def next_display(cls):
        # substitute is a dictionary
        return view.next_display()

class UserRequestHandler():

    installed = model.is_installed()
    uninstalled = not installed

    @classmethod
    def install(cls):
        print("installed : ", cls.installed, " uninstalled : ", cls.uninstalled)
        if not cls.installed:
            try:
                model.install()
            except:
                print("Error while installing")
            else:
                cls.installed = True
                cls.uninstalled = False
                return True
        
        else:
            print("Already installed")
            return False

    @classmethod
    def uninstall(cls):
        print("installed : ", cls.installed, " uninstalled : ", cls.uninstalled)
        if not cls.uninstalled:
            try:
                model.uninstall()
            except:
                print("Error while uninstalling")
            else:
                cls.uninstalled = True
                cls.installed = False
                return True
        
        else:
            print("Already uninstalled")
            return False

    @classmethod
    def log_in(cls, user, login):
        print("installed : ", cls.installed, " uninstalled : ", cls.uninstalled)
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
        print("installed : ", cls.installed, " uninstalled : ", cls.uninstalled)
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
        # Get categories using Model
        # Get proper categories display using View
        if cls.installed:
            ProgramOutput.categories = model.list_categories()

    @classmethod
    def call_products(cls, category):
        # Get products provided a category using Model
        # Get proper products display using View
        if cls.installed:
            ProgramOutput.products = model.list_products(category)

    @classmethod
    def call_substitute(cls, product_code):
        # Get substitute provided a product using Model
        # Get proper substitute display using View
        if cls.installed:
            print("Getting substitute for {} ...".format(product_code))
            ProgramOutput.substitute = model.get_substitute(product_code)
    
    @classmethod
    def save_substitute(cls, user, login, product_code, substitute_code):
        # Register product and substitute using Model
        # Get proper registration display using View
        if cls.installed:
            if model.save_search(user, login, product_code, substitute_code):
                ProgramOutput.product = model.get_informations(product_code)
            else:
                print("Couldn't save substitute")
