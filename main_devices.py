#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 20:12:49 2017

@author: christoph
"""

ALTER TABLE `Steuerzentrale`.`set_Szenen` 
ADD COLUMN `Vm1FLU1DEK1LI01` TEXT NULL AFTER `V00WOH1RUM1PC01`;

UPDATE `Steuerzentrale`.`set_Szenen` SET `Vm1FLU1DEK1LI01`='ZWave' WHERE `Id`='1';
UPDATE `Steuerzentrale`.`set_Szenen` SET `Vm1FLU1DEK1LI01`='Deckenlicht' WHERE `Id`='5';


SELECT * FROM Steuerzentrale.set_Szenen where Id in (1,5);