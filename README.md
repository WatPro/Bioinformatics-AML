# Bioinformatics-AML
Note: AML is NOT for Anti-Money Laundering

## Download Clinical Data

```bash
folder_working='01downloadClinicalData/'

api_file='https://api.gdc.cancer.gov/files'
curl --request POST --header "Content-Type: application/json" --data "@${folder_working}search_payload_full.json" "${api_file}" > "${folder_working}response_list_full.json"
curl --request POST --header "Content-Type: application/json" --data "@${folder_working}search_payload.json"      "${api_file}" > "${folder_working}response_list.json"

python3 "${folder_working}script_payload_gen_bulk.py" "${folder_working}response_list.json" > "${folder_working}download_payload_bulk.json"

download_filename='gdc_download.tar.gz'
api_data='https://api.gdc.cancer.gov/data/'
curl --output "${folder_working}${download_filename}" --request POST --header 'Content-Type: application/json' --data @"${folder_working}download_payload_bulk.json" "${api_data}"

```

