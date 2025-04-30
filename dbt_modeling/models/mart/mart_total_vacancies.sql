-- occupation, city, total_vacancies

with total_vacancies as (

select occupation, municipality, occupation_field, sum(vacancies) as total_vacancies
from {{ ref('mart_ads') }}
group by occupation, municipality, occupation_field
order by total_vacancies desc 

)

select * from total_vacancies