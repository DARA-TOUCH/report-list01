import re
import os
import sys
import pandas as pd

# Latest version of COLUMN_LABELS
class COLUMN_LABEL:
    office_code = "Office Code"
    reg_serial = "Reg. Serial"
    reg_date = "Reg. Date"
    receipt_number = "Rcp. Number"
    receipt_date = "Rcp. Date"
    company_code = "Company Code"
    company_name = "Company Name"
    declarant_code = "Declarant Code"
    declarant_name = "Declarant Name"
    package = "Package Number"
    net_weight = "Net Weight (KGM)"
    gross_weight = "Gross Weight (KGM)"
    usd_value = "Item Price"
    khr_value = "Customs Value (KHR)"
    hs_code = "Commodity Code"
    commercial_des_ = "Commercial Description"
    origin_country = "Country of Origin"
    export_country = "Country of Export"
    import_country = "Country of Destination"
    extened_procedure = "Extended Procedure"
    national_procedure = "National Procedure"
    vpp = "VPP Amount"
    vop = "VOP Amount"
    vap = "VAP Amount"
    spp = "SPP Amount"
    sop = "SOP Amount"
    cop = "COP Amount"
    cpp = "CPP Amount"
    atp = "ATP Amount"
    dpp = "DPP Amount"
    vvf = "VVF Amount"
    crp = "CRP Amount"
    dsf = "DSF Amount"
    stf = "STF Amount"
    eto = "ETO Amount"
    etr = "ETR Amount"
    etw = "ETW Amount"
    etp = "ETP Amount"
    bur = "BUR Amount"
    vpp_mop = "VPP MOP"
    vop_mop = "VOP MOP"
    vap_mop = "VAP MOP"
    spp_mop = "SPP MOP"
    sop_mop = "SOP MOP"
    cop_mop = "COP MOP"
    cpp_mop = "CPP MOP"
    atp_mop = "ATP MOP"
    dpp_mop = "DPP MOP"
    vvf_mop = "VVF MOP"
    crp_mop = "CRP MOP"
    dsf_mop = "DSF MOP"
    stf_mop = "ST MOP"
COLUMN_LABELS = {
    "office_code": "Office Code",
    "reg_serial": "Reg. Serial",
    "reg_date": "Reg. Date",
    "receipt_number": "Rcp. Number",
    "receipt_date": "Rcp. Date",
    "company_code": "Company Code",
    "company_name": "Company Name",
    "declarant_code": "Declarant Code",
    "declarant_name": "Declarant Name",
    "package": "Package Number",
    "net_weight": "Net Weight (KGM)",
    "gross_weight": "Gross Weight (KGM)",
    "usd_value": "Item Price",
    "khr_value": "Customs Value (KHR)",
    "hs_code": "Commodity Code",
    "commercial_des_": "Commercial Description",
    "origin_country": "Country of Origin",
    "export_country": "Country of Export",
    "import_country": "Country of Destination",
    "extened_procedure": "Extended Procedure",
    "national_procedure": "National Procedure",
    "vpp": "VPP Amount",
    "vop": "VOP Amount",
    "vap": "VAP Amount",
    "spp": "SPP Amount",
    "sop": "SOP Amount",
    "cop": "COP Amount",
    "cpp": "CPP Amount",
    "atp": "ATP Amount",
    "dpp": "DPP Amount",
    "vvf": "VVF Amount",
    "crp": "CRP Amount",
    "dsf": "DSF Amount",
    "stf": "STF Amount",
    "eto": "ETO Amount",
    "etr": "ETR Amount",
    "etw": "ETW Amount",
    "etp": "ETP Amount",
    "bur": "BUR Amount",
    "vpp_mop": "VPP MOP",
    "vop_mop": "VOP MOP",
    "vap_mop": "VAP MOP",
    "spp_mop": "SPP MOP",
    "sop_mop": "SOP MOP",
    "cop_mop": "COP MOP",
    "cpp_mop": "CPP MOP",
    "atp_mop": "ATP MOP",
    "dpp_mop": "DPP MOP",
    "vvf_mop": "VVF MOP",
    "crp_mop": "CRP MOP",
    "dsf_mop": "DSF MOP",
    "stf_mop": "STF MOP",
    "eto_mop": "ETO MOP",
    "etr_mop": "ETR MOP",
    "etw_mop": "ETW MOP",
    "etp_mop": "ETP MOP",
    "bur_mop": "BUR MOP",
    "data_source": "Data Source",
}
# NUMERIC_OBJECTS = frozenset([item for item in COLUMN_LABELS.keys() if re.search(r"(Amount|Weight|KGM|Number|Value|Price)", COLUMN_LABELS[item])])
# STRING_OBJECTS = frozenset([item for item in COLUMN_LABELS.keys() if re.search(r"(Declarant|Company|Code|Country|Procedure|Serial)", COLUMN_LABELS[item])])
NUMERIC_OBJECTS = frozenset(
    {
        "vvf",
        "sop",
        "vop",
        "eto",
        "pakage",
        "etp",
        "etr",
        "crp",
        "stf",
        "cop",
        'cpp',
        "khr_value",
        "vpp",
        "dpp",
        "dsf",
        "usd_value",
        "gross_weight",
        "atp",
        "vap",
        "etw",
        "bur",
        "spp",
        "net_weight",
    })
STRING_OBJECTS = frozenset(
    {
        "extened_procedure",
        "hs_code",
        "import_country",
        "declarant_code",
        "national_procedure",
        "company_name",
        "company_code",
        "export_country",
        "declarant_name",
        "origin_country",
        "office_code",
    }
)

__file_path = os.path.abspath(__file__)
stamp_file_path = os.path.abspath(os.path.join(__file_path, "..", "..", "..", 'staticfiles', 'excel', 'csv', 'stamp_by_hs.csv'))

stamp_dataframe = pd.read_csv(stamp_file_path)
stamp_item_list = stamp_dataframe['stamp_kind'].unique()
sorted_stamp_item_list = sorted(stamp_item_list)
STAMP_TYPES = {i: item for i, item in enumerate(sorted_stamp_item_list)}
