with attributes AS (
select occupation_field, experience_required, access_to_own_car, driver_licence
from {{ ref('mart_ads') }}
)

select * from attributes