import { FC } from "react";

import { useTheme } from "@mui/material";

const ResultsPage: FC = () => {
  const theme = useTheme();

  return (
    <>
      <h1
        className="title"
        style={{ color: theme.palette.mode === "dark" ? "white" : "" }}
      >
        Job Hunting AI Web Tool
      </h1>
    </>
  );
};

export default ResultsPage;
