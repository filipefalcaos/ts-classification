import pandas as pd
import subprocess

from git import Repo, GitCommandError
from tqdm import tqdm


def get_vector(filename):
    """
    Get the vector representation of a Java file by using the Tokenizer software, available at
    https://github.com/dspinellis/tokenizer

    :param filename: The filename
    :return The vector representation of the Java file
    """

    command = 'tokenizer -l Java ' + filename
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    try:
        output, error = process.communicate()
        output = output.decode('utf8')
        output = output.replace('\t', ' ').replace('\n', '')
        return output
    except:
        print(error)
        return ''


def get_source_vectors(testsmells):
    """
    Get the vector representation of the Java files for each entry in the test smells datasets

    :param testsmells: The list of test smells
    :return A list of Pandas DataFrames of test smell classes
    """

    for testsmell in testsmells:
        df = pd.read_csv('data/' + testsmell + '_data.csv')
        df['Vector'] = ''

        repnames = df['App'].unique().tolist()
        for repname in repnames:
            print('Processing project \'' + repname + '\' for ' + testsmell + '...')
            currdf = df[df['App'] == repname]
            repo = Repo('repositories/' + repname)
            vectors = []
            
            # Get the vectors for each Java file in the dataframe
            for _, row in tqdm(list(currdf.iterrows())):                
                try:
                    repo.git.checkout(row['CommitSHA'], force=True)
                    file_path = 'repositories/' + repname + '/' + row['RelativeTestFilePath']
                    vectors.append(get_vector(file_path))
                except GitCommandError as err:
                    print('Failed for ' + row['App'] + ':' + row['CommitSHA'])
                    print(err)
                    vectors.append('')
            
            df.loc[df['App'] == repname, 'Vector'] = vectors  # Set the vectors on the dataframe
        
        filename = 'data/' + testsmell + '_vectors.csv'
        df.to_csv(filename, index=False)


def main():
    testsmells = ['ConditionalTestLogic', 'ExceptionCatchingThrowing']
    get_source_vectors(testsmells)


if __name__ == '__main__':
    main()
