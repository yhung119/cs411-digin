BEGIN;
--
-- Create model Token
--
CREATE TABLE `authtoken_token` (
    `key` varchar(40) NOT NULL PRIMARY KEY, 
    `created` datetime(6) NOT NULL, 
    `user_id` integer NOT NULL UNIQUE
    FOREIGN KEY (`user_id`) 
        REFERENCES `users_customuser` (`id`)
        ON DELETE CASCADE;
    );
COMMIT;