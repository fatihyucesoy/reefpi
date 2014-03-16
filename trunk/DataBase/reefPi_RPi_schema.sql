SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `reefPi_RPi_schema` ;
CREATE SCHEMA IF NOT EXISTS `reefPi_RPi_schema` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
SHOW WARNINGS;
USE `reefPi_RPi_schema` ;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`deviceType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`deviceType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`deviceType` (
  `iddeviceType` INT NOT NULL AUTO_INCREMENT,
  `deviceName` VARCHAR(45) NOT NULL,
  `busType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`iddeviceType`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`controllerType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`controllerType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`controllerType` (
  `idcontrollerType` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` BLOB NULL,
  PRIMARY KEY (`idcontrollerType`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`controller`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`controller` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`controller` (
  `idcontroller` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `description` BLOB NULL,
  `idcontrollerType` INT NOT NULL,
  PRIMARY KEY (`idcontroller`),
  CONSTRAINT `FK_controller_controllerType`
    FOREIGN KEY (`idcontrollerType`)
    REFERENCES `reefPi_RPi_schema`.`controllerType` (`idcontrollerType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `FK_controllerType_idx` ON `reefPi_RPi_schema`.`controller` (`idcontrollerType` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`devices`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`devices` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`devices` (
  `iddevices` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NULL,
  `iddeviceType` INT NULL,
  `address` VARCHAR(45) NULL,
  `status` TINYINT(1) NULL,
  `idcontoller` INT NULL,
  `level` INT NULL,
  PRIMARY KEY (`iddevices`),
  CONSTRAINT `FK_deviceType`
    FOREIGN KEY (`iddeviceType`)
    REFERENCES `reefPi_RPi_schema`.`deviceType` (`iddeviceType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_contoller`
    FOREIGN KEY (`idcontoller`)
    REFERENCES `reefPi_RPi_schema`.`controller` (`idcontroller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `deviceType_idx` ON `reefPi_RPi_schema`.`devices` (`iddeviceType` ASC);

SHOW WARNINGS;
CREATE INDEX `FK_contoller_idx` ON `reefPi_RPi_schema`.`devices` (`idcontoller` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensorType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensorType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensorType` (
  `idSensorType` INT NOT NULL AUTO_INCREMENT,
  `sensorName` VARCHAR(45) NOT NULL,
  `busType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idSensorType`))
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
  `idsensorType` INT NOT NULL,
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
    ON UPDATE NO ACTION,
  CONSTRAINT `type`
    FOREIGN KEY (`idsensorType`)
    REFERENCES `reefPi_RPi_schema`.`sensorType` (`idSensorType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `devieID_idx` ON `reefPi_RPi_schema`.`sensors` (`device` ASC);

SHOW WARNINGS;
CREATE INDEX `type_idx` ON `reefPi_RPi_schema`.`sensors` (`idsensorType` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensorReadings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensorReadings` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensorReadings` (
  `idSensorReadings` INT NOT NULL AUTO_INCREMENT,
  `timeStamp` TIMESTAMP NOT NULL,
  `sensorId` INT NOT NULL,
  `reading` DOUBLE NOT NULL,
  PRIMARY KEY (`idSensorReadings`),
  CONSTRAINT `sensor`
    FOREIGN KEY (`sensorId`)
    REFERENCES `reefPi_RPi_schema`.`sensors` (`Idsensors`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `sensor_idx` ON `reefPi_RPi_schema`.`sensorReadings` (`sensorId` ASC);

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

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`link_controller_controllerType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`link_controller_controllerType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`link_controller_controllerType` (
  `idlink_controller_controllerType` INT NOT NULL AUTO_INCREMENT,
  `idcontroller` INT NULL,
  `idcontrollerType` INT NULL,
  PRIMARY KEY (`idlink_controller_controllerType`),
  CONSTRAINT `FK_controller`
    FOREIGN KEY (`idcontroller`)
    REFERENCES `reefPi_RPi_schema`.`controller` (`idcontroller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_controllerType`
    FOREIGN KEY (`idcontrollerType`)
    REFERENCES `reefPi_RPi_schema`.`controllerType` (`idcontrollerType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `controller_idx` ON `reefPi_RPi_schema`.`link_controller_controllerType` (`idcontroller` ASC);

SHOW WARNINGS;
CREATE INDEX `FK_controllerType_idx` ON `reefPi_RPi_schema`.`link_controller_controllerType` (`idcontrollerType` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`scheduleType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`scheduleType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`scheduleType` (
  `idscheduleType` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `Description` VARCHAR(255) NULL,
  PRIMARY KEY (`idscheduleType`))
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
