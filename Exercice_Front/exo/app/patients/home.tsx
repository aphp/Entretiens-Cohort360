import type { Route } from "./+types/home";

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  const res = await fetch(`http://localhost:8000/Patient`);
  const patients = await res.json();
  return patients;
}

export function HydrateFallback() {
  return <p>Chargement des patients...</p>;
}


export default function PatientList({
  loaderData,
}: Route.ComponentProps) {

  return (
    <main >
      <h1>Les patients</h1>
      <table>
        <thead>
          <th>id</th>
          <th>Prénom</th>
          <th>Nom</th>
          <th>Date de naissance</th>
        </thead>
        {loaderData.map(p => {
          return (
            <tr>
              <td>{p.id}</td>
              <td>{p.first_name}</td>
              <td>{p.last_name}</td>
              <td>{p.birth_date}</td>
            </tr>
          )
        })}
      </table>
    </main>
  );
}

