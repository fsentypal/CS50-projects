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
WHERE EXISTS (
    SELECT 1 FROM flights f
    JOIN passengers pas ON f.id = pas.flight_id
    WHERE a.id = f.destination_airport_id
    AND f.year = 2021 AND f.month = 7 AND f.day = 29 AND f.hour = 8 AND f.minute = 20
    AND EXISTS (
        SELECT 1 FROM people p
        WHERE p.passport_number = pas.passport_number AND p.name = "Sofia"
    )
);


SELECT p2.name
FROM people p1, people p2, phone_calls ph
WHERE p1.name = "Sofia"
AND p1.phone_number = ph.caller
AND p2.phone_number = ph.receiver
AND ph.year = 2021 AND ph.month = 7 AND ph.day = 28 AND ph.duration < 60
AND p1.name != p2.name;