import { FC } from "react";

import { useTheme } from "@mui/material";

import InputForm from "./InputForm/InputForm";
import "./Home.css";

const Home: FC = () => {
  const theme = useTheme();

  return (
    <>
      <h1
        className="title"
        style={{ color: theme.palette.mode === "dark" ? "white" : "" }}
      >
        Job Hunting AI Web Tool
      </h1>
      <br />
      <InputForm />
    </>
  );
};

export default Home;
