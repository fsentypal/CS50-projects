-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports ORDER BY date DESC LIMIT 5;
SELECT * FROM witness_statements WHERE report_id = ?;  -- Replace '?' with the relevant report ID
SELECT * FROM people WHERE name LIKE '%keyword%';  -- Replace 'keyword' with any name or detail mentioned
SELECT * FROM vehicles WHERE license_plate LIKE '%keyword%';  -- Replace 'keyword' with any license plate or detail mentioned
SELECT * FROM interviews WHERE person_id = ?;  -- Replace '?' with the relevant person's ID
SELECT * FROM get_fit WHERE person_id = ? AND date = 'YYYY-MM-DD';  -- Replace '?' with the person's ID and 'YYYY-MM-DD' with the date of the crime
SELECT * FROM phone_records WHERE person_id = ? AND date = 'YYYY-MM-DD';  -- Replace '?' with the person's ID and 'YYYY-MM-DD' with the date of the crime
