import { FC } from "react";

import { useTheme } from "@mui/material";

import SearchResults from "./SearchResults/SearchResults";

const ResultsPage: FC = () => {
  const theme = useTheme();

  return (
    <>
      <h1
        className="title"
        style={{ color: theme.palette.mode === "dark" ? "white" : "" }}
      >
        Results
      </h1>
      <SearchResults></SearchResults>
    </>
  );
};

export default ResultsPage;
