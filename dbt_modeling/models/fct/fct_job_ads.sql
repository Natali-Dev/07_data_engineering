with job_ads as (select * from {{ ref('src_job_ads') }})

select
        {{dbt_utils.generate_surrogate_key(['occupation__label'])}} as occupation_id, --surrogate key for occupation_id
        {{dbt_utils.generate_surrogate_key(['id'])}} as job_details_id , --key for job_details_id
        {{dbt_utils.generate_surrogate_key(['employer__workplace', 'workplace_address__municipality'])}} as employer_id, -- key for employer_id
        {{dbt_utils.generate_surrogate_key(['experience_required', 'driver_licence', 'access_to_own_car'])}} as auxillary_attributes_id,
        relevance, 
        vacancies, 
        application_deadline 
        from job_ads