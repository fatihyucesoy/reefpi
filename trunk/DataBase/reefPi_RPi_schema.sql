SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `reefPi_RPi_schema` ;
CREATE SCHEMA IF NOT EXISTS `reefPi_RPi_schema` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `reefPi_RPi_schema` ;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensorReadings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensorReadings` ;

CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensorReadings` (
  `idsenosrReadings` INT NOT NULL,
  `timeStamp` TIMESTAMP NOT NULL,
  `probeId` VARCHAR(45) NOT NULL,
  `reading` DOUBLE NOT NULL,
  PRIMARY KEY (`idsenosrReadings`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensors`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensors` ;

CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensors` (
  `Idsenors` INT NOT NULL,
  `senosrId` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NULL,
  `lowerlimit` DOUBLE NULL,
  `upper;Limit` DOUBLE NULL,
  `device` INT NULL,
  PRIMARY KEY (`Idsenors`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`devices`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`devices` ;

CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`devices` (
  `iddevices` INT NOT NULL,
  `deviceId` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  PRIMARY KEY (`iddevices`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`commands`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`commands` ;

CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`commands` (
  `idcommands` INT NOT NULL,
  `commandId` INT NOT NULL,
  `parameterList` VARCHAR(255) NULL,
  PRIMARY KEY (`idcommands`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
