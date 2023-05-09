ALTER TABLE t_errors ADD description_error VARCHAR(200);

UPDATE t_errors 
SET description_error = 'Repeat league'
WHERE id_error = 5;
