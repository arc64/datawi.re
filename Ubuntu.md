

apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C7917B12 
apt-get update 
apt-get dist-upgrade
apt-get install git python-virtualenv libxslt-dev rabbitmq-server nginx supervisor postgresql-9.1-postgis 
apt-get install nodejs

npm install -g bower

pip install -e git+https://github.com/arc64/datawi.re.git#egg=datawire

apt-get install ruby-sass
npm install -g uglify-js