WITH SuspiciousActivities AS (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
    AND minute BETWEEN 15 AND 25
    AND activity = "exit"
),
SuspiciousCalls AS (
    SELECT caller
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND duration < 60
),
SuspiciousTransactions AS (
    SELECT account_number
    FROM atm_transactions
    WHERE year = 2021 AND month = 7 AND day = 28
),
SuspiciousFlights AS (
    SELECT passengers.passport_number
    FROM passengers
    JOIN flights ON passengers.flight_id = flights.id
    WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29
    AND flights.hour = 8  AND flights.minute = 20
)

SELECT name
FROM people
WHERE license_plate IN (SELECT * FROM SuspiciousActivities)
AND phone_number IN (SELECT * FROM SuspiciousCalls)
AND id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (SELECT * FROM SuspiciousTransactions)
)
AND passport_number IN (SELECT * FROM SuspiciousFlights);


SELECT DISTINCT airports.city
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29
AND flights.hour = 8  AND flights.minute = 20
AND flights.id IN (
    SELECT flight_id
    FROM passengers
    WHERE passport_number IN (
        SELECT passport_number
        FROM people
        WHERE name = "Bruce"
    )
);


SELECT name
FROM people
WHERE phone_number IN (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28
    AND duration < 60
    AND caller IN (
        SELECT phone_number
        FROM people
        WHERE name = "Bruce"
    )
);