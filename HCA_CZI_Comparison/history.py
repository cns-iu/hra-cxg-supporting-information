'''
def compare_CXG_HCA_dataframe(cxg_df, hca_df):
    # TODO: Include all dataset. 
    all_datasets = list(set([str(ds_name).lower() for ds_name in cxg_df['doi_id'].tolist()]).union([str(ds_name).lower() for ds_name in hca_df['doi_id'].tolist()]))
    master_df = pd.DataFrame(columns=['dataset_id', 'dataset_name', 'sex', 'development_stage', 'organs','organ_cell_count', 'total_cell_count', 'disease', 'publication_name / collection_name','doi_title_is_same_as_dataset_title' , 'doi_id', 'doi_url', 'doi_title' ])
    for i in range(cxg_df.shape[0]):
        if (cxg_df.loc[i, 'doi_id'].lower() in all_datasets):
            master_df.loc[len(master_df)] = [cxg_df.loc[i, 'dataset_id'], cxg_df.loc[i, 'dataset_name'], cxg_df.loc[i, 'genders'], cxg_df.loc[i, 'development_stage'], cxg_df.loc[i, 'organ/tissue'],'N/A', cxg_df.loc[i, 'total_cell_count'], cxg_df.loc[i, 'disease'], cxg_df.loc[i, 'collection_name'], cxg_df.loc[i, 'doi_title_is_same_as_dataset_title'], cxg_df.loc[i, 'doi_id'], cxg_df.loc[i, 'doi_url'], cxg_df.loc[i, 'doi_dataset_title']]
            all_datasets.remove(str(cxg_df.loc[i, 'doi_id']).lower())
            
    for j in range(hca_df.shape[0]):
        if (hca_df.loc[j, 'doi_id'].lower() in all_datasets):
            total_cell_count = 'N/A'
            if (not None in [next(iter(d.values())) for d in hca_df.loc[j, 'organ_cell_count'] ]):
                ls = [next(iter(d.values())) for d in hca_df.loc[j, 'organ_cell_count']]
                total_cell_count = sum(ls)
            master_df.loc[len(master_df)] = [hca_df.loc[j, 'dataset_id'], hca_df.loc[j, 'dataset_name'], hca_df.loc[j, 'genders'], hca_df.loc[j, 'development_stage'], hca_df.loc[j, 'organs'],hca_df.loc[j, 'organ_cell_count'], total_cell_count, hca_df.loc[j, 'disease'], hca_df.loc[j, 'publication_name'], hca_df.loc[i, 'doi_title_is_same_as_dataset_title'], hca_df.loc[i, 'doi_id'], hca_df.loc[i, 'doi_url'], hca_df.loc[i, 'doi_dataset_title'] ]
            all_datasets.remove(str(hca_df.loc[j, 'doi_id']).lower())
    master_df = label_dataset_columns(master_df, cxg_df, hca_df)
    print(master_df )
    return master_df


def label_dataset_columns(master_df, cxg_df, hca_df):
    """
    ()
    """
    lower_hca_list = [ds_name.lower() for ds_name in hca_df.loc[:,'doi_id']]
    lower_cxg_list = [ds_name.lower() for ds_name in cxg_df.loc[:,'doi_id']]
    for i in range(master_df.shape[0]):
        doi_id = str(master_df.loc[i, 'doi_id']).lower()
        master_df.loc[i, 'HCA + CellXGene'] = 1 if ((doi_id in lower_cxg_list) and (doi_id in lower_hca_list)) else 0
        master_df.loc[i, 'HCA portal'] = 1 if (doi_id in lower_hca_list) else 0
        master_df.loc[i, 'CellXGene portal'] = 1 if (doi_id in lower_cxg_list) else 0
    master_df['CellXGene portal'] = master_df['CellXGene portal'].astype(int)
    master_df['HCA portal'] = master_df['HCA portal'].astype(int)
    master_df['HCA + CellXGene'] = master_df['HCA + CellXGene'].astype(int)
    
    master_df.insert(2, 'CellXGene portal', master_df.pop('CellXGene portal'))
    master_df.insert(3, 'HCA portal', master_df.pop('HCA portal'))
    master_df.insert(4, 'HCA + CellXGene', master_df.pop('HCA + CellXGene'))
    return master_df
'''
