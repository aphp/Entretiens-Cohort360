import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "../components/layout/Layout";
import Home from "../pages/Home/Home";
import Patients from "../pages/Patients/Patients";
import Medications from "../pages/Medications/Medications";
import Prescriptions from "../pages/Prescriptions";

const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
        </Route>
        <Route path="/patients" element={<Layout />}>
          <Route index element={<Patients />} />
        </Route>
        <Route path="/medications" element={<Layout />}>
          <Route index element={<Medications />} />
        </Route>
        <Route path="/prescriptions" element={<Layout />}>
          <Route index element={<Prescriptions />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;
