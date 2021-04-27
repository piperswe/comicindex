SELECT s.id,
       s.osm_id,
       s.name,
       s.phone_number,
       s.email_address,
       s.website,
       a.line_1,
       a.line_2,
       a.city,
       a.region,
       a.postal_code,
       a.country
FROM stores s
         LEFT JOIN addresses a on a.id = s.address