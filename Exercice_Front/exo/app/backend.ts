import type { Medication, Patient, Prescription } from "./types";

// TODO Move this parameter into the central configuration file
// and make it depend on the deployment environment.
const baseBackendUrl = "http://localhost:8000";

export async function fetchPatientList() {
    console.debug("Fetching patient list from backend")
    const res = await fetch(`${baseBackendUrl}/Patient`);
    const patients = await res.json() as Patient[];
    return patients;
}

export async function fetchMedicationList() {
    console.debug("Fetching medication list from backend")
    const res = await fetch(`${baseBackendUrl}/Medication`);
    const patients = await res.json() as Medication[];
    return patients;
}

export async function fetchPrescriptionList(filter) {
    const baseUrl = new URL(`${baseBackendUrl}/Prescription`);
    const searchParams = baseUrl.searchParams;


    for (const [key, value] of Object.entries(filter)) {
        searchParams.set(key, `${value}`);
    }

    console.debug("Fetching prescription list from backend", baseUrl.toString());
    const res = await fetch(baseUrl);
    const prescriptions = await res.json() as Prescription[];
    return prescriptions;
}

export async function createPrescription(data: FormData) {
    const baseUrl = new URL(`${baseBackendUrl}/Prescription`);
    return await fetch(baseUrl, { method: "POST", body: data });
}