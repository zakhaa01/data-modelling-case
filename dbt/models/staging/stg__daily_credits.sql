with
    final as (
        select
            {{ dbt_utils.generate_surrogate_key(["movie_id", "actor_id"]) }} as surrogate_key,
            movie_id,
            actor_id,
            actor_name,
            character_name,
            extracted_at_utc

        from {{ source("raw", "credits") }}
        where extracted_at_utc::date = current_date
    )

select * from final
