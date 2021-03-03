# Cyber Security Base 2021 - Project 1

This project is course project (Project 1) for the online course https://cybersecuritybase.mooc.fi/.

The project *SHOULD NOT* be used for anything else than for the project course as it is insecure and against all best security practices.

## Getting started

To run the project first run

> python manage.py migrate

Create some users for the systems so you can log in

>python manage.py createsuperuser

Then to start the server run

> python manage.py runserver

## Purpose of project

The project demonstrates the following vulnerabilities:

### XXS injection for redirecting to another site

The Login screen has a security vulnerability in the Username field where by entering a correctly formatted
string the Login screen can be used as a redirect to another site.

This can be demonstrated by clicking on the **XSS injection attack (site redirect)** and clicking submit.

The Login screen can also directly be abused (without submittinh the FORM) by accessing the [this link](http://localhost:8000/login?message=%3Cimg%20src=%22https://www.freepnglogos.com/uploads/hacker-png/hacker-interpol-arrests-suspected-anonymous-hackers-motley-5.png%22%20onload=%22window.location.href=%27http://some.malicious.site.com%27;this.parentNode.removeChild(this);%22/%3E%20not%20found).

### Insecure credential management

The Login screen additionally will send the username and password as HTTP GET parameters so they will also be exposed in server logs and the browser history.

### Access control vulnerability in product filtering

You can view all products in the system simply by giving the filter parameter to the url. You can test this out via the link on the login screen.

### XSS injection for stealing cookie

Once you have successfully logged in you can test another XSS vulnerability in the "Add product:" field by injecting a script tag in the product name field. This can be simulated with the **XSS injection attack (steal cookies)** link as well.

### SQL inject attack to list users and other sensitive data of system

The "Find Product by Name" field can be used for SQL injection attacks to get any information from the system database. An example of this can been seen by clicking the **Sql injection attack (Get all users of system along with their details)** link. Once you click search you will be taken to a page that lists all users of the system.

### Using Components with Known Vulnerabilities

The system uses the insecure [PullDOM](https://docs.python.org/3/library/xml.dom.pulldom.html#module-xml.dom.pulldom) library for processing XML imports. This gives access to the following vulnerability.

### XXE vulnerability in processing XML product imports

The system provides a utility to import product defined in XML. By using a XML file the ENTITY header can be used to pull information from the system. It can be tested by uploading the /static/products.xml file.