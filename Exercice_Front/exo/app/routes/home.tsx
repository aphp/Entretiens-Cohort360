import type { Route } from "./+types/home";
import { NavLink } from "react-router";


export default function Home({ loaderData }: Route.ComponentProps) {
  return (
    <>
      <h1>Bienvenue</h1>
      <nav>
        <ul>
          <li><NavLink to="/patients">Liste des patients</NavLink></li>
          <li><NavLink to="/medications">Liste des médicaments</NavLink></li>
          <li><NavLink to="/prescriptions">Liste des prescriptions</NavLink></li>
        </ul>
      </nav>
    </>
  );
}
