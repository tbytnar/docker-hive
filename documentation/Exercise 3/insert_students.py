import re
import pandas as pd
from pyhive import hive

# compile regular expressions
rx_dict = {
    'school': re.compile(r'School = (?P<school>.*)\n'),
    'grade': re.compile(r'Grade = (?P<grade>\d+)\n'),
    'name_score': re.compile(r'(?P<name_score>Name|Score)'),
}

def _parse_line(line):
    # check line for all regex matches
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def parse_file(filepath):
    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            key, match = _parse_line(line)

            # extract school name
            if key == 'school':
                school = match.group('school')

            # extract grade
            if key == 'grade':
                grade = match.group('grade')
                grade = int(grade)

            # identify a table header 
            if key == 'name_score':
                # extract type of table, i.e., Name or Score
                value_type = match.group('name_score')
                line = file_object.readline()
                # read each line of the table until a blank line
                while line.strip():
                    # extract number and value
                    number, value = line.strip().split(',')
                    value = value.strip()
                    # create a dictionary containing this row of data
                    row = {
                        'School': school,
                        'Grade': grade,
                        'Student number': number,
                        value_type: value
                    }
                    # append the dictionary to the data list
                    data.append(row)
                    line = file_object.readline()

            line = file_object.readline()

        # create a pandas DataFrame from the list of dicts
        data = pd.DataFrame(data)
        # set the School, Grade, and Student number as the index
        data.set_index(['School', 'Grade', 'Student number'], inplace=True)
        # consolidate df to remove nans
        data = data.groupby(level=data.index.names).first()
        # upgrade Score from float to integer
        data = data.apply(pd.to_numeric, errors='ignore')

        for key, values in data.iterrows():
            record =[key[0],key[1],key[2],values[0],values[1]]
            print('\t'.join(record))

def insert_record(record):
    conn = hive.Connection(host='hive-server', port='10000')
    cur = conn.cursor()
    insert_cmd = "INSERT INTO schooldb.students SELECT '{0}',{1},{2},'{3}',{4}".format(record[0],record[1],record[2],record[3],record[4])
    print(insert_cmd)
    cur.execute(insert_cmd)
    conn.close()

if __name__ == '__main__':
    filepath = 'students.txt'
    parse_file(filepath)
