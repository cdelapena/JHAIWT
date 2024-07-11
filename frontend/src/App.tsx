import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./Pages/Home/Home";
import "./App.css";
import { ThemeProvider } from "@mui/material/styles";
import theme from "./theme";

const App = () => {
  return (
    <ThemeProvider theme={theme}>
    <BrowserRouter>
      <Routes>
        <Route index path="/" element={<Home />} />
        <Route path="/path1" element={<Home />} />
        <Route path="/path2" element={<Home />} />
      </Routes>
    </BrowserRouter>
    </ThemeProvider>
  );
};

export default App
