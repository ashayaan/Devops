drop database IF EXISTS devops;
create database devops;
use devops;
CREATE TABLE users(ID int NOT NULL AUTO_INCREMENT,Name varchar(255) NOT NULL, username varchar(255),password varchar(300),email varchar(45),number varchar(100),PRIMARY KEY (ID) );
alter table users add UNIQUE(username);
create table books(user_id int,ISBN varchar(100),name varchar(100),author varchar(100),description varchar(100), PRIMARY KEY(user_id,ISBN));
alter table books add time_added DATE;
alter table books add type varchar(20);
CREATE table requests(user_id int, requests varchar(1000));
alter table requests add FOREIGN KEY (user_id) REFERENCES users(ID);
alter table requests add time_added DATE;
alter table books add FOREIGN KEY (user_id) REFERENCES users(ID);

