from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.fhirtypes import PatientType
from fhir.resources.fhirtypes import HumanNameType
from fhir.resources.identifier import Identifier
from fhir.resources.fhirtypes import IdentifierType
from fhir.resources.encounter import Encounter
from fhir.resources.fhirtypes import EncounterType

from pydantic import BaseModel

import requests 
from fastapi import FastAPI

Name = "Manjunath Maddareddy"

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
    contact=   [{'name': {'family': 'Manjunath', 'given': ['Maddareddy']}},
               {'telecom': [{'system': 'phone', 'value': '555-555-2003', 'use': 'home'}]},
               {'address': {'line': ['123 Main St'], 'city': 'Somewhere', 'state': 'CA', 'postalCode': '90210', 'country': 'USA'}},
               {'relationship': [{'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/v2-0131', 'code': 'N', 'display': 'Next of Kin'}]}]},
               {'gender': 'male'}
              ])
patient_json = patient.model_dump_json()
# ... create an Encounter resource

#enttype = EncounterType(coding=[{'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode', 'code': 'AMB', 'display': 'Ambulatory'}])
encounter = Encounter(status='finished'    
                     )

@app.post("/create_patient/")
def create_patient():   
    patient_instance = Patient.parse_raw(patient_json)
    response = requests.post(FHIR_SERVER_URL, data=patient_instance.model_dump_json(), headers={"Content-Type": "application/fhir+json"})
    return response.json()

@app.get("/get_patient/{patient_id}")
def get_patient(patient_id: str):
    response = requests.get(f"{FHIR_SERVER_URL}/{patient_id}", headers={"Content-Type": "application/fhir+json"})
    Name = response.json().get('name', [{}])[0]
    print("Patient Name:", Name)    
    gender = response.json().get('gender', 'unknown')
    print("Patient Gender:", gender)
    
    #response = requests.get(f"{MY_API_URL}/{patient_id}", headers={"Content-Type": "application/fhir+json"})
    if response.status_code == 200:
        patient_instance = Patient.model_validate_json(response.text)
        #return patient_instance.model_dump()
        return gender
    else:
        return {"error": "Patient not found", "status_code": response.status_code}
@app.post("/create_encounter/patient_id/{patient_id}")
def create_encounter(patient_id: str):   
    encounter_instance = Encounter.parse_raw(encounter.model_dump_json())
    response = requests.post(FHIR_SERVER_URL.replace("Patient", "Encounter"), data=encounter_instance.model_dump_json(), headers={"Content-Type": "application/fhir+json"})
    return response.json()
    
@app.get("/get_encounter/{encounter_id}")
def get_encounter(encounter_id: str):
    response = requests.get(f"{FHIR_SERVER_URL}/Encounter/{encounter_id}", headers={"Content-Type": "application/fhir+json"})
    if response.status_code == 200:
        encounter_instance = Encounter.parse_raw(response.text)
        return encounter_instance.model_dump()
    else:
        return {"error": "Encounter not found", "status_code": response.status_code}

@app.get("/")  
def read_root():
    return {"Hello": Name}
