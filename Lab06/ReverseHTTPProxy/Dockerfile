FROM httpd:2.4

#Enables the required modules
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/* 
RUN sed -i 's/^#Include conf\/extra\/httpd-ssl.conf/Include conf\/extra\/httpd-ssl.conf/' /usr/local/apache2/conf/httpd.conf
RUN echo "LoadModule proxy_http_module modules/mod_proxy_http.so" >> /usr/local/apache2/conf/httpd.conf \
  && echo "LoadModule proxy_http_module modules/mod_proxy_http.so" >> /usr/local/apache2/conf/httpd.conf \
  && echo "LoadMoule ssl_module modules/ssl_ssl.so" >> /usr/local/apache2/conf/httpd.conf

#Copies the configuration and SSL certs located in .ssl
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ssl/ /usr/local/apache2/conf/ssl
