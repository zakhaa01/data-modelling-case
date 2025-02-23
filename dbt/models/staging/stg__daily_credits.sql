with
    final as (
        select
            movie_id,
            actor_id,
            actor_name,
            character_name,
            extracted_at_utc

        from {{ source("raw", "credits") }}
        where extracted_at_utc::date = current_date
    )

select * from final
