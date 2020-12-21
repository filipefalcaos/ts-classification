import sqlite3
import pandas as pd
from sqlite3 import Error


def create_connection(db_file):
    """ 
    Create a SQLite connection to the database specified by the "db_file" parameter
    
    :param db_file: The database file
    :return: Connection object or None
    """
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def query_testsmell(conn, testsmell, cond, limit):
    """
    Query the database to retrieve the test classes that match a given test smell and a given
    condition (i.e., smell present or absent)

    :param conn: The Connection object
    :param testsmell: The column name of the test smell
    :param cond: A string indicating if the smell is present or absent
    :param limit: A limit number of results to return
    :return A Pandas DataFrame with the query results
    """

    query = 'SELECT App, CommitSHA, RelativeTestFilePath FROM tool_testsmell_history WHERE ' + \
            testsmell + ' = \'' + cond + '\' ORDER BY RANDOM() LIMIT ' + str(limit)
    return pd.read_sql_query(query, conn)


def select_testsmell_data(conn):
    """
    Query the database to retrieve the test classes that present one of the following test smells:
    ConditionalTestLogic, ExceptionCatchingThrowing
    
    :param conn: The Connection object
    :return: A list of Pandas DataFrames of test smell classes
    """
    
    testsmells = ['ConditionalTestLogic', 'ExceptionCatchingThrowing']
    dataframes = []
    for testsmell in testsmells:
        df1 = query_testsmell(conn, testsmell, 'true', 5000)
        df2 = query_testsmell(conn, testsmell, 'false', 5000)
        df1['Smell'] = True
        df2['Smell'] = False
        
        df = pd.concat([df1, df2])  # Concat present and absent examples
        df = df.sample(frac=1).reset_index(drop=True)  # Shuffle dataframe
        dataframes.append({ 'testsmell': testsmell, 'df': df })
    
    return dataframes


def export_testsmell_data(testsmell_data):
    """
    Export the test smells data to CSV files

    :param testsmell_data: The list containing the test smell DataFrames
    """

    for data in testsmell_data:
        filename = 'data/' + data['testsmell'] + '_data.csv'
        print('Exporting ' + filename + '...')
        data['df'].to_csv(filename, index=False)


def main():
    db_file = 'data/testsmells_java.sqlite'
    conn = create_connection(db_file)
    testsmell_data = select_testsmell_data(conn)
    export_testsmell_data(testsmell_data)


if __name__ == '__main__':
    main()
