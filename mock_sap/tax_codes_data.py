from datetime import date
from typing import Any


TAX_CODES: list[dict[str, Any]] = [
    # -----------------------------------------------------
    # UNITED KINGDOM VAT
    # -----------------------------------------------------
    {
        "tax_code": "UK20",
        "tax_type": "VAT",
        "country_code": "GB",
        "region_code": None,
        "locality_code": None,
        "tax_jurisdiction": "UNITED_KINGDOM",
        "description": "UK Standard Rate VAT",
        "rate": 20.0,
        "input_tax_gl_account": "220000",
        "output_tax_gl_account": "220100",
        "recoverable_percentage": 100.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": False,
        "external_rate_lookup_required": False,
        "effective_from": "2020-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
    {
        "tax_code": "UK05",
        "tax_type": "VAT",
        "country_code": "GB",
        "region_code": None,
        "locality_code": None,
        "tax_jurisdiction": "UNITED_KINGDOM",
        "description": "UK Reduced Rate VAT",
        "rate": 5.0,
        "input_tax_gl_account": "220000",
        "output_tax_gl_account": "220100",
        "recoverable_percentage": 100.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": False,
        "external_rate_lookup_required": False,
        "effective_from": "2020-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
    {
        "tax_code": "UK00",
        "tax_type": "VAT",
        "country_code": "GB",
        "region_code": None,
        "locality_code": None,
        "tax_jurisdiction": "UNITED_KINGDOM",
        "description": "UK Zero-Rated VAT",
        "rate": 0.0,
        "input_tax_gl_account": "220000",
        "output_tax_gl_account": "220100",
        "recoverable_percentage": 100.0,
        "reverse_charge": False,
        "zero_rated": True,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": False,
        "external_rate_lookup_required": False,
        "effective_from": "2020-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
    {
        "tax_code": "UKEX",
        "tax_type": "VAT",
        "country_code": "GB",
        "region_code": None,
        "locality_code": None,
        "tax_jurisdiction": "UNITED_KINGDOM",
        "description": "UK VAT Exempt",
        "rate": 0.0,
        "input_tax_gl_account": "220000",
        "output_tax_gl_account": "220100",
        "recoverable_percentage": 0.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": True,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": False,
        "external_rate_lookup_required": False,
        "effective_from": "2020-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },

    # -----------------------------------------------------
    # AUSTRALIA GST
    # -----------------------------------------------------
    {
        "tax_code": "AUG10",
        "tax_type": "GST",
        "country_code": "AU",
        "region_code": None,
        "locality_code": None,
        "tax_jurisdiction": "AUSTRALIA",
        "description": "Australia Standard GST",
        "rate": 10.0,
        "input_tax_gl_account": "221000",
        "output_tax_gl_account": "221100",
        "recoverable_percentage": 100.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": False,
        "external_rate_lookup_required": False,
        "effective_from": "2000-07-01",
        "effective_to": None,
        "status": "ACTIVE",
    },

    # -----------------------------------------------------
    # SINGAPORE GST
    # -----------------------------------------------------
    {
        "tax_code": "SGG09",
        "tax_type": "GST",
        "country_code": "SG",
        "region_code": None,
        "locality_code": None,
        "tax_jurisdiction": "SINGAPORE",
        "description": "Singapore Standard GST",
        "rate": 9.0,
        "input_tax_gl_account": "222000",
        "output_tax_gl_account": "222100",
        "recoverable_percentage": 100.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": False,
        "external_rate_lookup_required": False,
        "effective_from": "2024-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },

    # -----------------------------------------------------
    # INDIA GST
    # -----------------------------------------------------
    {
        "tax_code": "INIG18",
        "tax_type": "IGST",
        "country_code": "IN",
        "region_code": None,
        "locality_code": None,
        "tax_jurisdiction": "INDIA_INTERSTATE",
        "description": "India Integrated GST",
        "rate": 18.0,
        "input_tax_gl_account": "223000",
        "output_tax_gl_account": "223100",
        "recoverable_percentage": 100.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": True,
        "external_rate_lookup_required": False,
        "effective_from": "2017-07-01",
        "effective_to": None,
        "status": "ACTIVE",
    },

    # -----------------------------------------------------
    # UNITED STATES SALES AND USE TAX
    # These are representative base rates only.
    # Local rates may also apply.
    # -----------------------------------------------------
    {
        "tax_code": "USCA725",
        "tax_type": "SALES_TAX",
        "country_code": "US",
        "region_code": "CA",
        "locality_code": None,
        "tax_jurisdiction": "US_CALIFORNIA_BASE",
        "description": "California Statewide Base Sales and Use Tax",
        "rate": 7.25,
        "input_tax_gl_account": "224000",
        "output_tax_gl_account": "224100",
        "recoverable_percentage": 0.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": True,
        "external_rate_lookup_required": True,
        "effective_from": "2017-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
    {
        "tax_code": "USNY400",
        "tax_type": "SALES_TAX",
        "country_code": "US",
        "region_code": "NY",
        "locality_code": None,
        "tax_jurisdiction": "US_NEW_YORK_STATE_BASE",
        "description": "New York State Base Sales Tax",
        "rate": 4.0,
        "input_tax_gl_account": "224000",
        "output_tax_gl_account": "224100",
        "recoverable_percentage": 0.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": True,
        "external_rate_lookup_required": True,
        "effective_from": "1965-08-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
    {
        "tax_code": "USEXEMPT",
        "tax_type": "SALES_TAX",
        "country_code": "US",
        "region_code": None,
        "locality_code": None,
        "tax_jurisdiction": "UNITED_STATES",
        "description": "US Sales Tax Exempt Transaction",
        "rate": 0.0,
        "input_tax_gl_account": "224000",
        "output_tax_gl_account": "224100",
        "recoverable_percentage": 0.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": True,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": True,
        "external_rate_lookup_required": False,
        "effective_from": "2020-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },

    # -----------------------------------------------------
    # CANADA GST, HST AND PST
    # -----------------------------------------------------
    {
        "tax_code": "CAABGST5",
        "tax_type": "GST",
        "country_code": "CA",
        "region_code": "AB",
        "locality_code": None,
        "tax_jurisdiction": "CANADA_ALBERTA",
        "description": "Alberta Federal GST",
        "rate": 5.0,
        "input_tax_gl_account": "225000",
        "output_tax_gl_account": "225100",
        "recoverable_percentage": 100.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": True,
        "external_rate_lookup_required": False,
        "effective_from": "2008-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
    {
        "tax_code": "CAONHST13",
        "tax_type": "HST",
        "country_code": "CA",
        "region_code": "ON",
        "locality_code": None,
        "tax_jurisdiction": "CANADA_ONTARIO",
        "description": "Ontario Harmonised Sales Tax",
        "rate": 13.0,
        "input_tax_gl_account": "225200",
        "output_tax_gl_account": "225300",
        "recoverable_percentage": 100.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": True,
        "external_rate_lookup_required": False,
        "effective_from": "2010-07-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
    {
        "tax_code": "CABCGST5",
        "tax_type": "GST",
        "country_code": "CA",
        "region_code": "BC",
        "locality_code": None,
        "tax_jurisdiction": "CANADA_BRITISH_COLUMBIA",
        "description": "British Columbia Federal GST",
        "rate": 5.0,
        "input_tax_gl_account": "225000",
        "output_tax_gl_account": "225100",
        "recoverable_percentage": 100.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": True,
        "compound_group": "CA_BC_STANDARD",
        "place_of_supply_required": True,
        "external_rate_lookup_required": False,
        "effective_from": "2008-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
    {
        "tax_code": "CABCPST7",
        "tax_type": "PST",
        "country_code": "CA",
        "region_code": "BC",
        "locality_code": None,
        "tax_jurisdiction": "CANADA_BRITISH_COLUMBIA",
        "description": "British Columbia Provincial Sales Tax",
        "rate": 7.0,
        "input_tax_gl_account": "225400",
        "output_tax_gl_account": "225500",
        "recoverable_percentage": 0.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": False,
        "compound_tax": True,
        "compound_group": "CA_BC_STANDARD",
        "place_of_supply_required": True,
        "external_rate_lookup_required": False,
        "effective_from": "2013-04-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
    {
        "tax_code": "CAEXEMPT",
        "tax_type": "GST_HST",
        "country_code": "CA",
        "region_code": None,
        "locality_code": None,
        "tax_jurisdiction": "CANADA",
        "description": "Canada Tax-Exempt Transaction",
        "rate": 0.0,
        "input_tax_gl_account": "225000",
        "output_tax_gl_account": "225100",
        "recoverable_percentage": 0.0,
        "reverse_charge": False,
        "zero_rated": False,
        "exempt": True,
        "compound_tax": False,
        "compound_group": None,
        "place_of_supply_required": True,
        "external_rate_lookup_required": False,
        "effective_from": "2020-01-01",
        "effective_to": None,
        "status": "ACTIVE",
    },
]


def get_all_tax_codes() -> list[dict]:
    """
    Return all configured tax codes.
    """
    return TAX_CODES


def get_tax_code(
    tax_code: str,
) -> dict | None:
    """
    Return one tax code by its identifier.
    """
    tax_code = tax_code.upper()

    for item in TAX_CODES:
        if item["tax_code"] == tax_code:
            return item

    return None


def get_tax_codes_for_country(
    country_code: str,
) -> list[dict]:
    """
    Return all active tax codes for one country.
    """
    country_code = country_code.upper()

    return [
        item
        for item in TAX_CODES
        if item["country_code"] == country_code
        and item["status"] == "ACTIVE"
    ]


def get_tax_codes_for_region(
    country_code: str,
    region_code: str,
) -> list[dict]:
    """
    Return active tax codes for one country and region.
    """
    country_code = country_code.upper()
    region_code = region_code.upper()

    return [
        item
        for item in TAX_CODES
        if item["country_code"] == country_code
        and item["region_code"] == region_code
        and item["status"] == "ACTIVE"
    ]


def get_compound_tax_codes(
    compound_group: str,
) -> list[dict]:
    """
    Return all active codes belonging to a compound tax group.
    """
    compound_group = compound_group.upper()

    return [
        item
        for item in TAX_CODES
        if item["compound_group"] == compound_group
        and item["status"] == "ACTIVE"
    ]


def is_tax_code_active(
    tax_code: str,
    transaction_date: str | None = None,
) -> bool:
    """
    Check whether a tax code is active on the selected date.
    """
    item = get_tax_code(tax_code)

    if item is None:
        return False

    if item["status"] != "ACTIVE":
        return False

    check_date = (
        date.fromisoformat(transaction_date)
        if transaction_date
        else date.today()
    )

    effective_from = date.fromisoformat(
        item["effective_from"]
    )

    effective_to = (
        date.fromisoformat(item["effective_to"])
        if item["effective_to"]
        else None
    )

    if check_date < effective_from:
        return False

    if effective_to and check_date > effective_to:
        return False

    return True