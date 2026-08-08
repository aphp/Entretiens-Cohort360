import { NavLink, Outlet } from "react-router";
// import logo from "./public/logo.avif"

export default function MedicationLayout() {
  return (
    <>
      <header>
        <NavLink to="/">
          <img src="/logo.avif" alt="Logo de l'outil Cohort360" />
        </NavLink>
        L'app qui sauve
      </header>
      <main>
        <Outlet />
      </main>
      <footer>&copy; 2026</footer>
    </>
  );
}

