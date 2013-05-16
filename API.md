

http://api.datawi.re/
                    /1/submit/<service>/<event>
                    /1/services
                    /1/services/<service>
                    /1/frames
                    /1/frames/<urn>
                    /1/users
                    /1/users/<id>
                    /1/entities
                    /1/watchlists/<id>
                    /1/watchlists/<id>/entries
                    /1/search


Domain Model

    Service [key, label, ]
        Event [key, label, template, service_id]
        Writer [service_id, user_id]
    User [key, display_name, email, twitter_id, facebook_id, api_key]
        Entity [user_id, category, ]
            Match [entity_id, category, urn, timestamp]
    Frame [urn, hash, created_at]



Components: 

    * Ingest
    * Upload
    * Matcher
    * Searcher
    * API
    * Frontend