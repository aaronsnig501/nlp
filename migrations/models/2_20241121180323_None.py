from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `process_request` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `processor` VARCHAR(15) NOT NULL,
    `language_code` VARCHAR(5) NOT NULL,
    `client_id` VARCHAR(50) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `token` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `word` VARCHAR(50) NOT NULL,
    `tag` VARCHAR(50) NOT NULL,
    UNIQUE KEY `uid_token_word_7c0837` (`word`, `tag`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `process_request_tokens` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `process_request_id` INT NOT NULL,
    `token_id` INT NOT NULL,
    CONSTRAINT `fk_process__process__8d63eb88` FOREIGN KEY (`process_request_id`) REFERENCES `process_request` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_process__token_5c26d2c1` FOREIGN KEY (`token_id`) REFERENCES `token` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `nlp_languages` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(25) NOT NULL,
    `short_code` VARCHAR(2) NOT NULL,
    `long_code` VARCHAR(8) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `nlp_services` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(25) NOT NULL,
    `languages_id` INT NOT NULL,
    CONSTRAINT `fk_nlp_serv_nlp_lang_a9371ab8` FOREIGN KEY (`languages_id`) REFERENCES `nlp_languages` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `nlp_domains` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(25) NOT NULL,
    `services_id` INT NOT NULL,
    CONSTRAINT `fk_nlp_doma_nlp_serv_a8715ead` FOREIGN KEY (`services_id`) REFERENCES `nlp_services` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `ProcessRequestTokens` (
    `process_request_id` INT NOT NULL,
    `token_id` INT NOT NULL,
    FOREIGN KEY (`process_request_id`) REFERENCES `process_request` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`token_id`) REFERENCES `token` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_ProcessRequ_process_79af29` (`process_request_id`, `token_id`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
