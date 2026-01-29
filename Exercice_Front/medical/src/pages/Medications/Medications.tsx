import React, { useEffect, useState } from "react";
import axios from "axios";
import { BASE_URL_PYTHON } from "../../config/config";

// Définir le type pour une Medication
interface Medication {
  id: number;
  code: string;
  label: string;
  status: string;
}

const Medications: React.FC = () => {
  const [medications, setMedications] = useState<Medication[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Appeler l'API pour récupérer les Medications
  useEffect(() => {
    const fetchMedications = async () => {
      try {
        const response = await axios.get<Medication[]>(
          `${BASE_URL_PYTHON}/Medication`
        );
        setMedications(response.data);
        setLoading(false);
      } catch (err) {
        setError("Erreur lors du chargement des prescriptions.");
        setLoading(false);
      }
    };

    fetchMedications();
  }, []);

  // Affichage en cas de chargement ou d'erreur
  if (loading) return <p>Chargement des Medications...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h1>Liste des Medications</h1>
      <table>
        <thead>
          <tr>
            <th>Code</th>
            <th>Label</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody>
          {medications.map((medication) => (
            <tr key={medication.id}>
              <td>{medication.code}</td>
              <td>{medication.label}</td>
              <td>{medication.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Medications;
