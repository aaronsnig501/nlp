from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `assessment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `mood` VARCHAR(25) NOT NULL,
    `bias` VARCHAR(25) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `process_request` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `processor` VARCHAR(15) NOT NULL,
    `language_code` VARCHAR(5) NOT NULL,
    `client_id` VARCHAR(50) NOT NULL,
    `text` LONGTEXT NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `sentiment_analysis` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `text` LONGTEXT NOT NULL,
    `mood` VARCHAR(25) NOT NULL,
    `bias` VARCHAR(25) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `sentiment_analysis_assessment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `assessment_id` INT NOT NULL,
    `sentiment_analysis_id` INT NOT NULL,
    CONSTRAINT `fk_sentimen_assessme_a27f825a` FOREIGN KEY (`assessment_id`) REFERENCES `assessment` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_sentimen_sentimen_c0b1c498` FOREIGN KEY (`sentiment_analysis_id`) REFERENCES `sentiment_analysis` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `token` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `word` VARCHAR(50) NOT NULL,
    `tag` VARCHAR(50) NOT NULL,
    UNIQUE KEY `uid_token_word_7c0837` (`word`, `tag`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `assessment_token` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `assessment_id` INT NOT NULL,
    `token_id` INT NOT NULL,
    CONSTRAINT `fk_assessme_assessme_105f1a36` FOREIGN KEY (`assessment_id`) REFERENCES `assessment` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_assessme_token_3e98eb19` FOREIGN KEY (`token_id`) REFERENCES `token` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `process_request_tokens` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `process_request_id` INT NOT NULL,
    `sentiment_analysis_id` INT,
    `token_id` INT NOT NULL,
    CONSTRAINT `fk_process__process__8d63eb88` FOREIGN KEY (`process_request_id`) REFERENCES `process_request` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_process__sentimen_4f3aea10` FOREIGN KEY (`sentiment_analysis_id`) REFERENCES `sentiment_analysis` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_process__token_5c26d2c1` FOREIGN KEY (`token_id`) REFERENCES `token` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `languages` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(25) NOT NULL,
    `short_code` VARCHAR(2) NOT NULL,
    `long_code` VARCHAR(8) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `services` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(25) NOT NULL,
    `display_name` VARCHAR(50) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `domains` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(25) NOT NULL,
    `display_name` VARCHAR(50) NOT NULL,
    `services_id` INT NOT NULL,
    CONSTRAINT `fk_domains_services_47252b87` FOREIGN KEY (`services_id`) REFERENCES `services` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `service_languages` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `language_id` INT NOT NULL,
    `service_id` INT NOT NULL,
    CONSTRAINT `fk_service__language_6923fbc2` FOREIGN KEY (`language_id`) REFERENCES `languages` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_service__services_84382cc2` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
