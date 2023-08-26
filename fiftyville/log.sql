SELECT p.name
FROM people p
WHERE EXISTS (
    SELECT 1 FROM bakery_security_logs b
    WHERE p.license_plate = b.license_plate
    AND b.year = 2021 AND b.month = 7 AND b.day = 28 AND b.hour = 10 AND b.minute BETWEEN 15 AND 25 AND b.activity = "exit"
)
AND EXISTS (
    SELECT 1 FROM phone_calls ph
    WHERE p.phone_number = ph.caller
    AND ph.year = 2021 AND ph.month = 7 AND ph.day = 28 AND ph.duration < 60
);

SELECT a.city
FROM airports a
JOIN flights f ON a.id = f.destination_airport_id
JOIN passengers pas ON f.id = pas.flight_id
JOIN people p ON p.passport_number = pas.passport_number
WHERE f.year = 2021 AND f.month = 7 AND f.day = 29 AND f.hour = 8 AND f.minute = 20
AND p.name = "Bruce";  -- Replace "Bruce" with the name deduced from the previous query

SELECT p2.name
FROM people p1
JOIN passengers pas1 ON p1.passport_number = pas1.passport_number
JOIN flights f1 ON pas1.flight_id = f1.id
JOIN passengers pas2 ON f1.id = pas2.flight_id
JOIN people p2 ON pas2.passport_number = p2.passport_number
WHERE f1.year = 2021 AND f1.month = 7 AND f1.day = 29 AND f1.hour = 8 AND f1.minute = 20
AND p1.name = "Bruce"  -- Replace "Bruce" with the name deduced from the first query
AND p1.name != p2.name;