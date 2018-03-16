drop database IF EXISTS devops;
create database devops;
use shayaan;
CREATE TABLE users(ID int NOT NULL AUTO_INCREMENT,Name varchar(255) NOT NULL, username varchar(255),password varchar(45),email varchar(45),PRIMARY KEY (ID) );
