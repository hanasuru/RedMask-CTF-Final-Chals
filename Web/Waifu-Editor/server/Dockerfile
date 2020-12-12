from vulhub/imagemagick:7.0.10-36-php

run apt update
run apt install wget -y
run apt install php7.0-dev -y

workdir /var/www/html

run apt install apache2 libapache2-mod-php7.0 curl lynx-cur -y
RUN a2enmod php7.0
RUN a2enmod rewrite

RUN sed -i "s/short_open_tag = Off/short_open_tag = On/" /etc/php/7.0/apache2/php.ini
RUN sed -i "s/error_reporting = .*$/error_reporting = E_ERROR | E_WARNING | E_PARSE/" /etc/php/7.0/apache2/php.ini

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

COPY ./app /var/www/html
COPY ./apache-config.conf /etc/apache2/sites-enabled/000-default.conf

RUN echo redmask{imagetragick_here_we_go_again} > /flag_bendera

RUN chown -R www-data:www-data uploads/
RUN chown root:root uploads/index.html
RUN chown root:root uploads/shell.php
RUN chmod 755 uploads/index.html
RUN chmod 755 uploads/shell.php

RUN rm /bin/grep

CMD /usr/sbin/apache2ctl -D FOREGROUND
