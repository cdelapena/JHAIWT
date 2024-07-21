import React from 'react';
import SearchResults from './SearchResults/SearchResults';

const ResultsPage: React.FC = () => {
  return (
    <>
      <h1 className="title">Results</h1>
      <br />
      <SearchResults />
    </>
  );
};

export default ResultsPage;
