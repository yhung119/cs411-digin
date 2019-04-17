BEGIN;

-- Create model Question

CREATE TABLE `polls_question` (
    `id` int AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `question_text` varchar(200) NOT NULL, 
    `pub_date` datetime(6) NOT NULL,
    `owner_id` int NOT NULL,
    `is_active` boolean NOT NULL,
    `deadline` datetime(6) NOT NULL,
    FOREIGN KEY (`owner_id`) 
        REFERENCES `users_customuser` (`id`) 
        ON DELETE CASCADE
);
--
-- Create model polls_poll_members
--
CREATE TABLE `polls_poll_members` (
    `id` int AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `question_id` int NOT NULL,    
    `member_id` int NOT NULL,
    FOREIGN KEY (`member_id`) 
        REFERENCES `users_customuser` (`id`) 
        ON DELETE CASCADE,
    FOREIGN KEY (`question_id`) 
        REFERENCES `polls_question` (`id`) 
        ON DELETE CASCADE
);

--
-- Create model Place
--
CREATE TABLE `polls_place` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `name` varchar(200) NOT NULL, 
    `phone` varchar(200) NOT NULL, 
    `address` varchar(200) NOT NULL, 
    `price_level` integer NOT NULL, 
    `rating` integer NOT NULL, 
    `latitude` integer NOT NULL, 
    `longitude` integer NOT NULL, 
    `place_id` varchar(200) NOT NULL UNIQUE, 
    `website` varchar(200) NOT NULL, 
    `reviews` varchar(10000) NOT NULL
);

-- 
-- Create model Choice
--
CREATE TABLE `polls_choice` (
    `id` int AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `name` varchar(200) NOT NULL,
    `votes` int NOT NULL,
    `question_id` int NOT NULL,    
    `owner_id` int NOT NULL,
    `place_id` varchar(200) NOT NULL,
    FOREIGN KEY (`question_id`) 
        REFERENCES `polls_question` (`id`) 
        ON DELETE CASCADE,
    FOREIGN KEY (`owner_id`) 
        REFERENCES `users_customuser` (`id`) 
        ON DELETE CASCADE,
    FOREIGN KEY (`place_id`) 
        REFERENCES `polls_place` (`place_id`) 
        ON DELETE CASCADE
);



-- Create model Vote

CREATE TABLE `polls_vote` (
    `id` int AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `choice_id` int NOT NULL,
    `question_id` int NOT NULL,
    `owner_id` int NOT NULL,
    FOREIGN KEY (`question_id`) 
        REFERENCES `polls_question` (`id`) 
        ON DELETE CASCADE,
    FOREIGN KEY (`choice_id`) 
        REFERENCES `polls_choice` (`id`)
        ON DELETE CASCADE,
    FOREIGN KEY (`owner_id`) 
        REFERENCES `users_customuser` (`id`) 
        ON DELETE CASCADE
);
--
-- Creating archive question model
--
-- todo make sure archive is unique
CREATE TABLE `polls_archive_question` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `question_id` int NOT NULL,
    `place_id` varchar(200) NOT NULL,
    FOREIGN KEY (`question_id`) 
        REFERENCES `polls_question` (`id`) 
        ON DELETE CASCADE,
    FOREIGN KEY (`place_id`) 
        REFERENCES `polls_place` (`place_id`) 
        ON DELETE CASCADE
);


COMMIT;

