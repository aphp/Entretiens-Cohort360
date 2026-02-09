import { createContext } from "react-router";
import type { Medication, Patient } from "~/types";


export const patientContext = createContext<Map<number, Patient> | null>(null);
export const medicationContext = createContext<Map<number, Medication> | null>(null);
