import psycopg2
import os
import sys

def RangeQuery(ratingsTableName, ratingMinValue, ratingMaxValue, openconnection):
    data = []

    cur = openconnection.cursor()
    cur.execute('select current_database()')
    db_name = cur.fetchall()[0][0]

    cur.execute('select table_name from information_schema.tables where table_name like \'%rangeratingspart%\' and table_catalog=\'' + db_name + '\'')
    range_partitions = cur.fetchall()

    for table in range_partitions:
        table_name = table[0]
        cur.execute('select userid, movieid, rating from ' + str(table_name) + ' where rating >= ' + str(ratingMinValue) + ' and rating <= ' + str(ratingMaxValue))
        matches = cur.fetchall()

        for match in matches:
            partition = "RangeRatingsPart" + table_name[-1]
            data.append(str(partition) + "," + str(match[0]) + "," + str(match[1]) + "," + str(match[2]))
    
    cur.close()

    fh = open("RangeQueryOut.txt","w")
    fh.write("\n".join(data))
    fh.close()
