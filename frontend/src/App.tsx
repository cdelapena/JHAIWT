import { FC, useState, useMemo, useEffect } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { ThemeProvider } from "@mui/material/styles";
import {
  PaletteMode,
  createTheme,
  useMediaQuery,
  CssBaseline,
  ThemeOptions,
} from "@mui/material";

import "./App.css";
import { SearchContext, ThemeContext } from "./shared/contexts";
import Home from "./Pages/Home/Home";
import ResultsPage from "./Pages/ResultsPage/ResultsPage";
import BrowsePage from "./Pages/BrowsePage/BrowsePage";
import { getDesignTokens } from "./shared/colorTheme";
import Navbar from "./components/Navbar";
import { initialSearchValues } from "./shared/constants";
import { SearchInterface } from "./shared/interfaces";

const App: FC = () => {
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
  const [searchValues, setSearchValues] =
    useState<SearchInterface>(initialSearchValues);
  const [mode, setMode] = useState<PaletteMode>(
    prefersDarkMode ? "dark" : "light"
  );

  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
      },
    }),
    []
  );

  useEffect(() => {
    if (mode === "dark") {
      document.body.classList.add("dark");
    } else {
      document.body.classList.remove("dark");
    }
  }, [mode]);

  const theme = useMemo(
    () => createTheme(getDesignTokens(mode) as ThemeOptions),
    [mode]
  );

  return (
    <SearchContext.Provider value={{ searchValues, setSearchValues }}>
      <ThemeContext.Provider value={colorMode}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <BrowserRouter>
            <Navbar />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/results" element={<ResultsPage />} />
              <Route path="/browse" element={<BrowsePage />} />
            </Routes>
          </BrowserRouter>
        </ThemeProvider>
      </ThemeContext.Provider>
    </SearchContext.Provider>
  );
};

export default App;
