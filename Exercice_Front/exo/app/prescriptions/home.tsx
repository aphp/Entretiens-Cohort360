import type { Route } from "./+types/home";

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  const res = await fetch(`http://localhost:8000/Prescription`);
  const patients = await res.json();
  return patients;
}

export function HydrateFallback() {
  return <p>Chargement des prescriptions...</p>;
}


export default function PrescriptionList({
  loaderData,
}: Route.ComponentProps) {

  return (
    <main >
      <h1>Les prescriptions</h1>
      <table>
        <thead>
          <th>id</th>
          <th>Patient</th>
          <th>Médicament</th>
          <th>Etat</th>
          <th>Début</th>
          <th>Fin</th>
          <th>Commentaire</th>
        </thead>
        {loaderData.map(p => {
          return (
            <tr>
              <td>{p.id}</td>
              <td>{p.patient}</td>
              <td>{p.medication}</td>
              <td>{p.status}</td>
              <td>{p.begin_date}</td>
              <td>{p.end_date}</td>
              <td>{p.comment}</td>
            </tr>
          )
        })}
      </table>
    </main>
  );
}

