import React from "react";
import { Outlet, Link, useLocation } from "react-router-dom";
import styled from "styled-components";

const LayoutContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  height: 100%;
  width: 100%;
  margin: 0;
`;
const Header = styled.header`
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
`;

const Nav = styled.nav`
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
`;

const Logo = styled.div`
  font-size: 1.5rem;
  font-weight: bold;
  color: #2563eb;

  a {
    color: inherit;
    text-decoration: none;
  }
`;

const NavLinks = styled.div`
  display: flex;
  gap: 2rem;
  align-items: center;

  a {
    color: #4b5563;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: all 0.2s ease;

    &:hover {
      color: #2563eb;
      background-color: #f3f4f6;
    }

    &.active {
      color: #2563eb;
      font-weight: 600;
      background-color: #eff6ff;
    }
  }
`;

const Main = styled.main`
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
`;

const Footer = styled.footer`
  background-color: #1f2937;
  color: #ffffff;
  padding: 2rem;
  text-align: center;
  width: 100%;
  margin: 0 auto;
`;

const FooterContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const Layout: React.FC = () => {
  const location = useLocation();

  return (
    <LayoutContainer>
      <Header>
        <Nav>
          <Logo>
            <Link to="/">Exercice Front-End</Link>
          </Logo>
          <NavLinks>
            <Link to="/" className={location.pathname === "/" ? "active" : ""}>
              Accueil
            </Link>
            <Link
              to="/patients"
              className={location.pathname === "/patients" ? "active" : ""}
            >
              Patients
            </Link>
            <Link
              to="/medications"
              className={location.pathname === "/medications" ? "active" : ""}
            >
              Medications
            </Link>
            <Link
              to="/prescriptions"
              className={location.pathname === "/prescriptions" ? "active" : ""}
            >
              Prescriptions
            </Link>
          </NavLinks>
        </Nav>
      </Header>

      <Main>
        <Outlet />
      </Main>

      <Footer>
        <FooterContent>
          <p>&copy; {new Date().getFullYear()} Mon Application React.</p>
          <p>
            <Link to="/" style={{ color: "#ffffff", margin: "0 1rem" }}>
              Accueil
            </Link>
            <Link to="/patients" style={{ color: "#ffffff", margin: "0 1rem" }}>
              Patients
            </Link>
            <Link
              to="/medications"
              style={{ color: "#ffffff", margin: "0 1rem" }}
            >
              Medications
            </Link>
            <Link
              to="/prescriptions"
              style={{ color: "#ffffff", margin: "0 1rem" }}
            >
              Prescriptions
            </Link>
          </p>
        </FooterContent>
      </Footer>
    </LayoutContainer>
  );
};

export default Layout;
