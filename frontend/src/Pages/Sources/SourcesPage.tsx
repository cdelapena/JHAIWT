import React from 'react';
import './SourcesPage.css';

const SourcesPage: React.FC = () => {
    return (
        <div className="sources-container">
            <h1>Sources</h1>
            <p>Our job listings are aggregated from a trusted API provided by Remotive. We use this source to gather up-to-date and relevant job postings:</p>
            <p><a href="https://remotive.com/" target="_blank" rel="noopener noreferrer">Remotive API</a> - Source for job listings and relevant job data.</p>
            <p>We continuously monitor and update our sources to provide you with the most relevant job opportunities.</p>
            
            <h2>Project Repository</h2>
            <p>You can view the source code for this project and contribute to it on GitHub:</p>
            <p><a href="https://github.com/GomeChas/JHAIWT" target="_blank" rel="noopener noreferrer">GitHub Repository</a> - Explore our codebase and contribute to our project.</p>
        </div>
    );
};

export default SourcesPage;