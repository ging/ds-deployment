// src/components/Form.jsx
import React from 'react';
import { Form, Button } from 'react-bootstrap';

const CustomForm = () => {
  return (
    <Form>
      {/* Intervalo 1 */}
      <Form.Group className="mb-3" controlId="interval1">
        <Form.Label>Intervalo 1</Form.Label>
        <Form.Control type="number" placeholder="Ingrese un valor" />
      </Form.Group>

      {/* Intervalo 2 */}
      <Form.Group className="mb-3" controlId="interval2">
        <Form.Label>Intervalo 2</Form.Label>
        <Form.Control type="number" placeholder="Ingrese un valor" />
      </Form.Group>

      {/* Select */}
      <Form.Group className="mb-3" controlId="selectOption">
        <Form.Label>Opciones</Form.Label>
        <Form.Select>
          <option value="opcion1">Opción 1</option>
          <option value="opcion2">Opción 2</option>
          <option value="opcion3">Opción 3</option>
        </Form.Select>
      </Form.Group>

      {/* Botón para enviar */}
      <Button variant="primary" type="submit">
        Enviar
      </Button>
    </Form>
  );
};

export default CustomForm;
