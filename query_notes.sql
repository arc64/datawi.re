CREATE INDEX entity_user_id ON entity (user_id);
CREATE INDEX entity_id_user_id ON entity (id, user_id);

CREATE INDEX match_urn ON match (urn);

CREATE INDEX match_entity_id ON match (entity_id);
CREATE INDEX match_urn ON match (urn);
CREATE INDEX frame_urn ON frame (urn);


SELECT entity.id AS entity_id, entity.text AS entity_text, count(match.id) AS count_1 
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN frame ON frame.urn = match.urn
    LEFT JOIN match AS match_1 ON frame.urn = match_1.urn 
    
    WHERE entity.user_id = 2 AND (match_1.entity_id IN (3) OR match_1.entity_id IS NULL)
    GROUP BY entity.id, entity.created_at, entity.updated_at, entity.text, entity.facet, entity.user_id
    ORDER BY count(match.id) DESC, entity.text ASC;


SELECT match.entity_id, match.urn FROM match WHERE (entity_id IN (3) OR entity_id IS NULL);


SELECT entity.id AS entity_id, entity.text AS entity_text, COUNT(DISTINCT(match_1.urn)) AS count_1 
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN frame ON frame.urn = match.urn
    LEFT JOIN match AS match_1 ON frame.urn = match_1.urn 
    LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id
    WHERE entity.user_id = 2
        AND (match_1.entity_id IN (3) OR match_1.entity_id IS NULL)
        AND (entity_1.user_id = 2 OR entity_1.user_id IS NULL)
    GROUP BY entity.id, entity.text
    ORDER BY count(distinct(match_1.urn)) DESC, entity.text ASC;


SELECT entity.id AS entity_id, entity.text AS entity_text, COUNT(DISTINCT(match_1.urn)) AS count_1 
    FROM entity 
    LEFT OUTER JOIN match ON entity.id = match.entity_id
    LEFT OUTER JOIN frame ON frame.urn = match.urn
    LEFT OUTER JOIN match AS match_1 ON frame.urn = match_1.urn 
    LEFT OUTER JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id
    WHERE entity.user_id = 2
        AND (entity_1.user_id = 2 OR entity_1.user_id IS NULL)
    GROUP BY entity.id, entity.text
    ORDER BY count(distinct(match_1.urn)) DESC, entity.text ASC;


SELECT entity.id AS entity_id, entity.created_at AS entity_created_at, entity.updated_at AS entity_updated_at,
    entity.text AS entity_text, entity.category AS entity_category, entity.user_id AS entity_user_id, count(distinct(match.urn)) AS count_1 
FROM entity LEFT OUTER JOIN match ON entity.id = match.entity_id LEFT OUTER JOIN frame ON frame.urn = match.urn LEFT OUTER JOIN match AS match_1 ON frame.urn = match_1.urn LEFT OUTER JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id 
WHERE entity.user_id = 2 AND (entity_1.user_id = 2 OR entity_1.user_id IS NULL) AND (match_1.entity_id IN (4, 3) OR match_1.entity_id IS NULL) GROUP BY entity.id, entity.created_at, entity.updated_at, entity.text, entity.category, entity.user_id ORDER BY count(distinct(match.urn)) DESC, entity.text ASC;





SELECT entity.id AS entity_id, entity.text AS entity_text, COUNT(DISTINCT(match.urn)) AS count_1 
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    WHERE entity.user_id = 2
    GROUP BY entity.id, entity.text
    ORDER BY count(distinct(match.urn)) DESC, entity.text ASC;


SELECT entity.id AS entity_id, entity.text AS entity_text, COUNT(DISTINCT(match_1.urn)) AS count_1 
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN frame ON frame.urn = match.urn
    LEFT JOIN match AS match_1 ON frame.urn = match_1.urn 
    LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id
    WHERE entity.user_id = 2 AND entity_1.user_id = 2
    AND (entity_1.id IN (17) OR entity_1.id IS NULL)
    GROUP BY entity.id, entity.text
    ORDER BY count(distinct(match_1.urn)) DESC, entity.text ASC;


EXPLAIN ANALYZE

SELECT entity.id AS entity_id, entity.text AS entity_text, COUNT(DISTINCT(match.urn)) AS count_1 
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN frame ON match.urn = frame.urn
    LEFT JOIN match AS match_1 ON match_1.urn = frame.urn
    LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id
    WHERE entity.user_id = 2 AND entity_1.user_id = 2
    AND (entity_1.id IN (17) OR entity_1.id IS NULL)
    GROUP BY entity.id, entity.text
    ORDER BY count(distinct(match.urn)) DESC, entity.text ASC;


SELECT entity.id AS entity_id, entity.text AS entity_text, COUNT(DISTINCT(match.urn)) AS count_1 
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN frame ON match.urn = frame.urn
    LEFT JOIN match AS match_1 ON match_1.urn = frame.urn
    LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id
    WHERE entity.user_id = 2 AND (entity_1.user_id = 2 OR entity_1.user_id IS NULL)
    AND (entity_1.id IN (17) OR entity_1.id IS NULL)
    GROUP BY entity.id, entity.text
    ORDER BY count(distinct(match.urn)) DESC, entity.text ASC;




EXPLAIN ANALYZE

SELECT DISTINCT entity.text AS entity_text, entity_1.text
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN frame ON match.urn = frame.urn
    LEFT JOIN match AS match_1 ON match_1.urn = frame.urn
    LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id;
    
    WHERE (entity_1.id IN (3) OR entity_1.id IS NULL);
    GROUP BY entity.text 
    ORDER BY entity.text DESC;

SELECT COUNT(DISTINCT entity.text)
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN frame ON match.urn = frame.urn
    LEFT JOIN match AS match_1 ON match_1.urn = frame.urn
    LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id;



SELECT entity.text, COUNT(match.id)
    FROM entity
    LEFT JOIN match ON entity.id = match.entity_id
    WHERE entity.user_id = 2
    GROUP BY entity.text;

SELECT entity.id AS entity_id, entity.created_at AS entity_created_at, entity.updated_at AS entity_updated_at,
    entity.text AS entity_text, entity.category AS entity_category, entity.user_id AS entity_user_id,
    count(distinct(match.urn)) AS count_1 
    FROM entity
    LEFT OUTER JOIN match ON entity.id = match.entity_id
    LEFT OUTER JOIN frame ON frame.urn = match.urn
    LEFT OUTER JOIN match AS match_1 ON frame.urn = match_1.urn
    LEFT OUTER JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id 
    WHERE entity.user_id = 2 AND (entity_1.user_id = 2 OR entity_1.user_id IS NULL)
        AND (match_1.entity_id IN (3) OR match_1.entity_id IS NULL)
    GROUP BY entity.id, entity.created_at, entity.updated_at, entity.text, entity.category, entity.user_id
    ORDER BY count(distinct(match.urn)) DESC, entity.text ASC


SELECT entity.id AS entity_id, entity.text AS entity_text, COUNT(DISTINCT(match.urn)) AS count_1 
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN frame ON match.urn = frame.urn
    LEFT JOIN match AS match_1 ON match_1.urn = frame.urn
    LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id
    WHERE entity.user_id = 2 AND (entity_1.user_id = 2 OR entity_1.user_id IS NULL)
    AND (entity_1.id IN (3, 17) OR entity_1.id IS NULL)
    GROUP BY entity.id, entity.text
    ORDER BY count(distinct(match.urn)) DESC, entity.text ASC;


SELECT entity.id AS entity_id, entity.text AS entity_text, COUNT(DISTINCT(match.urn)) AS count_1 
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN frame ON match.urn = frame.urn
    LEFT JOIN match AS match_1 ON match_1.urn = frame.urn
    LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id
    WHERE entity.user_id = 2 AND entity_1.user_id = 2
    AND entity_1.id IN (3)
    GROUP BY entity.id, entity.text
    ORDER BY count(distinct(match.urn)) DESC, entity.text ASC;




SELECT COUNT(DISTINCT(match.urn)) AS count_1 
    FROM entity 
    LEFT JOIN match ON entity.id = match.entity_id
    LEFT JOIN match AS match_1 ON match_1.urn = match.urn
    LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id
    WHERE entity.user_id = 2 AND entity_1.user_id = 2 AND entity_1.id = 3 AND entity.id = 4;



SELECT entity_1.id AS entity_1_id, entity_1.created_at AS entity_1_created_at, entity_1.updated_at AS
    entity_1_updated_at, entity_1.text AS entity_1_text, entity_1.category AS entity_1_category, entity_1.user_id AS
    entity_1_user_id, count(distinct(match_1.urn)) AS count_1 
FROM entity AS entity_1
    LEFT OUTER JOIN match AS match_1 ON match_1.entity_id = entity_1.id
WHERE entity_1.user_id = 2
GROUP BY entity_1.id, entity_1.created_at, entity_1.updated_at, entity_1.text, entity_1.category, entity_1.user_id
ORDER BY entity_1.text ASC;


SELECT DISTINCT anon_1.entity_1_id AS anon_1_entity_1_id, anon_1.entity_1_created_at AS anon_1_entity_1_created_at, anon_1.entity_1_updated_at AS anon_1_entity_1_updated_at, anon_1.entity_1_text AS anon_1_entity_1_text, anon_1.entity_1_category AS anon_1_entity_1_category, anon_1.entity_1_user_id AS anon_1_entity_1_user_id, anon_1.count_1 AS anon_1_count_1 
FROM (SELECT entity_1.id AS entity_1_id, entity_1.created_at AS entity_1_created_at, entity_1.updated_at AS entity_1_updated_at, entity_1.text AS entity_1_text, entity_1.category AS entity_1_category, entity_1.user_id AS entity_1_user_id, count(distinct(match_1.urn)) AS count_1 
FROM entity AS entity_1 LEFT OUTER JOIN match AS match_1 ON match_1.entity_id = entity_1.id 
WHERE entity_1.user_id = 2 GROUP BY entity_1.id, entity_1.created_at, entity_1.updated_at, entity_1.text, entity_1.category, entity_1.user_id UNION SELECT entity_1.id AS entity_1_id, entity_1.created_at AS entity_1_created_at, entity_1.updated_at AS entity_1_updated_at, entity_1.text AS entity_1_text, entity_1.category AS entity_1_category, entity_1.user_id AS entity_1_user_id, count(distinct(NULL)) AS count_2 
FROM entity AS entity_1 LEFT OUTER JOIN match AS match_1 ON match_1.entity_id = entity_1.id 
WHERE entity_1.user_id = 2 GROUP BY entity_1.id, entity_1.created_at, entity_1.updated_at, entity_1.text, entity_1.category, entity_1.user_id) AS anon_1 ORDER BY anon_1.entity_1_text ASC, anon_1.count_1 DESC;






SELECT entity_1.id AS entity_id, COUNT(DISTINCT match_1.urn)
    FROM match AS match_1 LEFT JOIN entity AS entity_1 ON match_1.entity_id = entity_1.id
    WHERE entity_1.id IN (3) AND entity_1.user_id = 2
    GROUP BY entity_1.id;




SELECT * FROM match m WHERE m.entity_id IN (3);



SELECT m.entity_id, COUNT(DISTINCT m.urn)
    FROM match m
    LEFT JOIN match f1 ON f1.urn = m.urn
    LEFT JOIN match f2 ON f2.urn = m.urn
    WHERE f1.entity_id = 10 AND f2.entity_id = 11
    GROUP BY m.entity_id;


curl -X POST "http://localhost:9200/datawire/_search?pretty=true" -d '
  {
    "query" : { 
        "filtered" : {
            "query" : {
                "match_all" : { }
            },
            "filter" : {
                "and" : [
                    { "term": { "entities": "3" } },
                    { "term": { "entities": "4" } }
                ]
            }
        }
    },
    "facets" : {
      "entities" : { "terms" : {"field" : "entities"} }
    }
  }
'