import React from 'react';
import './FeaturesPage.css';
import slideImage from '../../assets/images/slide1.png'; 

const FeaturesPage: React.FC = () => {
    return (
        <div className="features-container">
            <h1>Features</h1>
            <ul>
                <li><strong>AI-Powered Job Recommendations:</strong> Tailored job recommendations based on your skills, experience, and preferences.</li>
                <li><strong>Responsive Web Design:</strong> A sleek and intuitive user interface that works seamlessly on both desktop and mobile devices.</li>
                <li><strong>Dark/Light Mode Toggle:</strong> Switch between themes based on your preferences for a personalized browsing experience.</li>
                <li><strong>Real-Time Job Listings:</strong> Up-to-date job listings aggregated from reliable sources using the Remotive API.</li>
                <li><strong>Skill-Based Filtering:</strong> Use our autocomplete and chip selection feature to filter jobs by specific skills and categories.</li>
                <li><strong>Open-Source Development:</strong> Our project is open-source. You can view and contribute to our project on <a href="https://github.com/GomeChas/JHAIWT" target="_blank" rel="noopener noreferrer">GitHub</a>.</li>
            </ul>
            <img src={slideImage} alt="Slide 1" style={{ width: '100%', marginTop: '20px' }} />
        </div>
    );
};

export default FeaturesPage;