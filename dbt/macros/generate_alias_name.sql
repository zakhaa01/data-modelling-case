-- Override default Macro:
-- In deployment, run models as usual
-- Otherwise (When run locally) username as table name prefix
{% macro generate_alias_name(custom_alias_name=none, node=none) -%}

    {% set myenv = env_var("ENV", "local") %}
    {% set env_deployment = ["dev", "live", "DEV", "LIVE"] %}

    {%- if myenv in env_deployment -%}

        {%- if custom_alias_name is none -%} {{ node.name }}
        {%- else -%} {{ custom_alias_name | trim }}
        {%- endif -%}

    {%- else -%}

        {%- if custom_alias_name is none -%} {{ target.user }}_{{ node.name }}
        {%- else -%} {{ target.user }}_{{ custom_alias_name | trim }}
        {%- endif -%}

    {%- endif -%}

{%- endmacro %}
