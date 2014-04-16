SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `reefPi_RPi_schema` ;
CREATE SCHEMA IF NOT EXISTS `reefPi_RPi_schema` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
SHOW WARNINGS;
USE `reefPi_RPi_schema` ;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`busType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`busType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`busType` (
  `idbusType` INT NOT NULL AUTO_INCREMENT,
  `busTypeName` VARCHAR(45) NOT NULL,
  `busTypeDescription` VARCHAR(255) NULL,
  PRIMARY KEY (`idbusType`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`deviceType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`deviceType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`deviceType` (
  `iddeviceType` INT NOT NULL AUTO_INCREMENT,
  `deviceTypeName` VARCHAR(45) NOT NULL,
  `idbusType` INT NOT NULL,
  PRIMARY KEY (`iddeviceType`),
  CONSTRAINT `FK_deviceType_busType`
    FOREIGN KEY (`idbusType`)
    REFERENCES `reefPi_RPi_schema`.`busType` (`idbusType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `FK_deviceType_busType_idx` ON `reefPi_RPi_schema`.`deviceType` (`idbusType` ASC);

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
  `deviceAddress` VARCHAR(45) NOT NULL,
  `deviceStatus` TINYINT(1) NULL,
  `deviceLevel` INT NULL,
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
-- Table `reefPi_RPi_schema`.`deviceReading`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`deviceReading` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`deviceReading` (
  `iddeviceReading` INT NOT NULL AUTO_INCREMENT,
  `deviceReading` DOUBLE NOT NULL,
  `deviceReadingTimeStamp` TIMESTAMP NULL DEFAULT now(),
  `iddevice` INT NOT NULL,
  PRIMARY KEY (`iddeviceReading`),
  CONSTRAINT `FK_deviceReading_device`
    FOREIGN KEY (`iddevice`)
    REFERENCES `reefPi_RPi_schema`.`device` (`iddevice`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `FK_deviceReading_device_idx` ON `reefPi_RPi_schema`.`deviceReading` (`iddevice` ASC);

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
-- Table `reefPi_RPi_schema`.`command`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`command` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`command` (
  `idcommand` INT NOT NULL AUTO_INCREMENT,
  `iddevice` INT NOT NULL,
  `iddeviceCommand` INT NOT NULL,
  `commandParam` VARCHAR(255) NULL,
  PRIMARY KEY (`idcommand`, `iddeviceCommand`),
  CONSTRAINT `FK_command_device`
    FOREIGN KEY (`iddevice`)
    REFERENCES `reefPi_RPi_schema`.`device` (`iddevice`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_command_deviceCommand`
    FOREIGN KEY (`iddeviceCommand`)
    REFERENCES `reefPi_RPi_schema`.`deviceCommand` (`iddeviceCommand`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `FK_command_device_idx` ON `reefPi_RPi_schema`.`command` (`iddevice` ASC);

SHOW WARNINGS;
CREATE INDEX `FK_command_deviceCommand_idx` ON `reefPi_RPi_schema`.`command` (`iddeviceCommand` ASC);

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
-- Table `reefPi_RPi_schema`.`deviceActionRelation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`deviceActionRelation` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`deviceActionRelation` (
  `iddeviceActionRelation` INT NOT NULL AUTO_INCREMENT,
  `deviceActionRelation` VARCHAR(45) NOT NULL,
  `deviceActionRelationSymbol` VARCHAR(45) NULL,
  `deviceActionRelationDescription` VARCHAR(45) NULL,
  PRIMARY KEY (`iddeviceActionRelation`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`deviceActionType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`deviceActionType` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`deviceActionType` (
  `iddeviceActionType` INT NOT NULL AUTO_INCREMENT,
  `deviceActionType` VARCHAR(45) NOT NULL,
  `deviceActionTypeDescription` BLOB NULL,
  PRIMARY KEY (`iddeviceActionType`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reefPi_RPi_schema`.`deviceAction`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reefPi_RPi_schema`.`deviceAction` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reefPi_RPi_schema`.`deviceAction` (
  `iddeviceAction` INT NOT NULL AUTO_INCREMENT,
  `idTargetDevice` INT NOT NULL,
  `deviceActionValue` DOUBLE NOT NULL,
  `iddeviceActionRelation` INT NOT NULL,
  `iddeviceActionType` INT NOT NULL,
  `idOutputDevice` INT NOT NULL,
  `iddeviceCommand` INT NOT NULL,
  `deviceCommandParam` VARCHAR(255) NULL,
  PRIMARY KEY (`iddeviceAction`),
  CONSTRAINT `FK_DeviceAction_DeviceOutput`
    FOREIGN KEY (`idOutputDevice`)
    REFERENCES `reefPi_RPi_schema`.`device` (`iddevice`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_DeviceAction_deviceCommand`
    FOREIGN KEY (`iddeviceCommand`)
    REFERENCES `reefPi_RPi_schema`.`deviceCommand` (`iddeviceCommand`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_DeviceAction_actionRelation`
    FOREIGN KEY (`iddeviceActionRelation`)
    REFERENCES `reefPi_RPi_schema`.`deviceActionRelation` (`iddeviceActionRelation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_DeviceAction_actionType`
    FOREIGN KEY (`iddeviceActionType`)
    REFERENCES `reefPi_RPi_schema`.`deviceActionType` (`iddeviceActionType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `FK_SensorAction_Device_idx` ON `reefPi_RPi_schema`.`deviceAction` (`idOutputDevice` ASC);

SHOW WARNINGS;
CREATE INDEX `FK_SensorSction_deviceCommand_idx` ON `reefPi_RPi_schema`.`deviceAction` (`iddeviceCommand` ASC);

SHOW WARNINGS;
CREATE INDEX `FK_SensorAction_actionRelation_idx` ON `reefPi_RPi_schema`.`deviceAction` (`iddeviceActionRelation` ASC);

SHOW WARNINGS;
CREATE INDEX `FK_SensorAction_actionType_idx` ON `reefPi_RPi_schema`.`deviceAction` (`iddeviceActionType` ASC);

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
