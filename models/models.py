from patito import Model
from datetime import date
from typing import Literal

class NDCNameTable(Model):
    ndc: str
    product: str

class HospitalTable(Model):
    id: str
    name: str
    beds: int
    address: str
    city: str
    state: str
    zip: str
    phone: str
    lat: float
    long: float
    retrieved: date 
    hospital_url: str
    is_340b: bool
    program_type: str | None

class HospitalPriceFile(Model):
    hospital_id: str
    description: str | None
    setting: Literal['inpatient', 'outpatient', 'both'] | None
    drug_unit_of_measurement: float
    drug_type_of_measurement: str | None
    standard_charge_gross: float | None = None
    standard_charge_discounted_cash: float | None
    standard_charge_negotiated_dollar: float
    plan_name: str
    payer_name: str
    standard_charge_methodology: str | None
    standard_charge_negotiated_percentage: float | None
    hcpcs: str | None
    ndc: str | None
    calculated_negotiated_dollars: bool
    mapped_plan_name: str | None
    mapped_lob_name: str | None

class HcpcsDescTable(Model):
    hcpcs: str
    hcpcs_desc: str

class BenchmarkFile(Model):
    ndc: str | None
    hcpcs: str | None
    asp: float | None
    nadac: float | None
    tx_unit_price: float | None
    tx_340b: float | None

class AGTable(Model):
    hospital_id: str
    description: str | None
    setting: Literal['inpatient', 'outpatient', 'both'] | None
    drug_unit_of_measurement: float
    drug_type_of_measurement: str | None
    standard_charge_gross: float | None = None
    standard_charge_discounted_cash: float | None
    standard_charge_negotiated_dollar: float
    plan_name: str
    payer_name: str
    standard_charge_methodology: str | None
    standard_charge_negotiated_percentage: float | None
    hcpcs: str | None
    ndc: str | None
    calculated_negotiated_dollars: bool
    mapped_plan_name: str | None
    mapped_lob_name: str | None
    name: str
    beds: int
    state: str
    retrieved: date 
    is_340b: bool

class TransparencyTable(Model):
    description: str
    benchmark: str
    mean_price: float
