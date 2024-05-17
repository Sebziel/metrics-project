#!/bin/bash -xe
apt-get update -y
#Pobieranie i konfiguracja klucza ELK, w celu umożliwienia instalacji poprzez apt
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.x.list
#Update repozytoriów po pobraniuklucza i instalacja elasticsearch'a
apt-get update && apt-get install elasticsearch
#Ustawienie zmiennej IP przy pomocy endpointu meta-data (Potrzebne do automatyzacji na AWS'ie bo ip się co chcwile zmienia)
IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
echo "IP is: $IP"
#Dodanie konfiguracji do Elasticsearcha tak żeby był dostępny publicznie i dziłał w trybie jednego node'a
echo "network.host: $IP" >> /etc/elasticsearch/elasticsearch.yml
echo "node.name: node-1" >> /etc/elasticsearch/elasticsearch.yml
echo "discovery.type: single-node" >> /etc/elasticsearch/elasticsearch.yml
echo "cluster.name: Metrics-project" >> /etc/elasticsearch/elasticsearch.yml
systemctl start elasticsearch.service
#Instalacja kibany
apt-get install kibana
#konfiguracja kibany
echo "server.host: $IP" >> /etc/kibana/kibana.yml
echo "elasticsearch.hosts: http://$IP:9200" >> /etc/kibana/kibana.yml
systemctl start kibana
#Instalacja metricbeata i dodatkowych narzędzi (Nie są niezbędbne, ale można dzięki nim zasymulować np. większe zużycie cpu)
apt-get install metricbeat apt-transport-https python3-pip stress -y
#Konfigurowanie metricbeat'a (Należy wskazać ip kibany (W celu umożliwienia załadowania out-of-the-box dashboard'ów) i elasticsearcha)
sed -i "s/#host: \"localhost:5601\"/host: \"http:\/\/$IP:5601\"/g" /etc/metricbeat/metricbeat.yml
sed -i "s/hosts: \[\"localhost:9200\"\]/hosts: \[\"$IP:9200\"\]/g" /etc/metricbeat/metricbeat.yml
#Wystawione metryki są w data-typie prometheusa, korzystamy więc z wbudowanego modułu prometheus, poniżej go aktywujemy
metricbeat modules enable prometheus
#Konfiguracja modułu prometheusa, wskazujemy ip z którego zaciągamy metryki, domyślnie uderza w endpoint /metrics
sed -i "s/hosts: \[\"localhost:9090\"\]/hosts: \[\"localhost:80\"\]/g" /etc/metricbeat/modules.d/prometheus.yml
systemctl start metricbeat
#Ładujemy domyślne dashboard'y, troche to trwa i musi być uruchomiana kibana, przez co wrzuciłem sleepa, żeby miała wystarczająco czasu, żęby się odpalić. 
echo "Loading Dashboard from metricbeat to kibana"
sleep 15
metricbeat setup --dashboards