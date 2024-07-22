import React from 'react';
import BrowseResults from './BrowseResults/BrowseResults';

const BrowsePage: React.FC = () => {
  return (
    <div style={{ margin: '20px' }}>
      <h1>Browse All Jobs</h1>
      <BrowseResults />
    </div>
  );
};

export default BrowsePage;
