#!/usr/bin/python
import sys

def aggregation(list):

    # Sort the list in case of tie, we use the first in lexicographical order.
    list.sort()gi

    # Retrieve the city which held the most number of matches for each country.
    max_key_city, max_count_city = max(list, key=lambda x:x[2])[1:]

    # Empty list for next country.
    list = []

    return max_key_city, max_count_city, list

def reducer():

    # Set variables.
    key_country = ""; key_city = ""; max_key_city = "";
    count_country = 0; count_city = 0; max_count_city = 0
    change = False
    temp_list = []

    # Create the output file and write header.
    output = open("output.txt", "w")
    output.write("country" + "\t" + "total_matches" + "\t" "city" + "\t" + "max_matches" + "\n")

    # Loop over the mapper input (key, value) pairs.
    for row in sys.stdin:
        data = row.strip().split("\t")

        # Retrieve the attributes of interest.
        curr_country, curr_city, value = data

        # Try to convert the value from mapper "1" to an integer 1.
        try:
            value = int(value)
        except ValueError:
            continue

        # If country key is not already present in the output we write to output.
        if key_country != curr_country:

            if key_country:
                output.write(key_country + "\t" + str(count_country) + "\t")
                temp_list.append((key_country, key_city, count_city))

            # Set variable to ensure that the aggregation "max" function only applies to cities by country.
            change = True

            # Call the aggregation function to retrieve the city with most matches and write to output.
            if change and temp_list:
                max_key_city, max_count_city, temp_list = aggregation(temp_list)
                output.write(max_key_city + "\n")

                # Print to shell for debugging.
                print("{0}\t{1}\t{2}\t{3}".format(key_country, str(count_country), max_key_city, str(max_count_city)))

            # Start over with a new country key.
            key_country = curr_country
            count_country = 0
            change = False

        # Increase the country count per iteration.
        count_country += int(value)

        # If country key is not already present in the country we append to list.
        if key_city != curr_city:
            if key_city:
                temp_list.append((key_country, key_city, count_city))

            # Start over with a new city key.
            key_city = curr_city
            count_city = 0

        # Increase the country count per iteration.
        count_city += int(value)

    # Print the final entry to shell for debugging.
    print("{0}\t{1}\t{2}\t{3}".format(key_country, str(count_country), max_key_city, str(max_count_city)))

    # Compute last aggregation and write the final entry to file once job is completed.
    max_key_city, max_count_city, _ = aggregation(temp_list)
    output.write(key_country + "\t" + str(count_country) + "\t" + max_key_city + "\t" + str(max_count_city) + "\n")

    # Close the output file.
    output.close()

if __name__ == "__main__":
    reducer()

# python mapper.py | sort | python reducer.py
