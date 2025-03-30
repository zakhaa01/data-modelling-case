with
    final as (
        select
            {{ dbt_utils.generate_surrogate_key(["movie_id", "similar_movie_id"]) }} as surrogate_key,
            movie_id,
            similar_movie_id,
            similar_movie_name,
            extracted_at_utc

        from {{ source("raw", "similar") }}
        where extracted_at_utc::date = current_date
    )

select * from final
