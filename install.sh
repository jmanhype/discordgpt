#!/bin/bash

# Download and install Go 1.20.6

echo "Downloading Go 1.20.6..."
wget https://dl.google.com/go/go1.20.6.linux-amd64.tar.gz

echo "Extracting the tarball..."
tar -xvf go1.20.6.linux-amd64.tar.gz

echo "Moving Go to /usr/local..."
sudo mv go /usr/local

# Set Go environment variables

echo "Configuring Go environment variables..."

# Add Go binary directory to PATH
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Verify installation

echo "Verifying Go installation..."
go version

echo "Go 1.20.6 has been successfully installed."