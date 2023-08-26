import csv
import sys


def main():

    # check for correct command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # read the CSV database file
    with open(sys.argv[1], "r") as database_file:
        reader = csv.DictReader(database_file)
        database = list(reader)
        str_list = reader.fieldnames[1:]

    # read the DNA sequence file
    with open(sys.argv[2], "r") as sequence_file:
        sequence = sequence_file.read()

   # compute the longest run of each STR in the DNA sequence
    str_counts = {}
    for str_sequence in str_list:
        str_counts[str_sequence] = longest_match(sequence, str_sequence)

    # compare the STR counts against the database
    for person in database:
        match = True
        for str_sequence in str_list:
            if int(person[str_sequence]) != str_counts[str_sequence]:
                match = False
                break
        if match:
            print(person["name"])
            return
    print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
