# Elasticsearch + Kibana + Metricbeat Demo Project

This project serves as a demo of an Elasticsearch + Kibana + metricbeat solution. Metricbeat gathers prometheus-like data from a Python HTTP server that produces fake data in prometheus format.

## Infrastructure

By default, AWS CloudFormation (CF) is used as the infrastructure. It consists only of an EC2 Ubuntu server and a security group to open ports allowing access from the public internet.

## Installation

The script for installation used in AWS CF is described in more detail in the `tools.sh` file. It shows the overall idea of what needs to be done in order to set up this solution. 

**Note:** There are a few adjustments required in case AWS is not in use - specifically, the IP of the instance has to be changed in the Elasticsearch and Kibana config files.

## Examples and Configuration

- `metric_examples` directory contains files with examples of what the data looks like served from the Python HTTP server. 

- `yamls` directory contains default metricbeat and prometheusModule files, along with adjusted versions to showcase which parts of the configuration require changes.

## Results

An expected outcome is default server metrics, along with kibana dashbaords out-of-the-box and random values of metrics genereted by python http server. 
