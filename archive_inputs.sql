START TRANSACTION;
set @N := (now());
INSERT INTO Steuerzentrale.HIS_inputs_arch select * from Steuerzentrale.HIS_inputs where Date < date_sub(@N,INTERVAL 14 DAY);
DELETE FROM Steuerzentrale.HIS_inputs WHERE Date < date_sub(@N,INTERVAL 14 DAY);
COMMIT;