with source as (
    select * from {{ source('public', 'race_control_events') }}
),

relevant_flags as (
    select
        session_key,
        lap_number,
        flag,
        category,
        message,
        year
    from source
    where flag in ('YELLOW', 'DOUBLE_YELLOW', 'RED', 'SAFETY_CAR', 'VIRTUAL_SAFETY_CAR')
)

select * from relevant_flags