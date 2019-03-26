BEGIN;
USE digin;
--
-- Create model Token
--
CREATE TABLE `authtoken_token` (
    `key` varchar(40) NOT NULL PRIMARY KEY, 
    `created` datetime(6) NOT NULL, 
    `user_id` integer NOT NULL UNIQUE
    );
ALTER TABLE `authtoken_token` ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`);
COMMIT;