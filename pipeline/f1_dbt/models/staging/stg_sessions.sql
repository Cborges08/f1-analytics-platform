with source as (
    select * from {{ source('public', 'sessions') }}
),

cleaned as (
    select
        session_key,
        session_name,
        session_type,
        date_start::date                    as race_date,
        extract(year from date_start)::int  as season_year,
        circuit_key,
        circuit_short_name,
        country_name,
        location,
        year
    from source
    where session_type = 'Race'
)

select * from cleaned