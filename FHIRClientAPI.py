from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.fhirtypes import PatientType
from fhir.resources.fhirtypes import HumanNameType
from fhir.resources.identifier import Identifier
from fhir.resources.fhirtypes import IdentifierType
from fhir.resources.encounter import Encounter


from pydantic import BaseModel


import requests 
from fastapi import FastAPI

app = FastAPI()
FHIR_SERVER_URL = "https://hapi.fhir.org/baseR4/Patient" # Replace with your server URL
MY_API_URL = "https://api-development-n7r3.onrender.com/get_patient/"


# ... create a Patient resource
patient_name = HumanName(family='Manjunath', given=['Maddareddy'])
patient = Patient(
    name=[patient_name], 
    gender='male',
    birthDate='1984-06-01',
    identifier=[Identifier(system='http://hospital.smarthealthit.org',
    value='547414464')],
    maritalStatus = {'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/v3-MaritalStatus', 'code': 'M', 'display': 'Married'}]},
    active=True,
    contact=   [{'relationship': 
               [{'coding': 
               [{'system': 'http://terminology.hl7.org/CodeSystem/v2-0131', 'code': 'E', 'display': 'Emergency'}]}]}     ])
encounter = Encounter(status = 'finished')
patient_json = patient.model_dump_json()

@app.post("/create_patient/")
def create_patient():   
    patient_instance = Patient.parse_raw(patient_json)
    response = requests.post(FHIR_SERVER_URL, data=patient_instance.model_dump_json(), headers={"Content-Type": "application/fhir+json"})
    return response.json()

@app.get("/get_patient/{patient_id}")
def get_patient(patient_id: str):
    #response = requests.get(f"{FHIR_SERVER_URL}/{patient_id}", headers={"Content-Type": "application/fhir+json"})
    response = requests.get(f"{MY_API_URL}/{patient_id}", headers={"Content-Type": "application/fhir+json"})
    if response.status_code == 200:
        patient_instance = Patient.model_validate_json(response.text)
        print("Patient ID:", patient_instance.identifier[0].value)
        print("Patient Name:", patient_instance.name[0].given[0], patient_instance.name[0].family)
        return patient_instance.model_dump_json()
    else:
        return {"error": "Patient not found", "status_code": response.status_code}

@app.get("/get_encounter/{encounter_id}")
def get_encounter(encounter_id: str):
    response = requests.get(f"{FHIR_SERVER_URL}/Encounter/{encounter_id}", headers={"Content-Type": "application/fhir+json"})
    if response.status_code == 200:
        encounter_instance = Patient.parse_raw(response.text)
        return encounter_instance.model_dump()
    else:
        return {"error": "Encounter not found", "status_code": response.status_code}

@app.get("/")  
def read_root():
    return {"message": "Welcome to the FHIR Client API"}
