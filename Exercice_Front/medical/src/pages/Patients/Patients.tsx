import React, { useEffect, useState } from "react";
import axios from "axios";
import { BASE_URL_PYTHON } from "../../config/config";

interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  birth_date: string;
}

const Patients: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Appeler l'API pour récupérer les prescriptions
  useEffect(() => {
    const fetchPations = async () => {
      try {
        const response = await axios.get<Patient[]>(
          `${BASE_URL_PYTHON}/Patient`
        );
        setPatients(response.data);
        setLoading(false);
      } catch (err) {
        setError("Erreur lors du chargement des prescriptions.");
        setLoading(false);
      }
    };

    fetchPations();
  }, []);

  // Affichage en cas de chargement ou d'erreur
  if (loading) return <p>Chargement des pations...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Liste des Pations</h1>
      <table>
        <thead>
          <tr>
            <th>Nom du Patient</th>
            <th>Prénom du Patient</th>
            <th>Date de naissance</th>
          </tr>
        </thead>
        <tbody>
          {patients.map((patient) => (
            <tr key={patient.id}>
              <td>{patient.first_name}</td>
              <td>{patient.last_name}</td>
              <td>{patient.birth_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Patients;
