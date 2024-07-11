import React from 'react';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./Pages/Home/Home";
import './App.css';

function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route index path="/" element={<Home />} />
      <Route path="/choose" element={<Home />} />
      <Route path="/adventures" element={<Home />} />
    </Routes>
  </BrowserRouter>
  );
}

export default App;
