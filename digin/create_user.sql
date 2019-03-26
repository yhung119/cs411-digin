BEGIN;
USE digin;
CREATE TABLE `users_customuser` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `password` varchar(128) NOT NULL, 
    `last_login` datetime(6) NULL, 
    `is_superuser` bool NOT NULL, 
    `username` varchar(150) NOT NULL UNIQUE, 
    `first_name` varchar(30) NOT NULL, 
    `last_name` varchar(150) NOT NULL, 
    `email` varchar(254) NOT NULL, 
    `is_staff` bool NOT NULL, 
    `is_active` bool NOT NULL, 
    `date_joined` datetime(6) NOT NULL, 
    `name` varchar(255) NOT NULL
    );

COMMIT;
