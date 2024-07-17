import { FC } from "react";

import SearchResults from "./SearchResults/SearchResults";

const ResultsPage: FC = () => {
  return (
    <>
      <h1 className="title">Results</h1>
      <br />
      <SearchResults></SearchResults>
    </>
  );
};

export default ResultsPage;
