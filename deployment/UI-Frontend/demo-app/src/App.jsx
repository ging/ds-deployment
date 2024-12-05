// src/App.jsx
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Navbar, Container, Row, Col, Button } from 'react-bootstrap';
import MapViewClient from './components/MapViewClient';
import MapViewCompany from './components/MapViewCompany';
import MapView from './components/MapView';
import Form from './components/Form';
import Logo from './assets/logo.jpg';

const App = () => {
  // Estados para controlar las vistas
  const [currentView, setCurrentView] = useState("MapView"); // Vista inicial
  const [showClientView, setShowClientView] = useState(true); // Alternar entre Cliente y Empresa
  

  // Manejador para el envío del formulario
  const handleFormSubmit = (event) => {
    event.preventDefault(); // Prevenir el comportamiento por defecto
    if (currentView === "MapView") {
      setCurrentView("MapViewClient"); // Cambiar a la vista del cliente
    }
  };

  // Alternar entre MapViewClient y MapViewCompany
  const toggleView = () => {
    setShowClientView((prev) => !prev);
  };

  return (
    <div className="d-flex flex-column min-vh-100">
      {/* Navbar */}
      <Navbar bg="dark" variant="dark">
        <Container fluid className="d-flex justify-content-between align-items-center">
          <Navbar.Brand href="#home">CivitAIs</Navbar.Brand>
          <a href="https://www.google.com" target="_blank" rel="noopener noreferrer">
            <img
              src={Logo}
              alt="Google"
              className="img-fluid"
              style={{ height: '30px' }}
            />
          </a>
        </Container>
      </Navbar>

      {/* Botón para cambiar de vista */}
      <Container fluid className="text-center py-3">
        <Button variant="primary" onClick={toggleView}>
          Cambiar a {showClientView ? "Vista Empresa" : "Vista Cliente"}
        </Button>
      </Container>

      {/* Body con dos secciones */}
      <Container fluid className="flex-grow-1 py-3">
        <Row>
          {/* Sección 1 */}
          <Col md={5} className="p-3">
            <h4 style={{ height: '4vh', width: '105vh' }}>Busca una región</h4>
            <Form onSubmit={handleFormSubmit} />
          </Col>
          {/* Sección 2 con vista dinámica */}
          <Col md={7} className="p-3">
            <h4>Interactive Map</h4>
            {currentView === "MapView" && <MapView />}
            {currentView === "MapViewClient" && showClientView && <MapViewClient />}
            {currentView === "MapViewClient" && !showClientView && <MapViewCompany />}
          </Col>
        </Row>
      </Container>

      {/* Footer */}
      <footer className="bg-dark text-white text-center py-3">
        <p>© 2024 CivitAIs</p>
      </footer>
    </div>
  );
};

export default App;
