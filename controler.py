# Get initial display using View
# Launch requests to OFF in Model
import modelbis as md
import view

class ProgramOutput():

    categories = list()
    products = list()
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
        # categories is a list
        return view.products_display(cls.products)

class UserRequestHandler():

    installed = md.is_installed()
    uninstalled = not installed

    @classmethod
    def install(cls):
        print("installed : ", cls.installed, " uninstalled : ", cls.uninstalled)
        if not cls.installed:
            try:
                md.install()
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
                md.uninstall()
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
                if md.manage_user(user, login, "login"):
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
                if md.manage_user(user, login, "create"):
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
            ProgramOutput.categories = md.list_categories()

    @classmethod
    def call_products(cls, category):
        # Get products provided a category using Model
        # Get proper products display using View
        if cls.installed:
            ProgramOutput.products = md.list_products(category)

    @classmethod
    def call_substitute(cls, user, login, product_code):
        # Get substitute provided a product using Model
        # Get proper substitute display using View
        if cls.installed:
            ProgramOutput.substitute = md.substitute(user, login, product_code)
            

# Register product and substitute using Model
# Get proper registration display using View

# Get history using Model
# Get proper history display using View