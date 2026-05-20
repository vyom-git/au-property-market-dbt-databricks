with source as (

    select *
    from {{ source('bronze', 'raw_property_sales') }}

),

renamed as (

    select
        cast(`Property ID` as bigint) as property_id,
        cast(`Sale counter` as bigint) as sale_counter,

        to_timestamp(`Download date / time`, 'yyyyMMdd HH:mm') as downloaded_at,

        nullif(trim(`Property name`), '') as property_name,
        nullif(trim(`Property unit number`), '') as property_unit_number,
        nullif(trim(`Property house number`), '') as property_house_number,
        nullif(trim(`Property street name`), '') as property_street_name,

        {{ standardise_suburb('`Property locality`') }} as suburb,

        cast(`Property post code` as int) as postcode,

        cast(`Area` as double) as area,
        nullif(trim(`Area type`), '') as area_type,

        to_date(`Contract date`, 'yyyyMMdd') as contract_date,
        to_date(`Settlement date`, 'yyyyMMdd') as settlement_date,

        cast(`Purchase price` as double) as purchase_price,

        nullif(trim(`Zoning`), '') as zoning,
        nullif(trim(`Nature of property`), '') as nature_of_property,
        nullif(trim(`Primary purpose`), '') as primary_purpose,

        cast(`Strata lot number` as bigint) as strata_lot_number,

        nullif(trim(`Dealing number`), '') as dealing_number,
        nullif(trim(`Property legal description`), '') as property_legal_description

    from source

),

final as (

    select
        *,
        case
            when purchase_price <= 0 then true
            else false
        end as is_invalid_purchase_price,

        case
            when lower(primary_purpose) like '%residence%' then 'Residential'
            when lower(primary_purpose) like '%commercial%' then 'Commercial'
            when lower(primary_purpose) like '%vacant%' then 'Vacant Land'
            else 'Other'
        end as property_purpose_group

    from renamed

)

select *
from final