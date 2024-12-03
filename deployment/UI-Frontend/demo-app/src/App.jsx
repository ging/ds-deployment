// src/App.jsx
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Navbar, Container, Row, Col } from 'react-bootstrap';
import MapView from './components/MapView';
import Form from './components/Form'
import Logo from './assets/logo.jpg';

const App = () => {
  return (
    <div className="d-flex flex-column min-vh-100">
      {/* Navbar */}
      <Navbar bg="dark" variant="dark">
        <Container fluid className="d-flex justify-content-between align-items-center">
          {/* Título de la app */}
          <Navbar.Brand href="#home">BuildMyMap</Navbar.Brand>

          {/* Imagen como link */}
          <a href="https://www.google.com" target="_blank" rel="noopener noreferrer">
            <img
              src= {Logo}
              alt="Google"
              className="img-fluid"
              style={{ height: '30px' }}
            />
          </a>
        </Container>
      </Navbar>

      {/* Body con dos secciones */}
      <Container fluid className="flex-grow-1 py-3">
        <Row>
          {/* Sección 1 */}
          <Col md={5} className="p-3">
            <h4 style={{ height: '4vh', width: '105vh' }}>Sección 1</h4>
            <Form />
          </Col>
          {/* Sección 2 con el componente MapView */}
          <Col md={7} className="p-3">
            <h4>Interactive Map</h4>
            <MapView />
          </Col>
        </Row>
      </Container>

      {/* Footer */}
      <footer className="bg-dark text-white text-center py-3">
        <p>© 2024 BuildMyMap</p>
      </footer>
    </div>
  );
};

export default App;
