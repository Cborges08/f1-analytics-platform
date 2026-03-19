with source as (
    select * from {{ source('public', 'race_results') }}
),

cleaned as (
    select
        id,
        session_key,
        driver_number,
        position,
        year,
        case
            when position = 1 then 'WIN'
            when position <= 3 then 'PODIUM'
            when position <= 10 then 'POINTS'
            else 'OUT_OF_POINTS'
        end as result_category
    from source
)

select * from cleaned