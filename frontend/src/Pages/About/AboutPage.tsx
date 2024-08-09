import React from 'react';
import teamPhoto from '../../assets/images/TeamPhoto.jpg';
import './AboutPage.css';

const AboutPage: React.FC = () => {
    return (
        <div className="about-container">
            <h1>About</h1>
            <div className="team-photo-container">
                <img src={teamPhoto} alt="Our Team" className="team-photo" />
            </div>
            <p>This project was developed by Bryan Wu, Chase Gomez, Rocky Cowan, and Chris Dela Pena as part of our CS467 capstone class at Oregon State University, where we collaborated to create an AI-powered job hunting tool. The project leverages modern web technologies such as React, Flask, and Google Cloud, combined with sophisticated input validation, AI-based job recommendation, and text preprocessing techniques.</p>
            <p>Our team members contributed in the following ways:</p>
            <ul>
                <li><strong>React App and Flask API Setup:</strong> Developed the initial React frontend and Flask backend, ensuring smooth integration between them.</li>
                <li><strong>Home and Browse Pages:</strong> Designed and implemented the home and browse all pages where users interact with the job search features.</li>
                <li><strong>Light/Dark Mode Toggle:</strong> Implemented a user preference system for switching between light and dark modes.</li>
                <li><strong>Autocomplete and Chip Selection:</strong> Built intuitive filtering systems to help users refine their job searches.</li>
                <li><strong>AI-Based Job Recommendation:</strong> Developed an AI component that processes user input and job descriptions using TF-IDF vectorization and cosine similarity to provide relevant job recommendations.</li>
                <li><strong>Google Cloud Deployment:</strong> Deployed the application on Google Cloud App Engine for enhanced reliability and scalability.</li>
                <li><strong>Text Preprocessing:</strong> Created backend functionality to improve the relevance of search results by preprocessing input text.</li>
                <li><strong>Code Reviews and Deployment:</strong> Ensured code quality through peer reviews and handled the deployment process.</li>
            </ul>
            <p>The development process involved multiple stages, including initial setup, feature implementation, integration, and deployment. Despite challenges, such as learning new technologies and dealing with deployment issues, we successfully delivered a functional and user-friendly application.</p>
        </div>
    );
};

export default AboutPage;