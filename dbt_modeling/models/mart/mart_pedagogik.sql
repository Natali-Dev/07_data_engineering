with pedagogik_ads AS (select * from {{ ref('mart_ads') }})

select * 
from pedagogik_ads
where occupation_field ILIKE 'pedagogik'
