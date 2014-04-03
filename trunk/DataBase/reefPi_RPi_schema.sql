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
  `idsensorType` INT NOT NULL AUTO_INCREMENT,
  `sensorTypeName` VARCHAR(45) NOT NULL,
  `busType` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idsensorType`))
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
    REFERENCES `reefPi_RPi_schema`.`sensorType` (`idsensorType`)
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
  `command` VARCHAR(45) NOT NULL,
  `parameterList` VARCHAR(255) NULL,
  PRIMARY KEY (`idcommands`, `command`),
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
-- Table `reefPi_RPi_schema`.`deviceCommand`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`deviceCommand` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`deviceCommand` (
  `iddeviceCommand` INT NOT NULL AUTO_INCREMENT,
  `deviceCommand` VARCHAR(45) NOT NULL,
  `deviceCommandDescription` BLOB NULL,
  PRIMARY KEY (`iddeviceCommand`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`link_deviceType_deviceCommand`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`link_deviceType_deviceCommand` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`link_deviceType_deviceCommand` (
  `idlink_deviceType_deviceCommand` INT NOT NULL AUTO_INCREMENT,
  `iddevice` INT NOT NULL,
  `iddeviceCommand` INT NOT NULL,
  PRIMARY KEY (`idlink_deviceType_deviceCommand`),
  CONSTRAINT `FK_link_device_devicecommand`
    FOREIGN KEY (`iddevice`)
    REFERENCES `reefPi_RPi_schema`.`device` (`iddevice`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_link_deviceCommand_device`
    FOREIGN KEY (`iddeviceCommand`)
    REFERENCES `reefPi_RPi_schema`.`deviceCommand` (`iddeviceCommand`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `FK_link_device_devicecommand_idx` ON `reefPi_RPi_schema`.`link_deviceType_deviceCommand` (`iddevice` ASC);

SHOW WARNINGS;
CREATE INDEX `FK_link_deviceCommand_device_idx` ON `reefPi_RPi_schema`.`link_deviceType_deviceCommand` (`iddeviceCommand` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`scheduleType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`scheduleType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`scheduleType` (
  `idscheduleType` INT NOT NULL AUTO_INCREMENT,
  `scheduleTypeName` VARCHAR(45) NOT NULL,
  `scheduleTypeDescription` BLOB NULL,
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
  `jobName` VARCHAR(45) NOT NULL,
  `idscheduleType` INT NOT NULL,
  `iddevice` INT NULL,
  `iddeviceCommand` INT NULL,
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
  PRIMARY KEY (`idscheduledEvent`),
  CONSTRAINT `FK_scheduleEvent_scheduleType`
    FOREIGN KEY (`idscheduleType`)
    REFERENCES `reefPi_RPi_schema`.`scheduleType` (`idscheduleType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_scheduleEvent_scheduleTypeCommand`
    FOREIGN KEY (`iddeviceCommand`)
    REFERENCES `reefPi_RPi_schema`.`deviceCommand` (`iddeviceCommand`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `FK_scheduleEvent_scheduleType_idx` ON `reefPi_RPi_schema`.`scheduledEvent` (`idscheduleType` ASC);

SHOW WARNINGS;
CREATE INDEX `FK_scheduleEvent_scheduleTypeCommand_idx` ON `reefPi_RPi_schema`.`scheduledEvent` (`iddeviceCommand` ASC);

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
  `action` VARCHAR(45) NOT NULL,
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
