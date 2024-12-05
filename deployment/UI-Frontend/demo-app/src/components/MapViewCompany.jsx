import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon, useMapEvent } from 'react-leaflet';
import viviendasData from "../data/viviendas_con_servicios.json";
import terrenosData from "../data/terrenos_con_servicios.json";
import region from "./mockdata";

const MapViewCompany = () => {
    // Nueva estructura de la región

    const viviendas = Object.keys(viviendasData.ID_Vivienda).map((key) => ({
        id: viviendasData.ID_Vivienda[key],
        coordinates: viviendasData.Coordenadas[key],
        district: viviendasData.Distrito[key],
        type: viviendasData.Tipo[key]
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
        // console.log(viviendas)
        console.log(terrenos)
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

                {/* Renderizar polígonos a partir del JSON */}
                {terrenos.features
                    ?.filter((feature) => Array.isArray(feature.geometry.coordinates[0]))
                    .map((feature, index) => (
                        <Polygon
                            key={feature.properties.ID_Terreno || `feature-${index}`}
                            positions={feature.geometry.coordinates[0].map(([lng, lat]) => [lat, lng])} // Convertir de [lng, lat] a [lat, lng]
                            color="green"
                        >
                            <Popup>
                                Zona Construible {index + 1}
                                <br />
                                <strong>ID:</strong> {feature.properties.ID_Terreno}
                                <br />
                                <strong>Superficie:</strong> {feature.properties["Superficie (m²)"]} m²
                            </Popup>
                        </Polygon>
                    ))}


                {/* Renderizar polígonos de zonas construibles */}
                {region.buildables.map((buildable, index) => (
                    <Polygon
                        key={`buildable-${index}`}
                        positions={buildable.coords}
                        color="green"
                    >
                        <Popup>Zona Construible {index + 1}</Popup>
                    </Polygon>
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
            { showHideButton && <button onClick={togglePolygonVisibility} style={{ marginTop: '10px', padding: '10px 20px' }}>
                {polygonVisible ? 'Ocultar Polígono' : 'Mostrar Polígono'}
            </button>}
        </div>
    );
};

export default MapViewCompany;
