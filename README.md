# DatabaseGUI

UPDATE SIGHTINGS
SET name = 'California', person= 'Frankfurt', location= 'orlando',sighted = '1923-23-12'
WHERE (name = 'California flannelbush' and person= 'jay' and location= 'Scodie Mountains' and sighted = '2006-06-26');


UPDATE SIGHTINGS
SET Person = "Bobby", Location = "Orlando", Sighted = "9999-99-99"
WHERE Person = "Donna" AND Location = "Chula Vista Campground" AND Sighted = "2006-07-03" AND name = "Alpine columbine"


SELECT PERSON, LOCATION, SIGHTED FROM SIGHTINGS WHERE NAME IN (SELECT COMNAME FROM FLOWERS WHERE COMNAME = "Alpine columbine")

SELECT * FROM SIGHTINGS ORDER BY SIGHTED DESC


'UPDATE SIGHTINGS SET Person =\"'+updateperson+',\" Location =\"'+updatelocation+',\" Sighted =\"'+updatesighting+'\" WHERE Person =\"'+originalperson+',\" Location =\"'+originallocation+',\" Sighted =\"'+originalsighting+',\" name =\"'+originalflower+'\"'



cc = conn.execute('UPDATE SIGHTINGS SET PERSON= \"'+updateperson+'\", LOCATION =\"'+updatelocation+'\", SIGHTED =\"'+updatesighting+'\" WHERE             ')
