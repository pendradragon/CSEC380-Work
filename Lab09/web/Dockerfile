FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    apache2 \
    php \
    php-mysql \
    unzip \
    wget \
    mysql-client

WORKDIR /var/www/html

RUN wget https://downloads.sourceforge.net/project/qdpm/qdPM_9.1.zip && \
    unzip qdPM_9.1.zip && \
    mv qdPM_9.1 qdpm && \
    chown -R www-data:www-data qdpm

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
