# Specification Document

## 1. Introduction

### Project Overview
Applying the results of my master's thesis in a real-world application as part of my first research paper.

### Purpose of the Document
This document will serve as my documentation and technical markdown about the development of this project.

## 2. Project Scope

### Objectives
- Create a mental health monitoring system for hospital patients with NLP capabilities.
- Include entertainment and spiritual content to serve as a hub for all the patients.

### Stakeholders
- Omar Embarki
- Supervisor: Merim Alaifa

## 3. Functional Requirements

### Client Side
- Login and Logout
- Sentiment and adding comments
- Chat with a chatbot to assess the emergency level
- Random facts and Quran verses to keep the religious side up
- Emergency call button

### Admin Side
- Patient management
- By-patient comment management
- By-patient chatbot messaging assessment
- Emergency listener
- Emergency history and response status

### User Stories or Use Cases

#### Client Side
- As a patient, I want to log in and log out securely so that my information is protected.
- As a patient, I want to add comments and receive sentiment analysis so that I can monitor my mental health.
- As a patient, I want to chat with a chatbot to assess my emergency level and receive immediate assistance if needed.
- As a patient, I want to receive random facts and Quran verses to maintain my spiritual well-being.
- As a patient, I want to have access to an emergency call button so that I can get help quickly in critical situations.

#### Admin Side
- As an admin, I want to manage patient information so that all data is up to date and accurate.
- As an admin, I want to manage comments by patients to monitor and respond to their needs.
- As an admin, I want to assess chatbot messages by patients to evaluate the urgency of their situation.
- As an admin, I want to listen to emergency calls and track their history and response status to ensure timely intervention.

## 4. Non-Functional Requirements

### Performance
- The system should respond to user inputs within 2 seconds.

### Usability
- The interface should be user-friendly and accessible to patients with various levels of technical expertise.

### Reliability
- The system should have an uptime of 99.9% to ensure availability for patients and administrators.

### Security
- Implement secure authentication and authorization to protect patient data.
- Ensure data encryption both in transit and at rest.

## 5. Technical Requirements

### Technology Stack
- Frontend: Flutter
- Backend: Flask RESTful API
- Database: PostgreSQL
- NLP: TensorFlow, Hugging Face

### System Architecture
Provide an overview of the system architecture, including diagrams if necessary.

## 6. Data Requirements

### Database Design
- Tables for users, comments, and emergency history.
- Relationships between users and their comments, as well as emergency events.

### Data Migration
Detail any data migration needs from existing systems.

## 7. User Interface Requirements

### Design Mockups
Include design mockups or wireframes for key screens.

### User Experience
Outline the UX principles and guidelines to follow.

## 8. Project Management

### Timeline
Provide a timeline with key milestones and deadlines.

### Budget
Outline the budget considerations and constraints.

### Risks
Identify potential risks and mitigation strategies.

## 9. Appendices

### Glossary
Include a glossary of terms used in the document.

### References
List any references or resources used in creating the document.
