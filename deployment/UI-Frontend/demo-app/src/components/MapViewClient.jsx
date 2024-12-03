import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon, useMapEvent } from 'react-leaflet';
import viviendasData from "../data/viviendas_con_notas.json";
import terrenosData from "../data/terrenos_con_servicios.json";
import region from "./mockdata";

const MapViewClient = () => {
    // Nueva estructura de la región

    const viviendas = viviendasData.map((vivienda) => ({
        id: vivienda.ID_Vivienda,
        coordinates: vivienda.Coordenadas.split(',').map((coord) => parseFloat(coord.trim())), // Convertir a [lat, lng]
        district: vivienda.Distrito,
        type: vivienda.Tipo,
        school: vivienda.Colegio,
        hospital: vivienda.Hospital,
        park: vivienda.Parque,
        shop: vivienda.Supermercado,
        grade: vivienda.Prediccion_Nota
    }));


    const terrenos = terrenosData.features.map((feature) => ({
        id: feature.properties.ID_Terreno,
        surface: feature.properties["Superficie (m²)"],
        price: feature.properties["Precio (€)"],
        coordinates: feature.geometry.coordinates[0].map(([lat, lng]) => [lat, lng]), // Leaflet necesita [lat, lng]
    }));

    const center = ['40.398337', '-3.702542'];

    // Estado para los marcadores creados por el usuario
    const [userMarkers, setUserMarkers] = useState([]);

    // Estado para controlar la visibilidad del polígono
    const [polygonVisible, setPolygonVisible] = useState(true);
    const [showHideButton, setShowHideButton] = useState(false);

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

                {/* Renderizar el polígono del barrio si está visible */}
                {polygonVisible && (
                    <Polygon positions={region.polygon} color={region.color}>
                        <Popup>{region.name}</Popup>
                    </Polygon>
                )}

                {viviendas
                    .filter((vivienda) => vivienda.coordinates) // Filtrar viviendas con coordenadas válidas
                    .map((vivienda) => (
                        <Marker key={vivienda.id} position={vivienda.coordinates}>
                            <Popup>
                                <strong>Distrito:</strong> {vivienda.district}
                                <br />
                                {/* <strong>ID:</strong> {vivienda.id}
                                <br /> */}
                                <strong>Tipo de Vivienda:</strong> {vivienda.type}
                                <br />
                                <strong>Coordenadas:</strong> {vivienda.coordinates.join(', ')}
                                <br />
                                <strong>Nº Colegios cerca:</strong> {vivienda.school}
                                <br />
                                <strong>Nº Hospitales cerca:</strong> {vivienda.hospital}
                                <br />
                                <strong>Nº Supermercados cerca:</strong> {vivienda.shop}
                                <br />
                                <strong>Nota CivitAIs:</strong> {vivienda.grade}
                            </Popup>
                        </Marker>
                    ))}


                {/* Renderizar marcadores creados por el usuario */}
                {userMarkers.map((marker, index) => (
                    <Marker key={`user-marker-${index}`} position={marker.coords}>
                        <Popup>{marker.name}</Popup>
                    </Marker>
                ))}

                {/* Componente que agrega marcadores en clic */}
                <AddMarkerOnClick />
            </MapContainer>

            {/* Botón para alternar visibilidad del polígono */}
            {showHideButton && <button onClick={togglePolygonVisibility} style={{ marginTop: '10px', padding: '10px 20px' }}>
                {polygonVisible ? 'Ocultar Polígono' : 'Mostrar Polígono'}
            </button>}
        </div>
    );
};

export default MapViewClient;
