# MyRepo
Flask Application with Course Info app and an anti -Plagiarism App and Memory Report Generating App


# All the python apps here make use of the ever powerful Flask framework and pipenv commands are used to create the virtaul env and the pipfile and pipfile.lock.

Enjoy..!

# Memory Report App 

This App lets you handle big chunks of file in Excel or Csv format with huge memory load in terms of hundreds of GBs and output the final memory load after conversion. This app will soon have visualisation in addition to the report which helps user to see the data they wanted.

This app makes advantage of Pandas library in the way how Pandas Dataframe handles data.Using this library when a file is uploaded all the heavy memory loaders are converted to their less memory consuming counterparts(int64 to int8, float64 to float32 and unique string to its integer "categories".

Visualisation will be done by the matplotlib library

# Defenders App

This is a Anti-Plagiarism app which make use of an nltk library called nltk.tokenize.punkt lib to search through the web for certain matches and give the corresponding probability of plagiarism.You can find the app in the URl below

http://athulraj.pythonanywhere.com/


# Angular App with BS4

This is a Angular-typescript based app with bootstrap 4 powered along with a NoSQL database (Firebase).This app displays a User interface where the user can register /Login through social media platforms and go through the content present over the website.

# Software Courses App

This flask app lets the user view the content(Software courses) after he/she logins through Social media platforms which gets registered in the database(Postegres).If the user intends to add content into the website they can add the url and description to the wesite and through Asynchronous task scheduler Celery(with redis broker) o send a mail to the approver as a pdf listing the details.Once it is approved the content will be reflected on the website

If you like these , please leave a Star :)

