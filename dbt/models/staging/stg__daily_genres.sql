with
    final as (
        select
            {{ dbt_utils.generate_surrogate_key(["movie_id", "genre_id"]) }} as surrogate_key,
            movie_id,
            genre_id,
            genre_name,
            extracted_at_utc

        from {{ source("raw", "movies_genre") }}
        where extracted_at_utc::date = current_date
    )

select * from final
