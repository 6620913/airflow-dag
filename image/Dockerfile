FROM php:7.4-fpm
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libpq-dev \
    libcurl4 \
    libcurl4-openssl-dev \
    zip \
    libzip-dev \
    unzip \
    gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pecl install redis apcu && docker-php-ext-install pdo_mysql pdo_pgsql mbstring exif pcntl bcmath gd opcache zip shmop sysvsem curl && docker-php-ext-enable redis apcu && rm -rf /tmp/pear
# Get latest Composer




# Install the new-relic php agent
ARG NR_INSTALL_SILENT=true

# RUN apt-get update && \
#     DEBIAN_FRONTEND="noninteractive" apt-get install -y nano wget gnupg && \
#     echo 'deb http://apt.newrelic.com/debian/ newrelic non-free' | tee /etc/apt/sources.list.d/newrelic.list && \
#     curl https://download.newrelic.com/548C16BF.gpg | apt-key add - && \
#     apt-get update && \
#     apt-get install -y newrelic-php5 && \
#     newrelic-install install && \
#     sed -i -e s/newrelic.appname[[:space:]]=[[:space:]].\*/newrelic.appname=\${NEW_RELIC_APP_NAME}/ \
#            -e s/newrelic.license[[:space:]]=[[:space:]].\*/newrelic.license=\${NEW_RELIC_LICENSE_KEY}/ /usr/local/etc/php/conf.d/newrelic.ini

RUN curl -L https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash && NEW_RELIC_API_KEY=NRAK-S0GQORVR7YKF424PFHDYQJQZDSI NEW_RELIC_ACCOUNT_ID=4404637 /usr/local/bin/newrelic install -y