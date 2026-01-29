import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import axios from "axios";
import Prescriptions from "./Prescriptions"; // Ensure this matches the export in Prescriptions.tsx
import Modal from "react-modal";

// Mock axios
jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe("Prescriptions Component", () => {
  const mockPrescriptions = [
    {
      id: 1,
      patient_name: "Doe John",
      patient: 1,
      medication_code: "MED001",
      medication: 1,
      prescription_start_date: "2024-01-01",
      prescription_end_date: "2024-01-31",
      presscription_status: "valide",
      commentaire: "Test comment",
    },
  ];

  const mockPatients = [{ id: 1, first_name: "John", last_name: "Doe" }];

  const mockMedications = [{ id: 1, code: "MED001" }];

  beforeEach(() => {
    mockedAxios.get.mockImplementation((url) => {
      if (url.includes("/Prescription")) {
        return Promise.resolve({
          data: mockPrescriptions,
          status: 200,
          statusText: "OK",
          headers: {},
          config: { url } as any,
        } as any);
      }
      if (url.includes("/Patient")) {
        return Promise.resolve({
          data: mockPatients,
          status: 200,
          statusText: "OK",
          headers: {},
          config: { url } as any,
        } as any);
      }
      if (url.includes("/Medication")) {
        return Promise.resolve({
          data: mockMedications,
          status: 200,
          statusText: "OK",
          headers: {},
          config: { url } as any,
        } as any);
      }
      return Promise.reject({
        response: {
          status: 404,
          statusText: "Not Found",
          headers: {},
          config: { url } as any,
        },
      });
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test("affiche le chargement initial", () => {
    render(<Prescriptions />);
    expect(
      screen.getByText(/Chargement des prescriptions/i)
    ).toBeInTheDocument();
  });
});
