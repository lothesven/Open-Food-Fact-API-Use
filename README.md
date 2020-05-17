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

* Config : Constants used in other modules for easy access

## *Requirements*

To use the application properly, you need to have python and mysql installed on your PC.
You also need to have the modules "requests" and "mysql.connector" for python.

Please find all informations following the links below:

* [Python](https://www.python.org/downloads/)
* [Mysql](https://dev.mysql.com/downloads/mysql/#downloads)
* [Requests](http://fr.python-requests.org/en/latest/user/install.html#install)
* [Mysql.connector](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)

## *Instructions*

1. Launch the command shell of your operating system
2. Launch mysql
> mysql -h localhost -u root -p
3. Create a Database and name it "ratatouille"
> CREATE DATABASE ratatouille CHARACTER SET 'utf8';
4. Create a User with name = "Pur" and login = "Beurre"
> CREATE USER 'Pur'@'localhost' IDENTIFIED BY 'Beurre';
5. Grant all accesses to "Pur" on Database "Ratatouille"
> GRANT ALL PRIVILEGES ON Ratatouille.* TO 'Pur'@'localhost' WITH GRANT OPTION;
6. Launch "yummy.py" and follow instructions displayed
> python yummy.py

## *Assistance*

If above instructions doesn't get you out of troubles, please contact us:

contact@purbeurre.fr