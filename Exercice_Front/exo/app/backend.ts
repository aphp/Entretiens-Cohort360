import type { Medication, Patient, Prescription } from "./types";

export async function fetchPatientList() {
    console.debug("Fetching patient list from backend")
    const res = await fetch(`http://localhost:8000/Patient`);
    const patients = await res.json() as Patient[];
    return patients;
}

export async function fetchMedicationList() {
    console.debug("Fetching medication list from backend")
    const res = await fetch(`http://localhost:8000/Medication`);
    const patients = await res.json() as Medication[];
    return patients;
}

export async function fetchPrescriptionList(filter) {
    const baseUrl = new URL('http://localhost:8000/Prescription');
    const searchParams = baseUrl.searchParams;


    for (const [key, value] of Object.entries(filter)) {
        searchParams.set(key, `${value}`);
    }

    console.debug("Fetching medication list from backend", "baseUrl", baseUrl.toString(), "filter", filter);
    const res = await fetch(baseUrl);
    const prescriptions = await res.json() as Prescription[];
    return prescriptions;
}