CREATE DATABASE login;
USE login;

CREATE TABLE accounts (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    mobile_number VARCHAR(20) NOT NULL,
    confirm_password VARCHAR(20) NOT NULL
);
desc accounts;
SELECT * FROM accounts;
drop table accounts;




