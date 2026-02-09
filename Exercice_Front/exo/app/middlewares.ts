
import { medicationContext, patientContext } from "~/context";
import { fetchMedicationList, fetchPatientList } from "~/backend";



export async function patientListMiddleware({ context }, next) {
    const patientsFromCtx = context.get(patientContext);
    if (patientsFromCtx === null) {
        const patientsFromApi = await fetchPatientList();
        const patients = patientsFromApi.reduce((map, p) => map.set(p.id, p), new Map());
        context.set(patientContext, patients);
    }
    await next();
}

export async function medicationListMiddleware({ context }, next) {
    const medicationsFromCtx = context.get(medicationContext);
    if (medicationsFromCtx === null) {
        const medicationsFromApi = await fetchMedicationList();
        const medications = medicationsFromApi.reduce((map, p) => map.set(p.id, p), new Map());
        context.set(medicationContext, medications);
    }
    await next();
}