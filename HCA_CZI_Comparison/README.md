# CellxGene_HCA_dataset_comparison
Comparison of datasets hosted on CZI CellXGene and Human Cell Atlas data portal.  

This repository contains the code and final comparison reports between datasets present on CZI CellxGene and Human Cell Atlas Data Portal. Additional details of metadata information present on CZI CellxGene and Human Cell Atlas Data Portal along with the final comparison table can be found [here](https://github.com/cns-iu/hra-cxg-supporting-information/tree/main/HCA_CZI_Comparison/data).


![HCA CXG Pipeline](https://github.com/cns-iu/hra-cxg-supporting-information/blob/main/HCA_CZI_Comparison/readme_images/HCA_CZI.png)

## Setup: 
1. Clone this repository
2. Install the required dependencies listed in the requirements file.
3. Set repository as the current working directory.
4. Run `python main.py` to execute the program. 

- If the HTTP request error arise when the HCA metadata is being fetched, try updating the API version in the config file. The latest API version can be found on the [Data Browser API Specification](https://service.azul.data.humancellatlas.org/)

## Methodology:

### Getting the metadata

#### CZI

- CZI API is used to fetch the metadata with filters applied to get the healthy, adult human cellular data. Multiple fields from the metadata are  extracted for this comparison. The fields that are extracted from the CZI dataset metadata are as follow: 
    - `dataset_id`
    - `dataset_name`
    - `genders`
    - `development_stage`
    - `ethnicity`
    - `cell_type`
    - `cell_type_ontology_id`
    - `organ/tissue`
    - `total_cell_count`
    - `is_primary_data`
    - `disease`
    - `collection_id`
    - `collection_name`

#### HCA 

- HCA Data Browser API is used to fetch the metadata information from the healthy, adult human datasets present on the [HCA DCP 2 portal](https://data.humancellatlas.org/explore/projects). The fields that are extracted from metadata are as follow: 
    - `dataset_id`
    - `dataset_name`
    - `dataset_shortname`
    - `genders`
    - `development_stage`
    - `organs`
    - `organ_cell_count`
    - `cell_count`
    - `disease`
    - `publication_name`
    - `publication_url`

#### Digital Object Identifier (DOI) fetch for comparison.

- The `dataset_name` is used to perform the reverse DOI search. The fields that are included from the DOI reverse search results are as follow:
    - `doi_id`
    - `doi_url`
    - `doi_title`


### Comparing based on common DOI Ids.

- This functionality flags the common datasets across both portal. The comparison key used here is the DOI Id of the corresponding dataset. 
- In the final master table, the `matched at (src, dest)` column contains the source index to destination index mapping in this format : `(src_index, dest_index)`. 

### Possible Extensions / Enhancements

- Compiling a new table that contains the unique datasets using the `matched at (src, dest)` column as reference for filtering out common entries. 
