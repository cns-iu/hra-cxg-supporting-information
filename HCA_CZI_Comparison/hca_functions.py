import json
import requests
from tqdm import tqdm
import pandas as pd
from doi_api_functions import *
from config import *


def query_HCA(query, filter={}):
    '''
    Function to query the HCA data portal Azul API
    '''
    endpoint_url = f'https://service.azul.data.humancellatlas.org' + query
    parameters = {'catalog': catalog}
    if filter:
        parameters['filters'] = json.dumps(filter)
    response = requests.get(endpoint_url, params=parameters)
    response.raise_for_status()
    data = response.json()
    return data


def get_metadata(data):
    metadata = {}
    metadata['projectId'] = data['projects'][0]['projectId']
    metadata['projectTitle'] = data['projects'][0]['projectTitle']
    metadata['projectDescription'] = data['projects'][0]['projectDescription']
    metadata['projectShortname'] = data['projects'][0]['projectShortname']
    metadata['donors'] = [{'biologicalSex': donor['biologicalSex'], 'developmentStage': donor['developmentStage'],
                           'disease': donor['disease']} for donor in data['donorOrganisms']]
    metadata['publications'] = [{'publicationTitle': publication['publicationTitle'],
                                 'publicationUrl':  publication['publicationUrl']} for publication in data['projects'][0]['publications']]
    metadata['organ_cell_count'] = [
        {organ['organ'][0]: organ['totalCells']} for organ in data['cellSuspensions']]
    metadata['doi_data'] = get_doi_data(data['projects'][0]['projectTitle'])
    metadata['cell_count'] = data['projects'][0]['estimatedCellCount']
    return metadata


def create_HCA_dataframe(hca_data):
    hca_df = pd.DataFrame(columns=['dataset_id', 'dataset_name',  'dataset_shortname', 'genders',
                          'development_stage', 'organs', 'organ_cell_count', 'cell_count','doi_title_is_same_as_dataset_title', 
                          'doi_id', 'doi_url', 'doi_dataset_title', 'disease', 'publication_name', 'publication_url'])
    for key in hca_data.keys():
        dataset_id = hca_data[key]['projectId']
        dataset_name = hca_data[key]['projectTitle']
        cell_count = hca_data[key]['cell_count']
        dataset_shortname = hca_data[key]['projectShortname']
        genders = " | ".join(hca_data[key]['donors'][0]['biologicalSex'])
        development_stage = " | ".join(
            hca_data[key]['donors'][0]['developmentStage'])
        disease = 'N/A'
        doi_data = hca_data[key]['doi_data']
        doi_title_is_same_as_dataset_title = doi_data['title_is_same']
        doi_id = doi_data['doi']
        doi_url = doi_data['url']
        doi_title = doi_data['title']
        
        try:
            disease = " | ".join(hca_data[key]['donors'][0]['disease'])
        except:
            pass
        organ_cell_count = hca_data[key]['organ_cell_count']
        ls = [next(iter(d.keys())) for d in hca_data[key]['organ_cell_count']]
        organs = 'N/A'
        if not None in ls:
            organs = (" | ".join(ls))
        try:
            publication_name = hca_data[key]['publications'][0]['publicationTitle']
            publication_url = hca_data[key]['publications'][0]['publicationUrl']
        except:
            publication_name = 'N/A'
            publication_url = 'N/A'
        hca_df.loc[len(hca_df)] = [dataset_id,  dataset_name,  dataset_shortname, genders,
                                   development_stage, organs, organ_cell_count, cell_count, doi_title_is_same_as_dataset_title, doi_id, doi_url, doi_title, disease, publication_name, publication_url]
    return hca_df


def refetch_hca_dataset(dataset_fetch_error, hca_data, retry=3):
    '''
    Refetch strategy for acquiring the metadata (HCA).
    
    History: 
    The Azul API sometimes fails to fetch the requested dataset. 
    The retry attempt is made 3 times to ensure that the dataset
    metadata is fetched. 
    '''
    dfe = []        
    print(f'\nRetry Attempts Left : {(retry-1)} \tFetching HCA datasets : {len(dataset_fetch_error)} \n {dataset_fetch_error} \n')
    for pid in tqdm(dataset_fetch_error, desc='Refetching missed HCA DCP datasets :'):
        query = '/index/projects/' + pid
        try:
            dataJ = query_HCA(query)
            metadata = get_metadata(dataJ)
            hca_data[pid] = metadata
        except Exception as e:
            print(f'Error refetching data : {e}')
            dfe.append(str(e).split('/')[-1].split('?')[0])
    if len(dfe) > 0 and retry > 0:
        hca_data = refetch_hca_dataset(dfe, hca_data, retry-1)
    return hca_data


def get_HCA_data():
    '''
    API calls to fetch the dataset metadata information from HCA portal. 
    '''
    query = '/index/files'
    filter = {"genusSpecies": {"is": ["Homo sapiens", "Homo Sapiens"]}, "donorDisease": {
        "is": ["normal"]}, "specimenDisease": {"is": ["normal"]}, "donorDisease": {"is": ["normal"]}}
    data = query_HCA(query, filter)
    project_ids = []
    project_ids = [pid['projectId'][0] for pid in data['termFacets']
                   ['project']['terms'] if pid not in project_ids]
    hca_data = {}
    dataset_fetch_error = []
    for num, pid in enumerate(tqdm(project_ids, desc='Fetching HCA DCP datasets: ', )):
        query = '/index/projects/' + pid
        try:
            dataJ = query_HCA(query)
            metadata = get_metadata(dataJ)
            hca_data[pid] = metadata
            #print('HCA DCP Dataset Fetched and Ingested : ', len(hca_data))
        except Exception as e:
            print('Error getting data : ', e)
            dataset_fetch_error.append(str(e).split('/')[-1].split('?')[0])
    print(f'Dataset fetch error for these datasets : {len(dataset_fetch_error)} \n {dataset_fetch_error}')
    if(len(dataset_fetch_error) > 0):
        print('Refetching...\n')
        hca_data = refetch_hca_dataset(dataset_fetch_error, hca_data) 

    print('Summarized HCA datasets successfully.')
    return hca_data
