





#-------------------------------------------------------------------------------

# report cleaner


def clean_report(report):
    """
    Clean the report by removing unwanted characters and formatting.

    Args:
        report (dict): Dictionary containing chapters and their corresponding text.

    Returns:
        dict: Cleaned report.
    """
    
    # Remove unwanted characters from the report
    for chapter, text in report.items():
        report[chapter] = text.strip()
        report[chapter] = report[chapter].replace("\n", " ")
        report[chapter] = report[chapter].replace("\t", " ")

    return report


#-------------------------------------------------------------------------------

## PAIRS GENERATION 

def generate_pairs(list,count_duplicates=True):
    """
    Generate all potential pairs from a list (used to generate list of thematic areas).

    Args:
        list (list): e.g. list of thematic areas.
        count_duplicates (bool, optional): Whether to count double pairs. Defaults to True.

    Returns:
        dict: Dictionary of pairs.
    """

    ta_pairs = {}  # dictionary to store all thematic area pairs
    ta_list = list  # list of thematic areas
    pair_id = 0  # initialize pair_id to 0

    for i in range(len(ta_list)): 
        for j in range(len(ta_list)):
            if i != j:
                if not count_duplicates and i > j:
                    continue
                ta_pairs[pair_id] = [ta_list[i], ta_list[j]] 
                pair_id += 1

    return ta_pairs

#--------------------------------------------------------------------------------

def generate_subthemes_dict(data):
    """
    Generate a dictionary with thematic areas as keys and sub-themes as nested keys.
    Each sub-theme should contain a list of dictionaries with target data (code, content and assessment from report1).

    Args:
        data (pandas.DataFrame): DataFrame that needs to contain the following columns: 
                                 'thematic_area_code', 'sub_theme', 'target_code', 'target_content', 'target_assessment'

    Returns:
        dict: Dictionary with thematic areas as keys and sub-themes as nested keys.
              Dictionary structure: 'target_data_dict' / thematic_area_code / sub_theme / ta_code | ta_content | ta_assessment.
              
    Example: target_data_dict['TA1']['Rail]
    """

    # Initialize an empty dictionary to store sub-themes and their target data
    subthemes_dict = {theme: data[data['sub_theme'] == theme][['target_code', 'target_content', 'target_assessment']].to_dict(orient='records') 
                      for theme in data['sub_theme'].unique()}

    # Initialize an empty dictionary to store the final result
    target_data_dict = {}

    # Iterate over unique thematic areas
    for ta in data['thematic_area_code'].unique():
        # Initialize the thematic area in the dictionary
        target_data_dict[ta] = {}
        
        # Iterate over unique sub-themes for the current thematic area
        for theme in data[data['thematic_area_code'] == ta]['sub_theme'].unique():
            # Add the sub-theme DataFrame to the target_data_dict
            target_data_dict[ta][theme] = subthemes_dict[theme]

    return target_data_dict

#--------------------------------------------------------------------------------

def generate_policydoc_dict(data):
    """
    Generate a dictionary with thematic areas as keys and policy documents as nested keys.
    Each policy document should contain a list of dictionaries with target data (code, content and assessment from report1).

    Args:
        data (pandas.DataFrame): DataFrame that needs to contain the following columns: 
                                 'thematic_area_code', 'policy_document_short', 'target_code', 'target_content', 'target_assessment'

    Returns:
        dict: Dictionary with thematic areas as keys and sub-themes as nested keys.
              Dictionary structure: 'target_data_dict' / thematic_area_code / policy_document_short / ta_code | ta_content | ta_assessment.
    
    Example: target_data_dict['TA1']['European Climate Law]
    """

    # Create a dictionary to store policy documents and their target data
    policydoc_dict = {policydoc: data[data['policy_document_short'] == policydoc][['target_code', 'target_content', 'target_assessment']].to_dict(orient='records') 
                      for policydoc in data['policy_document_short'].unique()}

    # Create the final overarching dictionary
    target_data_dict = {}

    # Iterate over unique thematic areas
    for ta in data['thematic_area_code'].unique():
        # Initialize the thematic area in the dictionary
        target_data_dict[ta] = {}
        
        # Iterate over unique policy documents for the current thematic area
        for policydoc in data[data['thematic_area_code'] == ta]['policy_document_short'].unique():
            # Add the policy document data to the target_data_dict
            target_data_dict[ta][policydoc] = policydoc_dict[policydoc]

    return target_data_dict

#--------------------------------------------------------------------------------

def generate_thematic_area_dict(data):
    """
    Generate a dictionary with thematic areas as keys and target data as values (codes, contents and assessments from report1).

    Args:
        data (pandas.DataFrame): DataFrame that needs to contain the following columns: 
                                 'thematic_area_code', 'target_code', 'target_content', 'target_assessment'

    Returns:
        dict: Dictionary with thematic areas as keys and sub-themes as nested keys.
              Dictionary structure: 'target_data_dict' / thematic_area_code / ta_code | ta_content | ta_assessment.
    
    Example: target_data_dict['TA1']
    """

    # Create a dictionary to store thematic areas and their target data
    target_data_dict = {ta: data[data['thematic_area_code'] == ta][['target_code', 'target_content', 'target_assessment']].to_dict(orient='records') 
                        for ta in data['thematic_area_code'].unique()}

    return target_data_dict


#-----------------------------------------------------------------------------------

def generate_dict(data, sort_by):
    """
    Generate a dictionary with thematic areas as keys and specified type as nested keys or values.

    Args:
        data (pandas.DataFrame): DataFrame containing thematic areas, target data, and other relevant columns.
        type (str): Type of dictionary to generate. Can be 'subthemes', 'policydoc', or 'thematic_area'.

    Returns:
        dict: Dictionary containing target data sorted by either subthemes, policydocs or just thematic areas.

    Raises:
        ValueError: If the specified type is not one of 'subthemes', 'policydoc', or 'thematic_area'.
    """

    if sort_by == 'subthemes':
        print(f'''You have selected to sort the data by 'subthemes'.\nThis is required to generate a subtheme-to-subtheme network. \n''')
        return generate_subthemes_dict(data)
    
    elif sort_by == 'policydoc':
        print(f'''You have selected to sort the data by 'policydoc'.\nThis is required to generate a policydoc-to-policydoc network. \n''')
        return generate_policydoc_dict(data)
    
    elif sort_by == 'thematic_area':
        print(f'''You have selected to sort the data by 'thematic_area'.\nThis is required to generate a target-to-target network. \n''')
        return generate_thematic_area_dict(data)
    
    else:
        raise ValueError("Invalid type. Must be one of 'subthemes', 'policydoc', or 'thematic_area'.")

    



#-------------------------------------------------------------------------------

import glob
import pandas as pd

def aggregate_csv(date: str, output_dir: str, sep: str = ',', file_pattern: str = '*.csv') -> None:
    """
    Aggregate CSV files in the specified output directory into a single dataframe and write to a new CSV file.

    Args:
        date (str): Date to include in the output file name.
        output_dir (str): Directory containing the CSV files to aggregate.
        sep (str, optional): Separator to use when reading and writing CSV files. Defaults to ','.
        file_pattern (str, optional): Pattern to match CSV files. Defaults to '*.csv'.
    """

    # Get a list of all CSV files matching the pattern
    csv_files = glob.glob(f"{output_dir}/{file_pattern}")

    # Initialize an empty list to store the dataframes
    dataframes = []

    # Iterate over each CSV file, read it into a dataframe, and append to the list
    for file in csv_files:
        try:
            df = pd.read_csv(file, on_bad_lines='skip', sep=sep)
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading file {file}: {e}")

    # Concatenate all dataframes into a single dataframe
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
    else:
        print("No dataframes to concatenate.")
        return

    # Write the combined dataframe to a new CSV file
    output_file = f"{output_dir}{date}_network_aggregated.csv"
    combined_df.to_csv(output_file, index=True, sep=sep)
    print(f"✅ Aggregation complete. Saved to: {output_dir}")


#-------------------------------------------------------------------------------
    



## Useful lists
    
impact_weight_meanings = {     # a list in json object format so that the LLM can most efficiently understand its structure, based on Nilssen et al. (2016)
  "weights": [
    {
      "weight": "+3",
      "name": "Indivisible",
      "explanation": "Inextricably linked to the achievement of another target.",
      "example": "Ending all forms of discrimination against women and girls is indivisible from ensuring women’s full and effective participation and equal opportunities for leadership."
    },
    {
      "weight": "+2",
      "name": "Reinforcing",
      "explanation": "Aids the achievement of another target.",
      "example": "Providing access to electricity reinforces water‐pumping and irrigation systems. Strengthening the capacity to adapt to climate‐related hazards reduces losses caused by disasters."
    },
    {
      "weight": "+1",
      "name": "Enabling",
      "explanation": "Creates conditions that further another target.",
      "example": "Providing electricity access in rural homes enables education, because it makes it possible to do homework at night with electric lighting."
    },
    {
      "weight": "-1",
      "name": "Constraining",
      "explanation": "Limits options on another target.",
      "example": "Improved water efficiency can constrain agricultural irrigation. Reducing climate change can constrain the options for energy access."
    },
    {
      "weight": "-2",
      "name": "Counteracting",
      "explanation": "Clashes with another target.",
      "example": "Boosting consumption for growth can counteract waste reduction and climate mitigation."
    },
    {
      "weight": "-3",
      "name": "Cancelling",
      "explanation": "Makes it impossible to reach another goal.",
      "example": "Fully ensuring public transparency and democratic accountability cannot be combined with national‐security goals. Full protection of natural reserves excludes public access for recreation."
    }
  ]
}


thematic_areas = {
    'TA1': 'TA1_Climate ambition',
    'TA2': 'TA2_Clean, affordable and secure energy',
    'TA3': 'TA3_Industrial strategy for a clean and circular economy',
    'TA4': 'TA4_Sustainable and smart mobility',
    'TA5': 'TA5_Greening the Common Agricultural Policy - Farm to Fork Strategy',
    'TA6': 'TA6_Preserving and protecting biodiversity',
    'TA7': 'TA7_Towards a zero-pollution ambition for a toxic free environment',
}


