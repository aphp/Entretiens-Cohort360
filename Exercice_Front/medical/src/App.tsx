import React from "react";
import { ThemeProvider } from "styled-components";
import AppRouter from "./router/AppRouter";
import { theme } from "./config/theme";

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <AppRouter />
      </div>
    </ThemeProvider>
  );
};

export default App;
