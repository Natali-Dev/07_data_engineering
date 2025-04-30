with tekniska_ads AS (select * from {{ ref('mart_ads') }})

select * 
from tekniska_ads
where occupation_field like '%teknisk inriktning'
