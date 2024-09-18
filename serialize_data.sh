#!/bin/bash
if ls *.json 1> /dev/null 2>&1; then
    rm *.json
fi

patient_info=$(curl "http://127.0.0.1:5000/patients/$1")
patient_id=$(echo "$patient_info" | jq -r '.PatientDetails[0].PatientId')

urls=("/appointments/$patient_id" "/medicalHistory/$patient_id" "/medications/$patient_id" "/patients/insuarance/$patient_id")
main_url="http://127.0.0.1:5000"


handle_error() {
    local exit_code=$1
    local message=$2
    echo "Error: $message"
    exit $exit_code
}

for url in "${urls[@]}";
do
    # req_url="$main_url$url"
    # data=$(curl "$req_url")
    response=$(curl -s "$main_url$url")
    # curl -s "$main_url$url" > "$temp_file"
    if [[ $? -ne 0 ]];
    then
        handle_error 1 "Failed to fetch data from $url"
    fi
    all_responses+=( "$response" )
    key=$(echo "$response" | jq -r 'keys[0]')
    echo "$response" >> "$key.json"
done