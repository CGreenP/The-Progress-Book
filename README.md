# The-Progress-Book
A GUI Student Management System with Python &amp; SQLite 3.

## Introduction:
In an educational system or to be more specific, in any institutions like school or colleges, student’s data is maintained. But these data are used just for record purposes only. If one can use these efficiently, then an institution can get much more out of it. Every student’s performance can be tracked individually and respective teachers/faculties can get an overview about how well their students are performing and who needs special attention. To achieve, these objectives, we prepared our project “The Progress Book” to meet these requirements. The intended audience of this project is any institution/school.

This project makes managing students’ effortlessly, we have also introduced simple security features to further protect the admin accounts and their data. Data Insertion, deletion, data updating all these features are implemented in GUI, so the user can do all these operation in user friendly, hassle-free way.

We use database and database technology are having a major impact on the growing use of computers. The implementation of the system was done using Python, Tkinter, Python Imaging Library, bcrypt and SQLite technologies, allowing system to be run in Windows OS.
Our project “The Progress Book” is specially designed to work with students’ data. We have designed 6 sections – LOGIN, VIEW, DATA ENTRY, MARKS ENTRY, RESULT, ADMIN PORTAL.

* In “Log In”, a username and password are required. There are two types of user, mainly one is “USER” and another is “ADMIN”. Certain types of actions like, deletion/addition of other users is restricted and also, ADMIN accounts can’t be deleted. Users/Admins can only access this program using a valid “username” and “password. In case of forget password / password recovery, this action must be done through System Administrator.
* In “View” section, all the enlisted students of the selected class and section/stream can be viewed and will allow data update for enlisted students.
* In “Data Entry” section, user will have to select the respective class first, and then user can add the details about student by filling some basic information like – Name, Class, Section, Roll No., Date of Birth, etc.
* In “Marks Entry” section, user should be able to enter marks details of respective students. Now, one thing to be noted that, to prevent ambiguation of higher secondary level subjects, we have omitted the normal section names and instead we are renaming these sections by their respective streams, i.e., “SCIENCE”, “ARTS”, “COMMERCE”.
* In “Results” section, important information like list of students in that class and student marks will be shown upon selecting the proper class and section.
* “Admin Portal” is only visible to admins, those who manage the database. Addition and deletion of users are available through this portal. As a security measures, some admin accounts are can’t be deleted. Even though while deleting, program may report that “This user is deleted” but it actually never deletes. These admin can safely re login again.

## Literature Review:
Our project is aimed towards the institution personnel and they are the intended recipients. As discussed earlier, the main objective is to maintain students’ data and storing it in a certain manner so that this can be used later to further improve the performance of the students itself. It is a cross platform app with simple user interface. This is an alpha version and it has some limitations too, which we have discussed in details later in the documentation.

## Materials & Prerequisite:
* Python3 - As a standalone app, should be installed in user’s PC while using. ( This is the main programming language used to prepare the app. )
* Tkinter - Python3 (Built-in) ( Provides main GUI of this app. )
* Bcrypt - Python3 (installable through PIP installer) ( Important for security functions to work. )
* Pillow - Python3 (installable through PIP installer) ( For importing certain images )
* Sqlite3 - Python3 (Built-in) ( Provides maintenance and storage functions for database )

Default Username - admin

Deafault Password - admin

## Architecture of the Application
Our project “The Progress Book” is specially designed to work with students’ data. We have designed 6 sections – LOGIN, VIEW, DATA ENTRY, MARKS ENTRY, RESULT, ADMIN PORTAL.
* In “Log In”, a username and password are required. There are two types of user, mainly one is “USER” and another is “ADMIN”. Certain types of actions like, deletion/addition of other users is restricted and also, ADMIN accounts can’t be deleted. Users/Admins can only access this program using a valid “username” and “password. In case of forget password / password recovery, this action must be done through System Administrator.
* In “View” section, all the enlisted students of the selected class and section/stream can be viewed and will allow data update for enlisted students.
* In “Data Entry” section, user will have to select the respective class first, and then user can add the details about student by filling some basic information like – Name, Class, Section, Roll No., Date of Birth, etc.
* In “Marks Entry” section, user should be able to enter marks details of respective students. Now, one thing to be noted that, to prevent ambiguation of higher secondary level subjects, we have omitted the normal section names and instead we are renaming these sections by their respective streams, i.e., “SCIENCE”, “ARTS”, “COMMERCE”.
* In “Results” section, important information like list of students in that class and student marks will be shown upon selecting the proper class and section.
* “Admin Portal” is only visible to admins, those who manage the database. Addition and deletion of users are available through this portal. As a security measures, some admin accounts are can’t be deleted. Even though while deleting, program may report that “This user is deleted” but it actually never deletes. These admin can safely re login again.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/5f67da68-15a7-46b7-838b-a8d11daa286c)
<p align="center"><i>Simple flow-chart to describe the project</i></p>

### Database table design:
A database management system (DBMS) is a collection of programs that enables you to store, modify, and extract information from a database. There are many different types of database management systems, ranging from small systems that run on personal computers to huge systems that run on mainframes.
We use database and database technology are having a major impact on the growing use of computers. The implementation of the system was done using SQLite.

#### USER table
In database, USER table is used to make admin and user for this application, so that the said valid user can enter to this application. To validate, we take user id as primary key, also take user type, password, entry date as a not null entity.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/61abe078-40b1-41ef-98cd-587b30d45b45)

#### JUNIOR, MIDDLE & SENIOR table
To enter student’s marks into the database, we make three tables such as JUNIOR, MIDDLE and SENIOR. Those 3 tables can fetch any sort of exam marks from class 1 to class 12.

##### JUNIOR table
In JUNIOR table, we can fetch unit test marks, half yearly marks and final exam marks for the student from class 1 to class 4. In this database, we also categorized classes into sections such as section A, section B and section C. In this table we take student roll number as primary key. Also take user name, user class and user section, date of birth, gender, guardian’s name and address as a not null integrity.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/ac6f0735-003d-4cb1-89c3-331f72437cf2)

##### MIDDLE table
In Middle table, we can fetch unit test marks, half yearly marks and final exam marks for the student from class 5 to class 10. In this database, we also categorized classes into sections such as section A, section B and section C. In this table we take student roll number as primary key. Also take user name, user class and user section, date of birth, gender, guardian’s name and address as a not null integrity.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/a9ac7727-1509-46ac-a42c-f4d0ddcd0024)

##### SENIOR table
In Senior table, we can fetch unit test marks, half yearly marks and final exam marks for the student from class 11 and class 10. In this database, we also categorized classes into various streams such as Arts, Commerce and Science. The extra column we added to this table is optional subject. Here, any student can choose their favourite optional subject into their stream such as in arts anyone can choose their optional subject between Education and Political Science. In this table we take student roll number as primary key. Also take user name, user class and user stream, optional Subject, date of birth, gender, guardian’s name and address as a not null integrity.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/77530bda-59da-4adf-9fef-debc3423b128)

## METHODOLOGY
We have designed 6 sections – LOGIN, VIEW, DATA ENTRY, MARKS ENTRY, RESULT, ADMIN PORTAL.

### Log In
In “Log In”, a username and password are required. There are two types of user, mainly one is “USER” and another is “ADMIN”. Certain types of actions like, deletion/addition of other users is restricted and also, ADMIN accounts can’t be deleted. Users/Admins can only access this program using a valid “username” and “password. In case of forget password / password recovery, this action must be done through System Administrator.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/e68a43cc-7272-4c54-affb-25ac0ad41790)
<p align="center"><i>Login Window</i></p>

While logging in, without any valid credentials input, i.e., blank input, a message will be thrown, “All fields are required”.

If one of the fields are incorrect, either “Username” or “Password” then an error message will be shown “Incorrect Username/Password Entered”.

If you click “Forgot Password”, then a message will appear “Please contact system admin!”. Please note, all fields are CASE SENSITIVE.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/c9790ae9-5983-4a39-89ab-4c1352052ca9)
<p align="center"><i>After Logging In successfully</i></p>

### Admin Portal
“Admin Portal” is only visible to admins, those who manage the database. Addition and deletion of users are available through this portal. As a security measures, some admin accounts are can’t be deleted. Even though while deleting, program may report that “This user is deleted” but it actually never deletes. These admin can safely re-login again.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/f8a011b8-4d86-43b7-a024-414d851568e1)
<p align="center"><i>Admin Portal Window</i></p>

As we have mentioned earlier, an admin account is required to add/remove users further, so program while running at first time in a new system, it checks whether a valid admin user is available in the system, if not available then it automatically creates one with the credential which is hardcoded in the program itself. One cannot remove this SUPERADMIN without editing the source code. It is designed to discourage any mistake which can make this app inoperable.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/b15d30ee-0ee0-4c3a-9bf7-052ed3f87ba1)
<p align="center"><i>Create ( ) function checking and creating Superadmin account when required.</i></p>

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/ed79afee-3232-4da2-9749-c4bb3668db7b)
<p align="center"><i>Adding User through Admin Portal</i></p>

### Data Entry
In “Data Entry” section, user will have to select the respective class first, and then user can add the details about student by filling some basic information like – Name, Class, Section, Roll No., Date of Birth, etc.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/cb5b13b6-0bb6-4e94-ac48-d5b1bf8a53ff)
<p align="center"><i>Data Entry Window</i></p>

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/4c4320c2-1d63-4a80-b1d1-8ac15cd6b8bc)
<p align="center"><i>Adding Student details in Data Entry</i></p>

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/f84204f0-3353-4c8a-967e-b033dd58bfdc)
<p align="center"><i>Confirmation Box before Adding Student Details in Data Entry</i></p>

All fields are needed to be filled up before proceeding, an error message “All fields are required” will appear if one proceeds without filling. Also, “ROLL NUMBER” can take only INTEGER VALUES, if other type of value is entered, then “Please check Roll Number! Only Integer Values are accepted!” will be shown. And as “ROLL NUMBER” is used as primary key in our database, the application doesn’t allow to Add students to have same “ROLL NUMBER” in Data Entry.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/03a3de4a-de3c-49b1-8f4e-837fdd6e1b27)
<p align="center"><i>Restricting User to Add Students with Existing Roll No.</i></p>

### View
In “View” section, all the enlisted students of the selected class and section/stream can be viewed and will allow data update for enlisted students.
One can’t update any student’s section, roll, class further once created. This is done to prevent database anomalies. To do these operations, one should delete the student first, then re-create.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/f97a8033-9b6b-44cd-85f4-9f06dcbfd8a9)
<p align="center"><i>View Window</i></p>

### Marks Entry
In “Marks Entry” section, user should be able to enter marks details of respective students. Now, one thing to be noted that, to prevent ambiguation of higher secondary level subjects, we have omitted the normal section names and instead we are renaming these sections by their respective streams, i.e., “SCIENCE”, “ARTS”, “COMMERCE”.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/34f2b7ab-33a0-409a-af6e-ffdc13c77107)
<p align="center"><i>Marks Entry Window</i></p>

### Result
In “Results” section, important information like list of students in that class and student marks will be shown upon selecting the proper class and section.

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/e4750ab8-35c2-4032-872c-f28c14ec8a85)
<p align="center"><i>Result Window</i></p>

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/263f1e18-4628-470e-b060-20820adefcb0)
<p align="center"><i>Result Window after selecting class and section/stream</i></p>

![image](https://github.com/CGreenP/The-Progress-Book/assets/56307530/9c827ffd-9de9-46bb-a2ef-957cd502bfb8)
<p align="center"><i>Result of a student shown in a window</i></p>

## Conclusion
The progress book has been specially created both for helping out teachers as well as students. For teachers, this would help to keep track of the academic quality as well as improvement level of students. This allows the teacher to manage student’s results academic wise, as well as class wise and stream wise. Students too can check their academic performance through this progress book.

A progress book at hand is beneficial, as it helps improvement of the general performance of students, it can be accessed easily, anywhere anytime – a record of everything can be kept due to its easy accessibility. It helps teachers keep track of students and as well as manage their activities. It even helps reducing the workload of teachers. It even improves student-teacher collaboration by increasing the interaction between teachers and students.

## Limitation
* A few operations are still static.
* The process of automation could not be performed due to lack of resources, manpower as well as timeframe. For example – The feature of Forget Password can only be controlled and handled by the Admin.
* Moreover, the authentication process could still be improved, it’s still in the basic level currently (due to unavailability of API).

## Future scopes
*  The authentication process could still be improved, which is currently in basic level will be worked upon.
* There will be upgradation of graphical interface in the future.
* More of analytics will be included.
* This shall be connected with cloud database.
* This shall be managed remotely.
