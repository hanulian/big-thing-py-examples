#!/bin/bash

check_signature_support() {
  if command -v apt > /dev/null 2>&1; then
    apt-key list > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
      echo 1
    else
      echo 0
    fi
  fi
}

check_apt_key_support() {
  if command -v apt-key > /dev/null 2>&1; then
    apt-key -h | grep -- --keyring > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
      echo 1
    else
      echo 2
    fi
  else
    if command -v apt-get > /dev/null 2>&1; then
      apt_version=$(apt-get --version | head -n 1 | awk '{print $3}')
      if [[ $apt_version == 2.* ]]; then
        echo 3
      else
        echo 2
      fi
    else
      echo 2
    fi
  fi
}

check_gcloud_account_set() {
  if [[ ! -z $(gcloud auth list 2>&1 | grep 'No credentialed accounts.') ]]; then
    echo 0
  else
    echo 1
  fi
}

check_gcloud_project_set() {
  if [[ ! -z $(gcloud config get-value project 2>&1 | grep '(unset)') ]]; then
    echo 0
  else
    echo 1
  fi
}

check_gcloud_project_exist() {
  project_name=$1

  if [[ ! -z $(gcloud projects list 2>&1 | grep $project_name) ]]; then
    echo 1
  else
    echo 0
  fi
}

check_adc_set() {
  if [[ ! -z $(gcloud auth application-default print-access-token 2>&1 | grep 'ERROR: (gcloud.auth.application-default.print-access-token) Your default credentials were not found.') ]]; then
    echo 0
  else
    echo 1
  fi
}

check_vision_api_enabled() {
  if [[ ! -z $(gcloud services list | grep 'vision.googleapis.com') ]]; then
    echo 1
  else
    echo 0
  fi
}

install_gcloud() {
  sudo apt-get update
  sudo apt-get install apt-transport-https ca-certificates gnupg curl sudo -y

  if [[ $(check_signature_support) == 1 ]]; then
    echo "signature_support enabled"
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
  else
    echo "signature_support disabled"
    echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
  fi

  gpg_key_url="https://packages.cloud.google.com/apt/doc/apt-key.gpg"
  if [[ $(check_apt_key_support) == 1 ]]; then
    echo "apt-key support enabled. check_apt_key_support == 1"
    curl $gpg_key_url | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
  elif [[ $(check_apt_key_support) == 2 ]]; then
    echo "apt-key support enabled. check_apt_key_support == 2"
    curl $gpg_key_url | sudo apt-key add -
  elif [[ $(check_apt_key_support) == 3 ]]; then
    echo "apt-key support enabled. check_apt_key_support == 3"
    curl $gpg_key_url | sudo tee /usr/share/keyrings/cloud.google.gpg
  else
    echo "apt-key support check failed"
  fi

  sudo apt-get update && sudo apt-get install google-cloud-cli -y
}

command -v gcloud > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
  echo "gcloud command not found. Install Google Cloud SDK..."

  install_gcloud
else
  echo "gcloud already installed."
fi

if [[ $(check_gcloud_account_set) == 0 ]]; then
  gcloud auth login
fi

if [[ $(check_gcloud_project_set) == 0 ]]; then
  if [[ $(check_gcloud_project_exist test-vision-api-app) == 0 ]]; then
    gcloud projects create test-vision-api-app
  else
    gcloud config set project test-vision-api-app
  fi
fi

if [[ $(check_vision_api_enabled) == 0 ]]; then
  gcloud services enable vision.googleapis.com
fi

if [[ $(check_adc_set) == 0 ]]; then
  gcloud auth application-default login
fi

pip install -r requirements.txt
