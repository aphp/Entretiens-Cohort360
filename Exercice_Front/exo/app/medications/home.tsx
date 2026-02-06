import type { Route } from "./+types/home";

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  const res = await fetch(`http://localhost:8000/Medication`);
  const patients = await res.json();
  return patients;
}

export function HydrateFallback() {
  return <p>Chargement des patients...</p>;
}


export default function MedicationList({
  loaderData,
}: Route.ComponentProps) {

  return (
    <main >
      <h1>Les médicaments</h1>
      <table>
        <thead>
          <th>id</th>
          <th>Code</th>
          <th>Etat</th>
          <th>Nom</th>
        </thead>
        {loaderData.map(p => {
          return (
            <tr>
              <td>{p.id}</td>
              <td>{p.code}</td>
              <td>{p.status}</td>
              <td>{p.label}</td>
            </tr>
          )
        })}
      </table>
    </main>
  );
}

