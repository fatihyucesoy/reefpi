SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `reefPi_RPi_schema` ;
CREATE SCHEMA IF NOT EXISTS `reefPi_RPi_schema` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
SHOW WARNINGS;
USE `reefPi_RPi_schema` ;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensorReadings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensorReadings` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensorReadings` (
  `idSensorReadings` INT NOT NULL AUTO_INCREMENT,
  `timeStamp` TIMESTAMP NOT NULL,
  `probeId` VARCHAR(45) NOT NULL,
  `reading` DOUBLE NOT NULL,
  PRIMARY KEY (`idSensorReadings`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`devices`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`devices` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`devices` (
  `iddevices` INT NOT NULL AUTO_INCREMENT,
  `deviceId` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  PRIMARY KEY (`iddevices`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensors`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensors` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensors` (
  `Idsensors` INT NOT NULL AUTO_INCREMENT,
  `sensorId` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NULL,
  `lowerlimit` DOUBLE NULL,
  `upper;Limit` DOUBLE NULL,
  `device` INT NULL,
  `period` MEDIUMTEXT NULL,
  PRIMARY KEY (`Idsensors`),
  CONSTRAINT `devieID`
    FOREIGN KEY (`device`)
    REFERENCES `reefPi_RPi_schema`.`devices` (`iddevices`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `devieID_idx` ON `reefPi_RPi_schema`.`sensors` (`device` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`commands`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`commands` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`commands` (
  `idcommands` INT NOT NULL AUTO_INCREMENT,
  `commandId` INT NOT NULL,
  `parameterList` VARCHAR(255) NULL,
  PRIMARY KEY (`idcommands`))
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
