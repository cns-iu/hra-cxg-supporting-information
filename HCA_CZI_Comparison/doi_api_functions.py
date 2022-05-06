import requests


def get_doi_data(dataset_name: str):
    """
    API calls to perform a reverse DOI search to identify the study/paper/publication
    that the dataset belongs to and fetch the information to be included in the table. 

    """

    parameters = {'rows': 5, 'query.title': dataset_name}
    endpoint_url = f'https://api.crossref.org/works'
    response = requests.get(endpoint_url, params=parameters)
    title_is_same = False
    try:
        response.raise_for_status()
        response_json = response.json()
        title_is_same = True if response_json['message']['items'][0]['title'][0].strip(
            '.').lower() == dataset_name.strip('.').lower() else False
    except Exception as e:
        print('Error : ', e)

    doi_data = {
        'doi': response_json['message']['items'][0]['DOI'],
        'dataset_name': dataset_name,
        'title': response_json['message']['items'][0]['title'][0],
        'url': response_json['message']['items'][0]['URL'],
        'title_is_same': title_is_same
    }

    return doi_data
