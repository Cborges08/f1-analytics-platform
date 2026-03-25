with source as (
    select * from {{ source('public', 'qualifying_results') }}
),

cleaned as (
    select
        session_key,
        driver_number,
        position as qualifying_position,
        q1_time,
        q2_time,
        q3_time,
        year
    from source
    where position is not null
)

select * from cleaned
