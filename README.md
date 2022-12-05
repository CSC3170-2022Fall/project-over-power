[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9503481&assignment_repo_type=AssignmentRepo)
# CSC3170 Course Project

## Project Overall Description

This is our implementation for the course project of CSC3170, 2022 Fall, CUHK(SZ). For details of the project, you can refer to [project-description.md](project-description.md). In this project, we will utilize what we learned in the lectures and tutorials in the course, and implement either one of the following major jobs:

<!-- Please fill in "x" to replace the blank space between "[]" to tick the todo item; it's ticked on the first one by default. -->

- [x] **Application with Database System(s)**
- [ ] **Implementation of a Database System**

## Team Members

Our team consists of the following members, listed in the table below (the team leader is shown in the first row, and is marked with 🚩 behind his/her name):

<!-- change the info below to be the real case -->

| Student ID | Student Name | GitHub Account (in Email) |
| ---------- | ------------ | ------------------------- |
| 123010245  | 张三 🚩      | sanzhang@gmail.com        |
| 123010345  | 李四         | sili@outlook.com          |
| 123030245  | 王五         | wuwang@foxmail.com        |
| 123020245  | 陈六         | liuchen@qq.com            |
| 123010249  | 朱九         | jiuzhu@163.com            |

## Project Specification

<!-- You should remove the terms/sentence that is not necessary considering your option/branch/difficulty choice -->

After thorough discussion, our team made the choice and the specification information is listed below:

- Our option choice is: **Option 2**
- Our branch choice is: **Branch 1**
- The difficulty level is: **Normal**

As for Option 2, our topic background specification can be found in [background-specification.md](background-specification.md).

## Project Abstract
The database system is a database management system based on the combination of user's html web page and back-end flask.This project aims at allowing registered users to record information and create content related to the canteens and foods provided by CUHKSZ. The website is a platform to find ratings and reviews of canteens and foods. 

## Background Specification
This project aims at allowing registered users to record information and create content related to the canteens and foods provided by CUHKSZ. The website is a platform to find ratings and reviews of canteens and foods. 
Below are the significant concepts and corresponding settings: 

User: The one who receives the service from the applications. The registered user can review the information on dishes provided by different canteens. The users can also add comments, have his/hers average spending recorded, and grade the quality of the dishes he or her has ordered.

Senior user: 
The administrator of a specific canteen. Information about his restaurant id should be included.

Restaurant: provide various types of dishes. Each restaurant has its ID, name, location, providing dishes, and its average price for each person (or other analyzed information), and the average rate of one restaurant. 

Rate: records storing the users' rating on the hygiene and service of the restaurants.

Dish: every restaurant provides various types of dishes. Every dish has its corresponding restaurant (providing the dish), its name, its type(how it is cooked, for example, fried or boiled), price, taste( special features that might cause unpleasant feelings for certain groups of people, for example, spicy or not）and its ordered time. 

Comments: records of comments added by the user for specific dishes. This should include the comment's actual content, the time the comment is added, the user’s ID of comment, and its corresponding dish’s restaurant ID and name.
 
And here is our ER diagram. 

The major functionalities of this platform have:
The main features of this platform include: 1. New users can create a new account as junior or regular platform users.
2. Clients can access their accounts.
3. After logging in, the user is free to check the statistics on the total number of passengers, the typical rating given by customers, and other important data that may be offered to the customer.
4. Under the directory of various regions, tastes, the initial letter of the name, and other features that are available, the user can search for the name of the dish. The user may offer feedback on the dish's flavor.
5. The senior user is permitted to introduce fresh menu items to particular canteens.


Some additional functionality that may be implemented:
1. The platform may give elderly users recommendations for the cuisine’s clients love the most.
2. The general public can get new recommendations for the kinds of new dishes they would enjoy.
