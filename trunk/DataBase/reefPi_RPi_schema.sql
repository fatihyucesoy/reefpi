SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `reefPi_RPi_schema` ;
CREATE SCHEMA IF NOT EXISTS `reefPi_RPi_schema` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
SHOW WARNINGS;
USE `reefPi_RPi_schema` ;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensorType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensorType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensorType` (
  `idSensorType` INT NOT NULL AUTO_INCREMENT,
  `sensorTypeName` VARCHAR(45) NOT NULL,
  `busType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idSensorType`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensor` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensor` (
  `Idsensor` INT NOT NULL AUTO_INCREMENT,
  `sensorName` VARCHAR(45) NOT NULL,
  `idsensorType` INT NOT NULL,
  `address` VARCHAR(45) NULL,
  `units` VARCHAR(45) NULL DEFAULT 'celsius',
  `period` INT NULL,
  PRIMARY KEY (`Idsensor`),
  CONSTRAINT `type`
    FOREIGN KEY (`idsensorType`)
    REFERENCES `reefPi_RPi_schema`.`sensorType` (`idSensorType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `type_idx` ON `reefPi_RPi_schema`.`sensor` (`idsensorType` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensorReadings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensorReadings` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensorReadings` (
  `idSensorReadings` INT NOT NULL AUTO_INCREMENT,
  `timeStamp` TIMESTAMP NOT NULL,
  `idsensor` INT NOT NULL,
  `reading` DOUBLE NOT NULL,
  PRIMARY KEY (`idSensorReadings`),
  CONSTRAINT `sensor`
    FOREIGN KEY (`idsensor`)
    REFERENCES `reefPi_RPi_schema`.`sensor` (`Idsensor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `sensor_idx` ON `reefPi_RPi_schema`.`sensorReadings` (`idsensor` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`deviceType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`deviceType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`deviceType` (
  `iddeviceType` INT NOT NULL AUTO_INCREMENT,
  `deviceTypeName` VARCHAR(45) NOT NULL,
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
  `controllerTypeName` VARCHAR(45) NOT NULL,
  `controllerTypeDescription` BLOB NULL,
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
  `controllerName` VARCHAR(45) NOT NULL,
  `idcontrollerType` INT NOT NULL,
  `controllerDescription` BLOB NULL,
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
-- Table `reefPi_RPi_schema`.`device`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`device` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`device` (
  `iddevice` INT NOT NULL AUTO_INCREMENT,
  `deviceName` VARCHAR(45) NOT NULL,
  `iddeviceType` INT NOT NULL,
  `idcontroller` INT NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `status` TINYINT(1) NULL,
  `level` INT NULL,
  PRIMARY KEY (`iddevice`),
  CONSTRAINT `FK_deviceType`
    FOREIGN KEY (`iddeviceType`)
    REFERENCES `reefPi_RPi_schema`.`deviceType` (`iddeviceType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_contoller`
    FOREIGN KEY (`idcontroller`)
    REFERENCES `reefPi_RPi_schema`.`controller` (`idcontroller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `deviceType_idx` ON `reefPi_RPi_schema`.`device` (`iddeviceType` ASC);

SHOW WARNINGS;
CREATE INDEX `FK_contoller_idx` ON `reefPi_RPi_schema`.`device` (`idcontroller` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`commands`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`commands` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`commands` (
  `idcommands` INT NOT NULL AUTO_INCREMENT,
  `iddevice` INT NOT NULL,
  `commandId` INT NOT NULL,
  `parameterList` VARCHAR(255) NULL,
  PRIMARY KEY (`idcommands`, `commandId`),
  CONSTRAINT `FK_command_device`
    FOREIGN KEY (`iddevice`)
    REFERENCES `reefPi_RPi_schema`.`device` (`iddevice`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `FK_command_device_idx` ON `reefPi_RPi_schema`.`commands` (`iddevice` ASC);

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
  `scheduleTypeName` VARCHAR(45) NOT NULL,
  `Description` VARCHAR(255) NULL,
  PRIMARY KEY (`idscheduleType`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`scheduledEvent`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`scheduledEvent` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`scheduledEvent` (
  `idscheduledEvent` INT NOT NULL AUTO_INCREMENT,
  `jobName` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `iddevice` INT NULL,
  `state` TINYINT(1) NULL,
  `value` INT NULL,
  `startDate` DATETIME NULL,
  `year` INT NULL,
  `month` INT NULL,
  `day` INT NULL,
  `week` INT NULL,
  `day_of_week` INT NULL,
  `hour` INT NULL,
  `minute` INT NULL,
  `second` INT NULL,
  PRIMARY KEY (`idscheduledEvent`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`sensorAction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`sensorAction` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`sensorAction` (
  `idsensorAction` INT NOT NULL AUTO_INCREMENT,
  `idsensor` INT NOT NULL,
  `value` DOUBLE NOT NULL,
  `relation` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  `iddevice` INT NOT NULL,
  `action` INT NOT NULL,
  PRIMARY KEY (`idsensorAction`),
  CONSTRAINT `FK_SensorAction_Device`
    FOREIGN KEY (`iddevice`)
    REFERENCES `reefPi_RPi_schema`.`device` (`iddevice`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `FK_SensorAction_Device_idx` ON `reefPi_RPi_schema`.`sensorAction` (`iddevice` ASC);

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
