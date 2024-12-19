// src/components/Form.jsx
import React from 'react';
import { Form, Button } from 'react-bootstrap';

const CustomForm = ({ onSubmit }) => {
  
  return (
    <Form onSubmit={onSubmit}>
      <Form.Group>
        <Form.Label htmlFor="city">Ciudad</Form.Label>
        <Form.Control
          type="text"
          id="city"
          aria-describedby="cityInput"
          placeholder='Introduce aqui tu ciudad'
        />
      </Form.Group>
      <Form.Group className="mb-3" controlId="selectOption">
        <Form.Label>Distrito</Form.Label>
        <Form.Select>
          <option value="opcion0" defaultValue="Elige un distrito"></option>
          <option value="opcion1">Arganzuela</option>
          <option value="opcion2">Centro</option>
          <option value="opcion3">Retiro</option>
          <option value="opcion3">Salamanca</option>
          <option value="opcion3">Chamartin</option>
          <option value="opcion3">Tetuan</option>
          <option value="opcion3">Chamberi</option>
          <option value="opcion3">Fuencarral-El Pardo</option>
          <option value="opcion3">Mocloa-Aravaca</option>
          <option value="opcion3">Latina</option>
          <option value="opcion3">Carabanchel</option>
          <option value="opcion3">Usera</option>
          <option value="opcion3">Puente de Vallecas</option>
          <option value="opcion3">Moratalaz</option>
          <option value="opcion3">Ciudad Lineal</option>
          <option value="opcion3">Hortaleza</option>
          <option value="opcion3">Villaverde</option>
          <option value="opcion3">Villa de Vallecas</option>
          <option value="opcion3">Vicalvaro</option>
          <option value="opcion3">San Blas</option>
          <option value="opcion3">Barajas</option>
        </Form.Select>
      </Form.Group>
      <Button variant="primary" type="submit">
        Buscar
      </Button>
    </Form>
  );
};

export default CustomForm;
