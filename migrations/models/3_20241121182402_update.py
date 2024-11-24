from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `nlp_services` DROP FOREIGN KEY `fk_nlp_serv_nlp_lang_a9371ab8`;
        ALTER TABLE `nlp_domains` ADD `display_name` VARCHAR(50) NOT NULL;
        ALTER TABLE `nlp_services` ADD `display_name` VARCHAR(50) NOT NULL;
        ALTER TABLE `nlp_services` DROP COLUMN `languages_id`;
        CREATE TABLE IF NOT EXISTS `nlp_service_languages` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `language_id` INT NOT NULL,
    `service_id` INT NOT NULL,
    CONSTRAINT `fk_nlp_serv_nlp_lang_67bca65a` FOREIGN KEY (`language_id`) REFERENCES `nlp_languages` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_nlp_serv_nlp_serv_09e6745c` FOREIGN KEY (`service_id`) REFERENCES `nlp_services` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE `ServiceLanguage` (
    `language_id` INT NOT NULL REFERENCES `nlp_languages` (`id`) ON DELETE CASCADE,
    `nlp_services_id` INT NOT NULL REFERENCES `nlp_services` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `ServiceLanguage`;
        ALTER TABLE `nlp_domains` DROP COLUMN `display_name`;
        ALTER TABLE `nlp_services` ADD `languages_id` INT NOT NULL;
        ALTER TABLE `nlp_services` DROP COLUMN `display_name`;
        DROP TABLE IF EXISTS `nlp_service_languages`;
        ALTER TABLE `nlp_services` ADD CONSTRAINT `fk_nlp_serv_nlp_lang_a9371ab8` FOREIGN KEY (`languages_id`) REFERENCES `nlp_languages` (`id`) ON DELETE CASCADE;"""
