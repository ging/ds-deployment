import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon, useMapEvent } from 'react-leaflet';
import viviendasData from "../data/viviendas_con_servicios.json";

const MapView = () => {

  const [showHideButton, setShowHideButton] = useState(false);

  const viviendas = Object.keys(viviendasData.ID_Vivienda).map((key) => ({
    id: viviendasData.ID_Vivienda[key],
    coordinates: viviendasData.Coordenadas[key],
    district: viviendasData.Distrito[key],
    type: viviendasData.Tipo[key]
  }));

  const center = ['40.41693', '-3.70346'];

  // Estado para los marcadores creados por el usuario
  const [userMarkers, setUserMarkers] = useState([]);

  // Estado para controlar la visibilidad del polígono
  const [polygonVisible, setPolygonVisible] = useState(true);

  // Función para alternar la visibilidad del polígono
  const togglePolygonVisibility = () => {
    setPolygonVisible((prevVisible) => !prevVisible);
    console.log(viviendas)
  };

  // Componente para manejar eventos de clic en el mapa
  const AddMarkerOnClick = () => {
    useMapEvent('click', (e) => {
      const { lat, lng } = e.latlng;
      setUserMarkers((prevMarkers) => [
        ...prevMarkers,
        { coords: [lat, lng], name: `Coordenadas: (${lat.toFixed(5)}, ${lng.toFixed(5)})` }
      ]);
    });
    return null; // Este componente no renderiza nada visible
  };

  return (
    <div>
      <MapContainer
        center={center}
        zoom={13}
        style={{ height: '68vh', width: '105vh' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {/* Componente que agrega marcadores en clic */}
        <AddMarkerOnClick />
      </MapContainer>

      {/* Botón para alternar visibilidad del polígono */}
      { showHideButton && <button onClick={togglePolygonVisibility} style={{ marginTop: '10px', padding: '10px 20px' }}>
        {polygonVisible ? 'Ocultar Polígono' : 'Mostrar Polígono'}
      </button>}
    </div>
  );
};

export default MapView;
