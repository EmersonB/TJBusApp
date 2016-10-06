CREATE DATABASE `buses`;

USE `buses`;

CREATE TABLE `position`
(
	`position_id` INT NOT NULL AUTOINCREMENT,
	`map_x` DOUBLE NOT NULL,
	`map_y` DOUBLE NOT NULL,
	`angle` DOUBLE NOT NULL,
	`last_updated` DATETIME,
	PRIMARY KEY (`position_id`)
);

CREATE TABLE `bus`
(
	`bus_id` INT NOT NULL AUTOINCREMENT,
	`name` VARCHAR(40),
	PRIMARY KEY (`bus_id`)
);

CREATE TABLE `assignment` (
	`assignment_id` INT NOT NULL AUTOINCREMENT,
	`date` DATE NOT NULL,
	`bus_id` INT NOT NULL,
	`position_id` INT NOT NULL,
	`last_updated` DATETIME,
	PRIMARY KEY (`assignment_id`),
	FOREIGN KEY (`bus_id`) REFERENCES `bus` (`bus_id`),
	FOREIGN KEY (`position_id`) REFERENCES `position` (`position_id`)
);
