import { FC, useContext } from "react";

import { useTheme } from "@mui/material";

import InputForm from "./InputForm/InputForm";
import { ThemeContext } from "../../shared/contexts";
import "./Home.css";

const Home: FC = () => {
  const theme = useTheme();
  const colorMode = useContext(ThemeContext);

  return (
    <div>
      <h1 className="title" onClick={colorMode.toggleColorMode}>
        Job Hunting AI Web Tool
      </h1>
      <br />
      <InputForm />
    </div>
  );
};

export default Home;
