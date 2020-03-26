# **Open-Food-Fact-API-Use**

## *Introduction*

"Open Classroom" Project n°5 for Python Application Developer formation.
The goal of the project is to request datas from an API and use them to create a database as ressource for a simple application.

Please find Open Classroom website [here](https://openclassrooms.com/)
Please find Open Food Facts API documentation [here](http://en.wiki.openfoodfacts.org/Project:API)

## *Structure*

This application is built using OOP, MVC and SOLID principles.
Modules are separated as specified below:

* Model : Classes used in the core mainly to
  * Build local database
  * Get datas from Open Food Facts API
  * Clean them
  * Fill local database with cleaned datas

* View : User Interface asking for choices
  * Between a list of categories
  * Between a list of products
  * Register program response or not, continue with an other search or quit

* Controler : To verify user inputs and response saves

## *Requirements*

To use the application properly, you need to have mysql and python installed on your PC.
You also need to have the module "requests" for python.

Please find all informations following the links below:

* [Mysql](https://dev.mysql.com/downloads/mysql/#downloads)
* [Python](https://www.python.org/downloads/)
* [Requests](http://fr.python-requests.org/en/latest/user/install.html#install)

## *Instructions*

1. Launch python or your prefered IDE
2. Launch "purbeurre.py" and follow instructions displayed