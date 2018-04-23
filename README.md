# MyRepo
Here u can find my Projects that i developed.

#MyFlaskApp Project

This project contains Flask microframework based web app with integration to Celery through Redis and Database connection through SQLAlchemy

Database is Postgres.

So this app enables user to register login and review materials on the app.User can contribute and when user adds anything it will sent as an email through Celery to my mailbox so that i can approve it.

Once the user add a Course URL it will be sent as a mail with the course details to the approver uwho can then add if applicable to the DB.

Shout out to the youtubers that helped me along this development especially Corey Schafer, traversy Media and so many intelligent guys out there and books that i went through to start this app project.

#ng5bs4fb project

This is a Angular 5 with bootstrap 4 and a noSQl database based app(here i have made use of Google's Firebase Db)

This app provides user to basically register,Login and browse through the various Study material courses regarding various technologies and Users can add thier own contributions which will be approved by Admin(me :))

Registrations are provided through Facebook, Google(gmail) and email verification after which the user can login(if authenticated) and view the material inside the app.

I will come up with new ways of making this app user friendly like voice activated buttons like speech recognition ability and so on.


#Plagiarism defender and Web scraping App

In myFlask.py , you can find my Anti plagiarism app which you can use to fing the probablility of plagiarism by typing in the text you want to check if it is plagiarised.

I have used the nltk kit to search through the net for the text and if found will tell you the probability.
(Note: I have used the source code used by Another user and modified on top on that)

Web scraping is done with the Beautiful Soup module.You can type in the url from which you guys want to scrape and the app does the scraping for you .

