import { api } from "./axios"
import type { Patient } from "../types/patient"

export const fetchPatients = async (): Promise<Patient[]> => {
  const { data } = await api.get<Patient[]>("/Patient")
  return data
}