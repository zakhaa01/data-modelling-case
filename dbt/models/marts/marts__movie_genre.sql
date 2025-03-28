with
    final as (
        select
            m.movie_id,
            m.title,
            g.genre_name
        from {{ ref('stg__daily_movies') }} m
        left join {{ ref('stg__daily_genres') }} g
        on m.movie_id=g.movie_id
        {{ dbt_utils.group_by(3) }}
    )

select * from final
