-- Override default Macro:
-- In deployment, run models in default schema
-- Otherwise (When run locally) always run models in _sandbox schema
{% macro generate_schema_name(custom_schema_name, node) -%}

    {% set myenv = env_var("ENV", "local") %}
    {%- set env_deployment = ["dev", "live", "DEV", "LIVE"] -%}
    {%- set default_schema = target.schema -%}

    {%- if myenv in env_deployment -%}

        {%- if custom_schema_name is none -%} {{ default_schema }}
        {%- else -%} {{ default_schema }}_{{ custom_schema_name | trim }}
        {%- endif -%}

    {%- else -%} {{ default_schema }}_sandbox
    {%- endif -%}

{%- endmacro %}
