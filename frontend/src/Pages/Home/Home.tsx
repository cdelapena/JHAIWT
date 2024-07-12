import InputForm from "./InputForm/InputForm";
import "./Home.css";
import { useTheme } from "@mui/material";

const Home = () => {
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
