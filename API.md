Technical Description
=====================

The key element of datawi.re are frames, which are unmodelled data 
records submitted to the service. Each ``Frame`` also carries some
metadata, such as a ``hash``, ``uuid`` and a ``timestamp``. Frames 
are not stored in the database, but in an external storage service
(e.g. Amazon S3), while only a small reference is kept in the
database. 

Each frame is created by submitting data to an ``Event`` endpoint,
which belongs to a ``Service``. For example, a registration of a new
company could be an event of a company register data service.
``Services`` are to be curated before they become part of the public
firehore and will represent the only point of authorization checks
in the system.

When a ``User`` signs in, they will see an overview of which
``Frames`` match the names of ``Entities`` which they have subscribed
to. ``Entities`` are part of a ``category``, which is either 
Person, Organisation, Place or Topic. We're looking for text/regex
matches only at the moment - more complicated match types can be
implemented via an API, e.g. by using lookups against external services
or by aggregating data to analyse trends. Whenever an ``Entity``
name is found to match a ``Frame``, a ``Match`` is created to store
the connection.

A ``Frame`` is identified by a ``urn`` of the form
``urn:dwre:SERVICE:EVENT:UUID``. This is also the file name stored 
on a remote backend, so that ``Frames`` can be retrieved directly 
(e.g. via S3 CORS).


API thoughts
------------

http://api.datawi.re/

* /1/submit/:service_key/:event_key
* /1/services
* /1/services/:key
* /1/frames
* /1/frames/:urn
* /1/users
* /1/users/:id
* /1/entities
* /1/entities/:id
* /1/matches/:category
* /1/matches/:id
                    
                    
Domain Model
------------

    Service [key, label, ]
        Event [key, label, template, service_id]
        Writer [service_id, user_id]
    User [key, display_name, email, twitter_id, facebook_id, api_key]
        Entity [user_id, category, ]
            Match [entity_id, category, urn, timestamp]
    Frame [urn, hash, created_at]



System Components 
-----------------

* Ingest - just take the inbound frame(s) and queue them.
* Validation and Upload - create database and storage representations, check validity.
* Matcher - find matches for user phrases.
* Searcher
* API
* Frontend