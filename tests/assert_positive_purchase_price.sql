select *
from {{ ref('stg_property_sales') }}
where purchase_price <= 0