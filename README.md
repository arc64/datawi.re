
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






Older explanation
=================

Optional: talk to some journalists. 

What tasks would this help with? 

* Keeping an eye on...
*  ... parliaments, 
*  ... procurement, 
*  ... grants,
*  ... air traffic, 
*  ... scientific research publications, 
*  ... patent applications,
*  ... crime and punishment,
*  ... obituaries,
*  ... gas prices,
*  ... movie release dates,
*  ... the sky,
*  ... the volcano,
*  ... lobbyists signing up to a register,
*  ... company statements coming out,
*  ... changes in company ownership,
*  ... local elections,
*  ... food prices, commodity prices, harvests.


Explain it to me, I'm a normal person: I want to be able to reduce the amount of manual labour
in keeping track of developments in different areas of expertise. I don't want to look at
that PDF every week. I don't want to waste hours in a week checking this data against that data.

Explain it to me, I'm a developer: You can create a feed service and push messages to the 
service. Messages have a metadata envelope and the actual data contained within a record
of the data source that you're providing. 

You can also write processing stages, such as geo-coders, company register lookups, 
value normalisation or named entity extraction. 

Even more, you can code event handlers which get triggered by matching filters and then 
take some action, such as notifying a user via email, a text message or by sending an 
automated killer drone which then eradicates a medium-sized village. We're hoping for 
good data quality on the last one. 


Revised pitch
-------------

* datawi.re is a streaming service for monitoring misc data feeds.
* datawi.re is just another thing you connect your scrapers to, allows for quick and simple submission of a data frame. 
* datawi.re has a twitter-like UI. each service defines a template with which a data frame is rendered.
* instead of following a user or a hashtag, you follow search terms by adding them to one of your four watchlists.









