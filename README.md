# DatabaseGUI

UPDATE SIGHTINGS
SET name = 'California', person= 'Frankfurt', location= 'orlando',sighted = '1923-23-12'
WHERE (name = 'California flannelbush' and person= 'jay' and location= 'Scodie Mountains' and sighted = '2006-06-26');


UPDATE SIGHTINGS
SET name = 'California', person= 'Frankfurt', location= 'orlando',sighted = '2006-09-29'
WHERE (name = 'Alpine columbine' and person= 'Jennifer' and location= 'Steve Spring' and sighted = '2006-09-28');


SELECT PERSON, LOCATION, SIGHTED FROM SIGHTINGS, FLOWERS WHERE (FLOWERS.COMNAME = "Alpine columbine") ORDER BY SIGHTINGS.SIGHTED DESC LIMIT 10

SELECT * FROM SIGHTINGS ORDER BY SIGHTED DESC
