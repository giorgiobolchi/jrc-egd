import pandas as pd
import openai
import time
import logging

### SET UP LOGGING
logging.basicConfig(filename='process_log_topic_classification.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

####################################
######### READ IN DATA #############
####################################

# read in query df
# read data
# dat = pd.read_excel('2023_08_26_query_data.xlsx', sheet_name='Global')
dat = pd.read_excel('additional_abstracts.xlsx', sheet_name='missing_abstracts')
dat = dat[['EID', 'Abstract', 'Title', 'DOI']]

# filter out rows with empty abstracts
dat = dat[dat['Abstract'].str.len() >= 20]

# export rows wqithout abstracts
no_abstract = dat[dat['Abstract'].str.len() <= 30]
no_abstract.to_excel('missing_abstracts.xlsx', sheet_name='missing_abstracts')

# set API token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4NWM5ZjYwLWFjZWEtNDY0NS05MTI2LTkwMzU0NDkxYWRiYiIsImlzcyI6ImdwdGpyYyIsImlhdCI6MTY5OTUzNjEzOCwiZXhwIjoxNzQ2NjYyNDAwLCJpc19yZXZva2VkIjpmYWxzZSwiYWNjb3VudF9pZCI6IlFXeGxjeTVTUlVKRlEwQmxlSFF1WldNdVpYVnliM0JoTG1WMVMyNXZkMU5FUjNNPSIsInVzZXJuYW1lIjoiQWxlcy5SRUJFQ0BleHQuZWMuZXVyb3BhLmV1IiwicHJvamVjdF9pZCI6Iktub3dTREdzIiwicXVvdGFzIjpbeyJtb2RlbF9uYW1lIjoiZ3B0LTM1LXR1cmJvLTA2MTMiLCJleHBpcmF0aW9uX2ZyZXF1ZW5jeSI6ImRhaWx5IiwidmFsdWUiOjIwMDAwMH0seyJtb2RlbF9uYW1lIjoiZ3B0LTM1LXR1cmJvLTE2ayIsImV4cGlyYXRpb25fZnJlcXVlbmN5IjoiZGFpbHkiLCJ2YWx1ZSI6MjAwMDAwfSx7Im1vZGVsX25hbWUiOiJncHQtMzUtdHVyYm8tMDMwMSIsImV4cGlyYXRpb25fZnJlcXVlbmN5IjoiZGFpbHkiLCJ2YWx1ZSI6MjAwMDAwfSx7Im1vZGVsX25hbWUiOiJncHQtNCIsImV4cGlyYXRpb25fZnJlcXVlbmN5IjoiZGFpbHkiLCJ2YWx1ZSI6MjAwMDAwfSx7Im1vZGVsX25hbWUiOiJncHQtNC0zMmsiLCJleHBpcmF0aW9uX2ZyZXF1ZW5jeSI6ImRhaWx5IiwidmFsdWUiOjIwMDAwMH1dfQ.gESiPlbhdVc5F5Nn5V4RT02HwNtj1Rm3-JrgEfG2Pac"
openai.api_base = "https://api-gpt.jrc.ec.europa.eu/v1"
openai.api_key = TOKEN

#####################################
####### TOPIC Classification ########
#####################################

def run_API_request(prompt):

    chat_completion = openai.ChatCompletion.create(
        headers={"Authorization": f"Bearer {TOKEN}"},
        model="gpt-4-1106",
        # model = "zephyr-7b-beta",
        temperature=1,
        stream=False,
        messages=[{"role": "user", "content": prompt}]
    )

    return chat_completion.choices[0].message.content

# define base prompt
base_prompt = '''Determine if the following abstract of an academic article is linked to aspects related to energy access (including subtopics like energy poverty, access to energy services, rural electrification, electricity access, mini grids, access to clean cooking). 
                Respond only with yes or no and provide further explanation only when choosing no 
                    Here the text:  '''


# Initialize an empty DataFrame for processedappending API responses
topic_classification_df = pd.DataFrame(columns=['EID', 'Prompt', 'Abstract', 'Response'])

# loop over query data and classify each abstract
for i in range(0, len(dat['EID'])):
# for i in range(0, 10):

    # abstract
    temp_abstract = dat.iloc[i, 1]

    # merge to full prompt
    temp_prompt = base_prompt + temp_abstract

    try:

        API_response = run_API_request(temp_prompt)

        if API_response is not None:

            # initiate new line as list
            processed_row = [str(dat.iloc[i, 0]), base_prompt, temp_abstract, API_response]

            # Add the processed row to the processed_df DataFrame
            topic_classification_df.loc[len(topic_classification_df)] = processed_row

            # Optionally, write/update the DataFrame to a CSV file after every row or after a batch of rows
            topic_classification_df.to_csv('topic_classification.csv', index=False)

            # update log
            logging.info(f'Successfully processed row {i} for Publlication {dat.iloc[i, 0]}')

        else:

            # initiate new line as list
            processed_row = [str(dat.iloc[i, 0]), base_prompt, temp_abstract, 'FAILED']

            # Add the processed row to the processed_df DataFrame
            topic_classification_df.loc[len(topic_classification_df)] = processed_row

            # Optionally, write/update the DataFrame to a CSV file after every row or after a batch of rows
            topic_classification_df.to_csv('topic_classification.csv', index=False)

            # update log
            logging.info(f'Failed to processed row {i} for Publlication {dat.iloc[i, 0]}')

    except openai.error.APIError:

        # initiate new line as list
        processed_row = [str(dat.iloc[i, 0]), base_prompt, temp_abstract, 'FAILED']

        # Add the processed row to the processed_df DataFrame
        topic_classification_df.loc[len(topic_classification_df)] = processed_row

        # Optionally, write/update the DataFrame to a CSV file after every row or after a batch of rows
        topic_classification_df.to_csv('topic_classification.csv', index=False)

        # write to log
        logging.info(f'APIError at index: {i} for Publlication {dat.iloc[i, 0]}')

        pass

    except openai.error.Timeout:

        # wait a few second before trying again
        time.sleep(10)

        # try again
        try:

            API_response = run_API_request(temp_prompt)

            if API_response is not None:

                # initiate new line as list
                processed_row = [str(dat.iloc[i, 0]), base_prompt, temp_abstract, API_response]

                # Add the processed row to the processed_df DataFrame
                topic_classification_df.loc[len(topic_classification_df)] = processed_row

                # Optionally, write/update the DataFrame to a CSV file after every row or after a batch of rows
                topic_classification_df.to_csv('topic_classification.csv', index=False)

                # update log
                logging.info(f'Successfully processed row {i} for Publlication {dat.iloc[i, 0]}')

            else:

                # initiate new line as list
                processed_row = [str(dat.iloc[i, 0]), base_prompt, temp_abstract, 'FAILED']

                # Add the processed row to the processed_df DataFrame
                topic_classification_df.loc[len(topic_classification_df)] = processed_row

                # Optionally, write/update the DataFrame to a CSV file after every row or after a batch of rows
                topic_classification_df.to_csv('topic_classification.csv', index=False)

                # update log
                logging.info(f'Failed to processed row {i} for Publlication {dat.iloc[i, 0]}')

        except openai.error.APIError:

            # initiate new line as list
            processed_row = [str(dat.iloc[i, 0]), base_prompt, temp_abstract, 'FAILED']

            # Add the processed row to the processed_df DataFrame
            topic_classification_df.loc[len(topic_classification_df)] = processed_row

            # Optionally, write/update the DataFrame to a CSV file after every row or after a batch of rows
            topic_classification_df.to_csv('topic_classification.csv', index=False)

            # write to log
            logging.info(f'APIError at index: {i} for Publlication {dat.iloc[i, 0]}')

            # continue
            pass

        except openai.error.Timeout:

            # initiate new line as list
            processed_row = [str(dat.iloc[i, 0]), base_prompt, temp_abstract, 'FAILED']

            # Add the processed row to the processed_df DataFrame
            topic_classification_df.loc[len(topic_classification_df)] = processed_row

            # Optionally, write/update the DataFrame to a CSV file after every row or after a batch of rows
            topic_classification_df.to_csv('topic_classification.csv', index=False)

            # write to log
            logging.info(f'TimeoutError at index: {i} for Publication {dat.iloc[i, 0]}')

            # continue
            pass
