#!/bin/bash

########################################################################################
# Setup project from template: Guide user through setup
# Change all occurences of project-name and user-name in file content and names
########################################################################################
set +e
echo "Setting up your project from the template (press ctrl + c to cancel at any point)"

export PYTHON_VERSION="3.9.18"
export RYE_VERSION="0.26.0"
export TFLINT_VERSION="v0.48.0"
export TERRAFORM_VERSION="1.5.7"
export GO_VERSION="1.20.11"
export RYE_TOOLCHAIN=$PYTHON_VERSION

while true; do
  read -p "Do you want to start the project setup? (y/n) " yn
  case $yn in
    [yY] ) echo "Ok. Starting setup."
      break;;
    [nN] ) echo "Exiting...";
      exit;;
    * ) echo "Error: invalid response. Please try again";;
  esac
done
echo ""

echo "Checking for Rye"
sleep 0.5s
if ! hash rye &> /dev/null; then
    echo "Error: Rye could not ne found. Installing it."
    curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash
    source "$HOME/.rye/env"
fi
echo "Ok: Rye found"
echo ""


echo "Checking for unzip"
sleep 0.5s
if ! hash unzip &> /dev/null; then
    echo "Error: unzip command not found. Installing it."
    sudo apt-get -qq update && sudo apt-get -qq --yes install unzip
fi
echo "Ok: unzip command found"
echo ""


echo "Checking for tflint"
sleep 0.5s
if ! hash tflint &> /dev/null; then
    echo "Error: tflint command not found."
    echo "Installing tflint"
    curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh  | bash
fi
echo "Ok: tflint command found"
echo ""


echo "Checking for go"
sleep 0.5s
if ! command go version &> /dev/null
then
    echo "Error: go could not be found. You will need to enter your sudo password!"
    echo "Installing go:"
    wget -O go.tar.gz https://dl.google.com/go/go${GO_VERSION}.linux-amd64.tar.gz
    sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go.tar.gz && rm go.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
    go version
fi
echo "Ok: go command found"
echo ""


echo "Checking for terraform"
sleep 0.5s
if ! hash terraform &> /dev/null; then
    echo "Error: terraform command not found."
    echo "Installing terraform"
    wget -O terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
    unzip -o terraform.zip
    rm terraform.zip
    sudo cp terraform /usr/bin
    rm terraform
fi
echo "Ok: terraform command found"
echo ""


echo "Setting up current folder with Rye for project: $PROJECT"
rye pin ${PYTHON_VERSION}
rye sync --no-lock


echo "Installing pre-commit hooks into git. Running pre-commit install:"
sleep 0.5s
rye run pre-commit install
echo ""


echo "#################################################################################"
echo "# Automatic Project Setup completed. Now, make sure to read the README.md"
echo "#################################################################################"
echo ""
