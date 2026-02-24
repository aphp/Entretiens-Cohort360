import { api } from "./axios"
import type { Medication } from "../types/medication"

export const fetchMedications = async (): Promise<Medication[]> => {
  const { data } = await api.get<Medication[]>("/Medication")
  return data
}