datawi.re - a wire service for data
-----------------------------------

The goal of datawi.re is to provide journalists and other researchers with an
easy-to-use way to subscribe to a feed of data records that may be of
interest. To effectively track topics, people, organisations and places of 
interest, datawi.re will help its users to create semantic, structured
watchlists.

Matching records will be sent to users via e-mail and retained on a match list
for later analysis. The service itself will not infinitely store data, i.e. 
the system will not be able to perform aggregate analysis (e.g. trends) itself. 

In many ways, datawi.re is adapting the model of twitter's activity feed,
replacing status updates with data records and the users which you follow 
with your entity watchlist.

Developers will be able to submit data records to datawi.re by specifying 
a service profile, enabling the easy integration with existing scrapers or 
streaming data services. 

Installation
============

*The main instance of datawi.re will be deployed at [http://datawi.re](http://datawi.re) and
accessible to anyone. These instructions are for making a developer 
installation of datawi.re. If you want to set up a production site you'll 
need to tweak these instructions.*

Before installing datawi.re itself, make sure you have the following 
dependencies available on your system (consider using [Vagrant](http://www.vagrantup.com/)
to isolate the project):

* A relational database supported by [SQLAlchemy](http://www.sqlalchemy.org/),
  we recommend using PostgreSQL.
* [RabbitMQ](http://www.rabbitmq.com/) 2.7.1 or newer
* Python 2.7 and [virtualenv](http://www.virtualenv.org/en/latest/)
* Twitter's [bower](https://github.com/bower/bower) for installing JS dependencies.
* [UglifyJS](https://github.com/mishoo/UglifyJS/)
* [SASS](http://sass-lang.com/download.html)

As well as installing these packages, you also need the following services
set up to work with:

* An [Amazon Web Services](http://aws.amazon.com/) account with an access
  key and secret.
* An OAuth-enabled [Twitter](http://dev.twitter.com/) application, created 
  through their developer site. Make sure to configure the callback URL as
  ``http://127.0.0.1:5000/sessions/twitter/callback``.
* A [Facebook](http://facebook.com) app with an app ID and secret.

When you set up datawi.re, first check out the application from GitHub,
create a virtual environment and install the Python dependencies:

	git clone https://github.com/arc64/datawi.re.git
	cd datawi.re
	virtualenv env
	source env/bin/activate
	pip install -r requirements.txt
	
If you're unfamiliar with virtualenv, be aware that you will need to 
execute the ``source env/bin/activate`` command each time you're working with
the project.

Next, you'll need to configure datawi.re. Create a copy of the file ``datawire/default_settings.py``, e.g. as ``settings.py`` in the repository base. Open the 
file and set up the various account configurations. A particularly important 
setting is ``STORE_URL``, as it decides whether data frames will be stored locally
or on Amazon S3:

	# Store data on S3, in the given bucket:
	STORE_URL = 's3://frames.datawi.re/'
	
	# Store data in your back yard:
	STORE_URL = 'file:///var/lib/datawire'
	
Make sure to also set up ``SQLALCHEMY_DATABASE_URI`` to be a valid [connection 
string](http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html).

Once the new configuration is set up, you need to set two environment variables:
the first will point datawi.re at the configuration file, while the second specifies
a secret key to be used by your instance.

	export DATAWIRE_SETTINGS=`pwd`/settings.py
	export DATAWIRE_SECRET="rosebud"
	
Finally, you can create the database schema with the management command:

	python datawire/manage.py createdb
	
For testing purposes, you can also install a sample service like this:

	make service
	
Finally, you can run datawi.re. Be aware that two services need to be alive at any 
time: the web frontend and background processing server. Thus, you'll need two 
terminal windows for development

	# Terminal 1: web service
	python datawire/manage.py runserver 

	# Terminal 2: queue processing
	python datawire/manage.py process
	


License
=======

Copyright (c) 2013, Friedrich Lindenberg, Annabel Church

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
