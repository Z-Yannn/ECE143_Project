import pandas as pd

def clean_data(cape_data):
    '''
    Cleans raw cape data
    
    Args:
        cape_data (pd.DataFrame): raw cape data

    Returns:
        pd.Dataframe: cleaned dataframe
    '''

    df = cape_data

    # subset the important columns
    df = df[['Instructor', 'Course', 'Term', 'Enroll', 'Evals Made', 'Rcmnd Class',
             'Rcmnd Instr', 'Study Hrs/wk',
             'Avg Grade Received']]

    # rename the columns for convenience
    df = df.rename(columns={
        'Instructor': 'instr', 'Course': 'course', 'Term': 'term', 'Enroll': 'enroll',
        'Evals Made': 'evals', 'Rcmnd Class': 'rmd_class',
        'Rcmnd Instr': 'rmd_instr', 'Study Hrs/wk': 'time',
        'Avg Grade Received': 'grade'})

    # drop rows with missing data
    df = df.dropna()

    # drop rows with not evals
    df = df[df['evals'] != 0]

    # set and reset index to build an incremental index that starts at 0
    df = df.set_index('instr').reset_index()

    # remove outdated evals
    unique_terms = df['term'].unique()[:25]
    df = df[df['term'].isin(unique_terms)]

    # seperate course name from number
    df[['Course_ID','Course_Name1','Course_Name2']] = df['course'].str.split(' - ', expand=True)
    df['Course_Name'] = df['Course_Name1'] + df['Course_Name2'].fillna('')
    df = df.drop(columns=['course', 'Course_Name1', 'Course_Name2'])

    # seperate letter grade and number
    df[['Grade','GPA']] = df['grade'].str.split(' ', expand=True)
    df['GPA'] = df['GPA'].str[1:-1].astype(float)
    df = df.drop(columns=['grade'])

    # convert percentages into number
    df['rmd_instr'] = df['rmd_instr'].str[:-1].astype(float)
    df['rmd_class'] = df['rmd_class'].str[:-1].astype(float)

    return df

path = "ECE143_Project/data.csv"
cape_data = pd.read_csv(path)
clean = clean_data(cape_data)

export = 'ECE143_Project/data_clean.csv'
clean.to_csv(export, index=False)