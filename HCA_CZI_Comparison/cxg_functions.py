from numpy import product
from requests.adapters import HTTPAdapter
#import datetime
from tqdm import tqdm
import requests
import pandas as pd
import json
from doi_api_functions import *


def fetch_Metadata():
    print('Fetching Data...')
    adapter = HTTPAdapter(max_retries=3)  # Hard-coded 3 Max Retries
    https = requests.Session()
    https.mount("https://", adapter)
    CELLXGENE_PRODUCTION_ENDPOINT = 'https://api.cellxgene.cziscience.com'
    COLLECTIONS = CELLXGENE_PRODUCTION_ENDPOINT + "/dp/v1/collections/"
    DATASETS = CELLXGENE_PRODUCTION_ENDPOINT + "/dp/v1/datasets/"
    r = https.get(COLLECTIONS)
    collections = sorted(
        r.json()['collections'], key=lambda key: key['created_at'], reverse=True)

    all_collections = []
    print('Total Collections on CellxGene : ', len(collections))
    for collection in collections:
        r1 = https.get(COLLECTIONS + collection['id'], timeout=5)
        collection_metadata = r1.json()
        all_collections.append(collection_metadata)
    print('Data Fetch Complete.')
    return all_collections


def getinformation(dataset, collection):
    dataset_id = dataset['id']
    dataset_name = dataset['name']
    genders = ' | '.join([sex['label'] for sex in dataset['sex']])
    development_stage = ' | '.join([stage['label']
                                   for stage in dataset['development_stage']])

    tissue = ' | '.join([tissue['label'] for tissue in dataset['tissue']])
    disease = ' | '.join([disease['label'] for disease in dataset['disease']])
    ethnicity = ' | '.join([ethnicity['label']
                           for ethnicity in dataset['ethnicity']])

    total_cell_count = 'N/A'
    cell_type = 'N/A'
    cell_type_ontology_id = 'N/A'
    collection_name = collection['name']

    doi_data = get_doi_data(dataset_name)
    doi_title_is_same_as_dataset_title = doi_data['title_is_same']
    doi_id = doi_data['doi']
    doi_url = doi_data['url']
    doi_title = doi_data['title']
    is_primary_data = dataset['is_primary_data']

    if 'cell_count' in dataset.keys():
        total_cell_count = dataset['cell_count']
    if 'cell_type' in dataset.keys():
        cell_type = ' | '.join([ct['label'] for ct in dataset['cell_type']])
        cell_type_ontology_id = ' | '.join(
            [ct['ontology_term_id'] for ct in dataset['cell_type']])
    collection_id = dataset['collection_id']

    return [dataset_id, dataset_name, genders, development_stage, ethnicity, cell_type, cell_type_ontology_id, tissue, total_cell_count, doi_title_is_same_as_dataset_title, doi_id, doi_url, doi_title, is_primary_data, disease, collection_id, collection_name]


def create_CXG_dataframe(all_collections):
    cxg_df = pd.DataFrame(columns=['dataset_id',  'dataset_name', 'genders', 'development_stage', 'ethnicity', 'cell_type',
                          'cell_type_ontology_id', 'organ/tissue', 'total_cell_count', 'doi_title_is_same_as_dataset_title', 
                          'doi_id', 'doi_url', 'doi_dataset_title', 'is_primary_data', 'disease', 'collection_id', 'collection_name'])
    only_normal_homo_sapiens_ids = []
    only_normal = []
    only_homo_sapiens = []
    cnt = 0
    total_ds = 0
    for metadata in tqdm(all_collections, desc='Fetching CZI CXG datasets: '):
        try: 
            collection_cell_counter = 0
            for dataset in metadata['datasets']:
                total_ds += 1
                diseases = dataset['disease']
                id = dataset['id']
                for disease in diseases:
                    if (str(disease['label']).lower() == 'normal'):
                        only_normal.append(id)
                    if (str(dataset['organism'][0]['label']).lower() == 'homo sapiens'):
                        only_homo_sapiens.append(id)
                    if (str(disease['label']).lower() == 'normal' and str(dataset['organism'][0]['label']).lower() == 'homo sapiens'):
                        cxg_df.loc[len(cxg_df)] = getinformation(dataset, metadata)
                        try:
                            collection_cell_counter += dataset['cell_count']
                        except Exception as e:
                            print('Exception : ', e)
                        only_normal_homo_sapiens_ids.append(id)
                        cnt += 1
        except Exception as e:
            print('Error occured : ', e)
    print('Summary : ')
    print('\nOnly Normal + Homo Sapiens datasets : ',
          len(only_normal_homo_sapiens_ids))
    print('Only Normal datasets : ', len(only_normal))
    print('Only Homo Sapiens datasets : ', len(only_homo_sapiens))
    print('Total DS  :', total_ds, '\nCount :', cnt)
    print('\nSummarized CXG datasets successfully.')
    return cxg_df
