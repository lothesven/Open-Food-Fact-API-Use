# **Open-Food-Fact-API-Use**

## *Introduction*

"Open Classroom" Project n°5 for Python Application Developer formation.
The goal of the project is to request datas from an API and use them to create a database as ressource for a simple application.

Please find Open Classroom website [here](https://openclassrooms.com/)
Please find Open Food Facts API documentation [here](http://en.wiki.openfoodfacts.org/Project:API)

## *Structure*

This application is built using MVC and SOLID principles.
Modules are separated as specified below:

* Model :
  * Gets datas from Open Food Facts API
  * Cleans datas collected
  * Sends data to local database

* View :
  * Displays user Interface asking for choices between lists of:
    * categories
    * products
  * Allows user to save program response (or not), continue with an other search or quit

* Controler :
  * Verifies User inputs and saves
  * Handles Model's interactions with local database
  * Builds Tables in local database

## *Requirements*

To use the application properly, you need to have mysql and python installed on your PC.
You also need to have the module "requests" for python.

Please find all informations following the links below:

* [Mysql](https://dev.mysql.com/downloads/mysql/#downloads)
* [Python](https://www.python.org/downloads/)
* [Requests](http://fr.python-requests.org/en/latest/user/install.html#install)

## *Instructions*

1. Launch mysql
2. Create a Database and name it "Ratatouille"
3. Creat a User with name = "Pur" and login = "Beurre"
4. Grant all accesses to "Pur" on Database "Ratatouille"
5. Launch python or your prefered IDE
6. Launch "Yummy_change.py" and follow instructions displayed