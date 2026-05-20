{% macro standardise_suburb(column_name) %}
    upper(nullif(trim({{ column_name }}), ''))
{% endmacro %}