BEGIN;
USE digin;

--
-- Create model Question
--
CREATE TABLE `polls_question` (
    `id` int AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `question_text` varchar(200) NOT NULL, 
    `pub_date` datetime(6) NOT NULL,
    `owner_id` int NOT NULL,
    FOREIGN KEY (`owner_id`) 
        REFERENCES `users_customuser` (`id`) 
        ON DELETE CASCADE
);
--
-- Create model Choice
--
CREATE TABLE `polls_choice` (
    `id` int AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `choice_text` varchar(200) NOT NULL, 
    `votes` int NOT NULL,
    `question_id` int NOT NULL,    
    `owner_id` int NOT NULL,
    FOREIGN KEY (`question_id`) 
        REFERENCES `polls_question` (`id`) 
        ON DELETE CASCADE,
    FOREIGN KEY (`owner_id`) 
        REFERENCES `users_customuser` (`id`) 
        ON DELETE CASCADE
);
--
-- Create model Vote
--
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

COMMIT;

