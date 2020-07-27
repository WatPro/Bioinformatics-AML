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

folder_data='03clinicalData/'
download_filename='gdc_download.tar.gz'
tar --extract --file="${folder_working}${download_filename}" --directory="${folder_data}"
 

```

## Common Data Element Dictionary

```bash
folder_data='03clinicalData/'
folder_processed='05datalist/'

ls ${folder_data}*/*.xml |
  python3 "${folder_processed}/script_extract_data.py" > "${folder_processed}list_extract_data.tsv"

cat "${folder_processed}list_extract_data.tsv" | 
  sed '1d' |
  awk 'BEGIN{FS=OFS="\t"} {second=sub(/.*:/,"",$2);print $4,$5}' |
  sort --numeric-sort --field-separator=$'\t' |
  uniq > "${folder_processed}list_cde_version.tsv"

api_cdelink='https://cdebrowser.nci.nih.gov/cdebrowserServer/rest/CDELink?publicId=__cde__&version=__cdever__'
cat "${folder_processed}list_cde_version.tsv" |
  awk 'BEGIN{FS=OFS="\t"} {if($1!=""){if($2==""){$2="1.0"};print $1,$2;}}' |
  while read -r line 
  do
    cde="${line%$'\t'*}"
    cdever="${line#*$'\t'}"
    api_query="${api_cdelink/__cde__/$cde}"
    api_query="${api_query/__cdever__/$cdever}"
    jsonpath="${folder_processed}publicId_${cde}_${cdever}.json"
    curl --output "${jsonpath}" "${api_query}"
  done 

api_search='https://cdebrowser.nci.nih.gov/cdebrowserServer/rest/search?publicId=__cde__'
cat "${folder_processed}list_cde_version.tsv" | 
  cut --delimiter=$'\t' --fields=1 | 
  sed '/^$/d' | 
  sort --numeric-sort | uniq | 
  while read -r line 
  do
    api_query="${api_search/__cde__/$line}"
    jsonpath="${folder_processed}search_${line}.json"
    curl --output "${jsonpath}" "${api_query}"
  done 

api_cdedata='https://cdebrowser.nci.nih.gov/cdebrowserServer/rest/CDEData?deIdseq=__deIdseq__'
ls ${folder_processed}search_*.json |
  while read -r line 
  do
    cde="${line##*search_}"
    cde="${cde%.json}"
    deidseq=`sed --silent 's/^.*"deIdseq":"\([^"]*\)".*$/\1/p' "${line}" | head --lines=1`
    echo -e "${cde}\t${deidseq}"
  done | 
  sed --silent '/^\S\+\t\S\+$/p' |
  sort --numeric-sort --key=1 |
  while read -r line
  do
    cde="${line%$'\t'*}"
    deidseq="${line#*$'\t'}"
    api_query="${api_cdedata/__deIdseq__/$deidseq}"
    jsonpath="${folder_processed}deIdseq_${deidseq}_${cde}.json"
    curl --output "${jsonpath}" "${api_query}"
  done 

ls ${folder_processed}*.json |
  while read -r line 
  do
    echo ${line##*/}$'\t'${line}
  done | 
  sed --silent '/^\(deIdseq_\|publicId_\)/p' |
  sort | 
  cut --delimiter=$'\t' --fields=2 | 
  while read -r line 
  do
    cde='00000000'`python3 "${folder_processed}script_get_id_from_json.py" "${line}"`
    cde="${cde: -8}"
    if [ "${cde}" = '00000000' ] 
    then
      continue
    fi
    filename="CommonDataElement_${cde}.json"
    python3 "${folder_processed}script_get_pretty_json.py" "${line}" > "${folder_processed}${filename}"
  done

ls ${folder_processed}CommonDataElement_*.json |
  python3 "${folder_processed}script_get_definition.py" > "${folder_processed}list_dictionary.tsv"
 

```

