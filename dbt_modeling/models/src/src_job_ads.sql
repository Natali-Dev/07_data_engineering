with stg_job_ads as (
    select * from {{ source('job_ads', 'stg_ads') }}
)

select 
        occupation__label, 
        id,
        employer__workplace, 
        workplace_address__municipality, 
        experience_required, 
        driving_license_required as driver_licence, 
        access_to_own_car,
        relevance, 
        number_of_vacancies as vacancies,
        application_deadline 
        from stg_job_ads
