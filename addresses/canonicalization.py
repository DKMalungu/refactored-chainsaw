"""
You are provided with extracts from two datasets (please refer to Task 2 folder). In full, the
datasets contain tens of thousands of observations so manual processing is not feasible. The task
at hand is to match the data items between the two datasets as best as possible. The primary
matching criteria is Address (identified by fields Address Name, City and Postcode). However,
address fields are often inputted by humans, thus conventions vary widely. Please prepare an
automated approach for canonicalization. Your code should handle for discrepancies such as
representing Straße in full or shortened (Str.). The algorithm need not handle for all possible
discrepancies so do it to the best of your ability. A description of an iterative procedure is also
sufficient.
"""

# Importing Libraries
import pandas as pd
from re import search
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# Loading data
task2_data1 = pd.read_csv('./data_file/task2_data1.csv').dropna()
task2_data2 = pd.read_csv('./data_file/task2_data2.csv').dropna()

"""Renaming Column names"""
task2_data1.rename(columns={'Company.Name': 'company_name', 'Address': 'address', 'City': 'city', 'Postcode': 'postal_code'}, inplace=True)

task2_data2.rename(columns={'Address': 'address', 'Postal.Code': 'postal_code', 'Location': 'city'}, inplace=True)

task2_data1['hse_no'] = ''
task2_data2['hse_no'] = ''
task2_data1['complete_address'] = ''
task2_data2['complete_address'] = ''


def preprocess(dataframe):
    """
    :param dataframe:
    :type: pandas.core.frame.DataFrame
    """
    data_frame = dataframe
    # data_frame['hse_no'] = ''
    for index, values in data_frame.iterrows():
        city = values['city'].lower()
        postal_code = values['postal_code']

        # preprocess
        address_v = values['address'].replace('.', '')
        substring = "str"
        if search(substring, address_v):
            address_v1 = address_v.replace(substring, 'straße')
        else:
            address_v1 = address_v

        # Getting hse number
        address_list = address_v1.split(' ')
        address = " ".join(address_list[:-1])
        house_number = address_list[-1]
        data_frame.at[index, 'hse_no'] = house_number
        task2_data1.at[index, 'hse_no'] = house_number
        data_frame.at[index, 'address'] = address
        data_frame.at[index, 'city'] = city
        data_frame.at[index, 'postal_code'] = postal_code
        complete_address = city + postal_code + address + house_number
        data_frame.at[index, 'complete_address'] = complete_address
        task2_data1.at[index, 'complete_address'] = complete_address
    return data_frame


database_a = preprocess(task2_data1)
database_b = preprocess(task2_data2)

# empty lists for storing the matches later
match_a = []
match_b = []
p = []

# converting DataFrame column to list of elements to do fuzzy matching
list_1 = database_a['complete_address'].tolist()
list_2 = database_b['complete_address'].tolist()

# taking the threshold as 70
threshold = 70

for item in list_1:
    match_a.append(process.extractOne(item, list_2, scorer=fuzz.ratio))
task2_data1['matches'] = match_a


# iterating through the closest matchesto filter out the maximum closest match
for j in task2_data1['matches']:
    if j[1] >= threshold:
        p.append(j[0])
    match_b.append(",".join(p))
    p = []

# storing the resultant matches back to dframe1
task2_data1['matches'] = match_b

task2_data1.to_csv('./data_file/matched_data.csv')
