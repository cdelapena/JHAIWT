import React from "react";
import SearchResults from "./SearchResults/SearchResults";
import { Button } from "@mui/material";

import "./ResultsPage.css";

const ResultsPage: React.FC = () => {
  return (
    <>
      <div className="results-container">
        <Button variant="outlined" href="/">
          Back to Search
        </Button>
        <h1 className="title">Results</h1>
        <SearchResults />
      </div>
    </>
  );
};

export default ResultsPage;
