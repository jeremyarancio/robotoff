SET threads to 4;
SET preserve_insertion_order = false;
SELECT
    code,
    additives_n,
    additives_tags,
    allergens_from_ingredients,
    allergens_from_user,
    allergens_tags,
    brands_tags,
    categories_properties_tags,
    categories,
    checkers_tags,
    cities_tags,
    compared_to_category,
    complete,
    completeness,
    correctors_tags,
    countries_tags,
    to_timestamp(created_t)::datetime AS created_t, -- Convert from unixtime to datetime
    creator,
    data_quality_errors_tags,
    data_quality_info_tags,
    data_quality_warnings_tags,
    data_sources_tags,
    ecoscore_data,
    ecoscore_grade,
    ecoscore_score,
    ecoscore_tags,
    editors,
    emb_codes,
    emb_codes_tags,
    entry_dates_tags,
    environment_impact_level,
    food_groups_tags,
    forest_footprint_data,
    generic_name,
    grades,
    images,
    informers_tags,
    ingredients_analysis_tags,
    ingredients_from_palm_oil_n,
    ingredients_n,
    ingredients_tags,
    ingredients_text_with_allergens,
    ingredients_text,
    COLUMNS('ingredients_text_\w{2}$'), -- All columns containing ingredients_text_..
    ingredients_with_specified_percent_n,
    ingredients_with_unspecified_percent_n,
    ciqual_food_name_tags,
    ingredients_percent_analysis,
    ingredients_original_tags,
    ingredients_without_ciqual_codes_n,
    ingredients_without_ciqual_codes,
    ingredients,
    known_ingredients_n,
    labels_tags,
    lang,
    languages_tags,
    languages_codes,
    last_edit_dates_tags,
    last_editor,
    to_timestamp(last_image_t)::datetime AS last_image_t,
    last_modified_by,
    to_timestamp(last_modified_t)::datetime AS last_modified_t,
    to_timestamp(last_updated_t)::datetime AS last_updated_t,
    link,
    main_countries_tags,
    manufacturing_places,
    manufacturing_places_tags,
    max_imgid,
    misc_tags,
    minerals_tags,
    new_additives_n,
    no_nutrition_data,
    nova_group,
    nova_groups,
    nova_groups_markers,
    nova_groups_tags,
    nucleotides_tags,
    nutrient_levels_tags,
    unknown_nutrients_tags,
    nutriments,
    nutriscore_data,
    nutriscore_grade,
    nutriscore_score,
    nutriscore_tags,
    nutrition_data_prepared_per,
    nutrition_data,
    nutrition_grades_tags,
    nutrition_score_beverage,
    nutrition_score_warning_fruits_vegetables_nuts_estimate_from_ingredients,
    nutrition_score_warning_no_fiber,
    nutrition_score_warning_no_fruits_vegetables_nuts,
    obsolete_since_date,
    obsolete,
    origins_tags,
    packaging_recycling_tags,
    packaging_shapes_tags,
    packaging_tags,
    packagings_materials,
    packagings_n,
    packagings_n,
    photographers,
    pnns_groups_1_tags,
    pnns_groups_2_tags,
    popularity_key,
    popularity_tags,
    product_name,
    product_quantity_unit,
    product_quantity,
    purchase_places_tags,
    quantity,
    rev,
    scans_n,
    scores,
    serving_quantity,
    serving_size,
    sources,
    sources_fields,
    specific_ingredients,
    states_tags,
    stores,
    stores_tags,
    traces_tags,
    unique_scans_n,
    unknown_ingredients_n,
    vitamins_tags,
    weighers_tags,
    with_non_nutritive_sweeteners,
    with_sweeteners,
FROM read_ndjson('{dataset_path}', ignore_errors=True)