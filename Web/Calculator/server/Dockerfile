FROM ubuntu:latest

USER root

run apt update
run apt install wget -y
run apt install php7.4-cli -y

workdir /var/www/html

run apt install apache2 libapache2-mod-php7.4 curl -y
run apt install sendmail -y
RUN a2enmod php7.4
RUN a2enmod rewrite

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

COPY ./flag.o /execute_me_to_get_flag
RUN chown root:root /execute_me_to_get_flag
RUN chmod +x /execute_me_to_get_flag
RUN chmod 511 /execute_me_to_get_flag

RUN apt update
RUN apt install sendmail -y
RUN apt install cron -y

# Copy cron file to the cron.d directory
COPY cron /etc/cron.d/rm-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/rm-cron

# Apply cron job
RUN crontab /etc/cron.d/rm-cron

RUN groupadd -g 999 www
RUN useradd -u 999 -ms /bin/bash -g www www

# Copy existing application directory contents
COPY ./vhost.conf /etc/apache2/sites-available/000-default.conf

copy ./entrypoint.sh /entrypoint.sh
entrypoint "/entrypoint.sh"