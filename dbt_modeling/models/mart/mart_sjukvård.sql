with sjukvård_ads AS (select * from {{ ref('mart_ads') }})

select * 
from sjukvård_ads
where occupation_field like '%sjukvård'
