# **Open-Food-Fact-API-Use**

## *Introduction*

"Open Classroom" Project n°5 for Python Application Developer formation.
The goal of the project is to request datas from an API and use them to create a database as ressource for a simple application.

User of the application can choose a food category, then a product of that category and expect the application to provide a more healthy substitute if any exists in the database.
Sustitute comes along with usefull informations (if they exist) such as:
* Description
* Stores where it can be purchased
* Url to product's page on Open Food Facts

The application is expected to record previous searches as well for rapid further access

Please find Open Classroom website [here](https://openclassrooms.com/)
Please find Open Food Facts API documentation [here](http://en.wiki.openfoodfacts.org/Project:API)

## *Structure*

This application is built using MVC and SOLID principles.
Modules are separated as specified below:

* Yummy : Main program waiting for user requests and returning application responses

* Controler :
  * Verifies User inputs
  * Handles Model's interactions with local database
  * Hands Model's informations to View

* Model :
  * Gets datas from Open Food Facts API
  * Cleans datas collected
  * Builds Tables in local database
  * Sends data to local database
  * Retrieves datas from local database
  * Finds substitute

* View :
  * Displays user Interface 
  * Displays application responses

* Parameters : Constants used in other modules for easy access

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
6. Launch "yummy.py" and follow instructions displayed