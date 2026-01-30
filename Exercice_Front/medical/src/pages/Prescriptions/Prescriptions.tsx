import React, { useEffect, useState } from "react";
import axios from "axios";
import Modal from "react-modal";
import { BASE_URL_PYTHON } from "../../config/config";

interface Prescription {
  id: number;
  patient_name: string;
  patient: number;
  medication_code: string;
  medication: number;
  prescription_start_date: string;
  prescription_end_date: string;
  presscription_status: string;
  commentaire?: string;
}

const Prescriptions: React.FC = () => {
  const [prescriptions, setPrescriptions] = useState<Prescription[]>([]);
  const [patients, setPatients] = useState<
    { id: number; last_name: string; first_name: string }[]
  >([]);
  const [medications, setMedications] = useState<
    { id: number; code: string }[]
  >([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [statusFilter, setStatusFilter] = useState<string>("");
  const [nameFilter, setNameFilter] = useState<string>("");
  const [startDateFilter, setStartDateFilter] = useState<string>("");
  const [endDateFilter, setEndDateFilter] = useState<string>("");

  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState<Partial<Prescription>>({});

  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => {
    setIsModalOpen(false);
    setIsEditing(false);
    setFormData({});
  };

  const fetchPrescriptions = async () => {
    setLoading(true);
    setError(null);

    try {
      const params: Record<string, string> = {};
      if (statusFilter) params.status = statusFilter;
      if (nameFilter) params.nom = nameFilter;
      if (startDateFilter) params.active_period_min = startDateFilter;
      if (endDateFilter) params.active_period_max = endDateFilter;

      // Effectuer la requête avec les paramètres
      const response = await axios.get<Prescription[]>(
        `${BASE_URL_PYTHON}/Prescription`,
        { params }
      );

      setPrescriptions(response.data);
    } catch (err) {
      setError("Erreur lors du chargement des prescriptions.");
    } finally {
      setLoading(false);
    }
  };
  const fetchPatients = async () => {
    try {
      const response = await axios.get<
        { id: number; first_name: string; last_name: string }[]
      >(`${BASE_URL_PYTHON}/Patient`);
      setPatients(response.data);
    } catch (err) {
      setError("Erreur lors du chargement des patients.");
    }
  };
  useEffect(() => {
    fetchPatients();
  }, []);
  const fetchMedications = async () => {
    try {
      const response = await axios.get<{ id: number; code: string }[]>(
        `${BASE_URL_PYTHON}/Medication`
      );
      setMedications(response.data);
    } catch (err) {
      setError("Erreur lors du chargement des Medication.");
    }
  };
  useEffect(() => {
    fetchMedications();
  }, []);
  const addPrescription = async () => {
    try {
      const response = await axios.post<Prescription>(
        `${BASE_URL_PYTHON}/Prescription`,
        {
          ...formData,
        }
      );
      setPrescriptions([...prescriptions, response.data]);
      setFormData({});
    } catch (err: any) {
      if (err?.response?.data) {
        const errorData = err.response.data;
        let element = "";
        // Parcourir toutes les propriétés de l'objet data
        Object.keys(errorData).forEach((field) => {
          if (Array.isArray(errorData[field])) {
            // Ajouter tous les messages d'erreur de ce champ
            errorData[field].forEach((message: string) => {
              element += `${field}: ${message}`;
            });
          }
        });

        window.alert(`Erreur :\n${element}`);
      } else {
        window.alert("Erreur lors de l'ajout de la prescription.");
      }
    }
  };

  const updatePrescription = async () => {
    if (!editingId) return;

    try {
      const response = await axios.put<Prescription>(
        `${BASE_URL_PYTHON}/Prescription/${editingId}`,
        {
          ...formData,
        }
      );
      console.log("Response data:", formData);
      setPrescriptions(
        prescriptions.map((prescription) =>
          prescription.id === editingId ? response.data : prescription
        )
      );
      setIsEditing(false);
      setFormData({});
    } catch (err: any) {
      if (err?.response?.data) {
        const errorData = err.response.data;
        let element = "";
        // Parcourir toutes les propriétés de l'objet data
        Object.keys(errorData).forEach((field) => {
          if (Array.isArray(errorData[field])) {
            // Ajouter tous les messages d'erreur de ce champ
            errorData[field].forEach((message: string) => {
              element += `${field}: ${message}`;
            });
          }
        });

        window.alert(`Erreur :\n${element}`);
      } else {
        window.alert("Erreur lors de la mise à jour de la prescription.");
      }
    }
  };

  const deletePrescription = async (id: number) => {
    try {
      await axios.delete(`${BASE_URL_PYTHON}/Prescription/${id}`);
      setPrescriptions(
        prescriptions.filter((prescription) => prescription.id !== id)
      );
    } catch (err) {
      setError("Erreur lors de la suppression de la prescription.");
    }
  };

  // Appeler l'API lorsque les filtres changent
  useEffect(() => {
    fetchPrescriptions();
  }, [statusFilter, nameFilter, startDateFilter, endDateFilter]);

  // Affichage en cas de chargement ou d'erreur
  if (loading) return <p>Chargement des prescriptions...</p>;
  if (error) return <p>{error}</p>;
  return (
    <div>
      <h1>Liste des Prescriptions</h1>

      {/* Filtres */}
      <div className="filters-container">
        <h2>Filtres</h2>
        <div className="filters">
          <div className="filter">
            <label>
              Statut :
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="">Tous</option>
                <option value="valide">Valide</option>
                <option value="en_attente">En attente</option>
                <option value="suppr">Supprimé</option>
              </select>
            </label>
          </div>

          <div className="filter">
            <label>
              Nom du patient :
              <input
                type="text"
                value={nameFilter}
                onChange={(e) => setNameFilter(e.target.value)}
                placeholder="Rechercher par nom"
              />
            </label>
          </div>
          <div className="filter">
            <label>
              Date de début :
              <input
                type="date"
                value={startDateFilter}
                onChange={(e) => setStartDateFilter(e.target.value)}
              />
            </label>
          </div>
          <div className="filter">
            <label>
              Date de fin :
              <input
                type="date"
                value={endDateFilter}
                onChange={(e) => setEndDateFilter(e.target.value)}
              />
            </label>
          </div>
        </div>
      </div>
      <div className="container-button">
        <button onClick={openModal}>Ajouter une Prescription</button>
      </div>
      <Modal
        isOpen={isModalOpen}
        onRequestClose={closeModal}
        contentLabel="Formulaire Prescription"
        style={{
          content: {
            top: "50%",
            left: "50%",
            right: "auto",
            bottom: "auto",
            marginRight: "-50%",
            transform: "translate(-50%, -50%)",
            width: "50%",
          },
        }}
      >
        <h2>
          {isEditing ? "Modifier une Prescription" : "Ajouter une Prescription"}
        </h2>
        <form
          className="modal-form"
          onSubmit={(e) => {
            e.preventDefault();
            isEditing ? updatePrescription() : addPrescription();
            closeModal();
          }}
        >
          <div className="form-group">
            <label>
              Patient :
              <select
                value={formData.patient || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    patient: parseInt(e.target.value),
                  })
                }
                required
              >
                <option value="">Sélectionner un patient</option>
                {patients.map((patient) => (
                  <option key={patient.id} value={patient.id}>
                    {patient.first_name + " " + patient.last_name}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <div className="form-group">
            <label>
              Médicament :
              <select
                value={formData.medication || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    medication: parseInt(e.target.value),
                  })
                }
                required
              >
                <option value="">Sélectionner un médicament</option>
                {medications.map((medication) => (
                  <option key={medication.id} value={medication.id}>
                    {medication.code}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <div className="form-group">
            <label>
              Date de début :
              <input
                type="date"
                value={
                  formData.prescription_start_date
                    ? new Date(formData.prescription_start_date)
                        .toISOString()
                        .split("T")[0]
                    : ""
                }
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    prescription_start_date: e.target.value,
                  })
                }
                required
              />
            </label>
          </div>
          <div className="form-group">
            <label>
              Date de fin :
              <input
                type="date"
                value={
                  formData.prescription_end_date
                    ? new Date(formData.prescription_end_date)
                        .toISOString()
                        .split("T")[0]
                    : ""
                }
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    prescription_end_date: e.target.value,
                  })
                }
                required
              />
            </label>
          </div>
          <div className="form-group">
            <label>
              Statut :
              <select
                value={formData.presscription_status || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    presscription_status: e.target.value,
                  })
                }
                required
              >
                <option value="">Sélectionner un statut</option>
                <option value="valide">Valide</option>
                <option value="en_attente">En attente</option>
                <option value="suppr">Supprimé</option>
              </select>
            </label>
          </div>
          <div className="form-group">
            <label>
              Commentaire :
              <textarea
                value={formData.commentaire || ""}
                onChange={(e) =>
                  setFormData({ ...formData, commentaire: e.target.value })
                }
              />
            </label>
          </div>
          <button type="submit">{isEditing ? "Modifier" : "Ajouter"}</button>
          <button type="button" onClick={closeModal}>
            Annuler
          </button>
        </form>
      </Modal>

      {/* Tableau des prescriptions */}
      <table>
        <thead>
          <tr>
            <th>Nom du patient</th>
            <th>Code medicament</th>
            <th>Date de début de prescription</th>
            <th>Date de fin de prescription</th>
            <th>Statut de la prescription</th>
            <th>Commentaire</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {prescriptions.map((prescription) => (
            <tr key={prescription.id}>
              <td>{prescription.patient_name}</td>
              <td>{prescription.medication_code}</td>
              <td>
                {new Date(
                  prescription.prescription_start_date
                ).toLocaleDateString()}
              </td>
              <td>
                {new Date(
                  prescription.prescription_end_date
                ).toLocaleDateString()}
              </td>
              <td>{prescription.presscription_status}</td>
              <td>{prescription.commentaire || "N/A"}</td>
              <td>
                <button
                  onClick={() => {
                    setIsEditing(true);
                    setEditingId(prescription.id);
                    setFormData(prescription);
                    openModal();
                  }}
                >
                  Modifier
                </button>
                <button onClick={() => deletePrescription(prescription.id)}>
                  Supprimer
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default Prescriptions;
