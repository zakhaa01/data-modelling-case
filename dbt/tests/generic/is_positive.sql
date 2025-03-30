{% test is_positive(model, column_name) %}

    with
        validation_errors as (

            select
                {{ column_name }} as validation_column,
                case when {{ column_name }} >= 0 then true else false end as is_positive

            from {{ model }}
            where validation_column is not null and is_positive is false

        )

    select *
    from validation_errors

{% endtest %}
