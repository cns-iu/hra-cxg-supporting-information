import os
import pandas as pd
from cxg_functions import *
from hca_functions import *
from datetime import datetime


def get_HCA_dataframe():
    # Creates HCA Dataframe.
    hca_data = get_HCA_data()
    hca_df = create_HCA_dataframe(hca_data)
    #print(hca_df)
    return hca_df


def get_CXG_dataframe():
    # Creates CZI CXG dataframe.
    all_collections = fetch_Metadata()
    cxg_df = create_CXG_dataframe(all_collections)
    #print(cxg_df)
    return cxg_df


def compare_CXG_HCA(cxg_df, hca_df):
    master_df = pd.DataFrame(columns=['dataset_id', 'dataset_name', 'Source', 'CZI CellXGene', 'Human Cell Atlas DCP', 'CXG + HCA (BOTH)', 'matched at (src, dest)', 'sex', 'development_stage', 'organs','organ_cell_count', 'total_cell_count', 'disease', 'publication_name / collection_name','doi_title_same_as_dataset_title' , 'doi_id', 'doi_url', 'doi_title' ])
    doi_id_logger = {}
    for i in range(cxg_df.shape[0]):
        doi_id_logger[len(master_df)] = cxg_df.loc[i, 'doi_id']
        master_df.loc[len(master_df)] = [cxg_df.loc[i, 'dataset_id'], cxg_df.loc[i, 'dataset_name'], 'CZI CXG', 1, 0, 'TBD', '', cxg_df.loc[i, 'genders'], cxg_df.loc[i, 'development_stage'], cxg_df.loc[i, 'organ/tissue'],'N/A', cxg_df.loc[i, 'total_cell_count'], cxg_df.loc[i, 'disease'], cxg_df.loc[i, 'collection_name'], cxg_df.loc[i, 'doi_title_is_same_as_dataset_title'], cxg_df.loc[i, 'doi_id'], cxg_df.loc[i, 'doi_url'], cxg_df.loc[i, 'doi_dataset_title']]
    
    for j in range(hca_df.shape[0]):
        total_cell_count = 'N/A'
        if (not None in [next(iter(d.values())) for d in hca_df.loc[j, 'organ_cell_count'] ]):
            ls = [next(iter(d.values())) for d in hca_df.loc[j, 'organ_cell_count']]
            total_cell_count = sum(ls)
        doi_id_logger[len(master_df)] = hca_df.loc[j, 'doi_id']
        master_df.loc[len(master_df)] = [hca_df.loc[j, 'dataset_id'], hca_df.loc[j, 'dataset_name'], 'HCA DCP', 0, 1, 'TBD', '', hca_df.loc[j, 'genders'], hca_df.loc[j, 'development_stage'], hca_df.loc[j, 'organs'],hca_df.loc[j, 'organ_cell_count'], total_cell_count, hca_df.loc[j, 'disease'], hca_df.loc[j, 'publication_name'], hca_df.loc[j, 'doi_title_is_same_as_dataset_title'], hca_df.loc[j, 'doi_id'], hca_df.loc[j, 'doi_url'], hca_df.loc[j, 'doi_dataset_title'] ]
    
    cxg_doi_id_list = cxg_df['doi_id'].tolist()
    hca_doi_id_list = hca_df['doi_id'].tolist()
    for (index, doi_id) in doi_id_logger.items():
        if str(doi_id) in cxg_doi_id_list and str(doi_id) in hca_doi_id_list:
            print('Found DOI at : \t CXG : ', cxg_doi_id_list.index(doi_id), '\tHCA : ', hca_doi_id_list.index(doi_id))
            master_df.loc[index, 'Human Cell Atlas DCP'] = 1
            master_df.loc[index, 'CZI CellXGene'] = 1
            master_df.loc[index, 'CXG + HCA (BOTH)'] = 1
            # (CXG, HCA) 
            src_index, dest_index = 0, 0
            if index < len(cxg_doi_id_list):
                src_index = index 
                # Destination - HCA datasets
                dest_index = hca_doi_id_list.index(doi_id) + len(cxg_doi_id_list)
            else:
                src_index = index
                # Destination - CXG datasets
                dest_index = cxg_doi_id_list.index(doi_id) 
            master_df.loc[index, 'matched at (src, dest)'] = str((src_index, dest_index))
          
        else:
            master_df.loc[index, 'CXG + HCA (BOTH)'] = 0
    print('Summarized the Master dataset successfully.')
    print('Master Dataset : \n')
    print(master_df.head(10))
    return master_df


if __name__ == '__main__':
    date_time = str(datetime.now().year) + '_' + '_'.join(datetime.now().ctime().replace(':','_').split(' ')[1:-1])
    file_location = 'data/'+date_time
    hca_df = get_HCA_dataframe()
    cxg_df = get_CXG_dataframe()
    master_df = compare_CXG_HCA(cxg_df, hca_df)
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        os.makedirs(file_location)
        os.makedirs(file_location + '/csv')
        os.makedirs(file_location + '/excel')

        cxg_df.to_csv(file_location + '/csv/cxg_data.csv', )
        hca_df.to_csv(file_location + '/csv/hca_data.csv', )
        master_df.to_csv(file_location + '/csv/cxg_hca_comparison.csv', )
        cxg_df.to_excel(file_location + '/excel/cxg_data.xlsx', )
        hca_df.to_excel(file_location + '/excel/hca_data.xlsx', )
        master_df.to_excel(file_location + '/excel/cxg_hca_comparison.xlsx',)
        print('\nCreated Tables successfully!')
    except Exception as e:
        print('Exception occured : ', e)

