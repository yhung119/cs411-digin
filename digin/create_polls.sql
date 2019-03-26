BEGIN;
USE digin;
--
-- Create model Choice
--
CREATE TABLE `polls_choice` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `choice_text` varchar(200) NOT NULL, 
    `votes` integer NOT NULL)
    ;
--
-- Create model Question
--
CREATE TABLE `polls_question` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
    `question_text` varchar(200) NOT NULL, 
    `pub_date` datetime(6) NOT NULL);
--
-- Add field question to choice
--
ALTER TABLE `polls_choice` ADD COLUMN `question_id` integer NOT NULL;
ALTER TABLE `polls_choice` ADD CONSTRAINT `polls_choice_question_id_c5b4b260_fk_polls_question_id` FOREIGN KEY (`question_id`) REFERENCES `polls_question` (`id`);
COMMIT;
