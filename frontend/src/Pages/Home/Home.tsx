import { FC } from "react";

import InputForm from "./InputForm/InputForm";
import "./Home.css";

const Home: FC = () => {
  return (
    <div>
      <h1 className="title">Job Hunting AI Web Tool</h1>
      <InputForm />
    </div>
  );
};

export default Home;
