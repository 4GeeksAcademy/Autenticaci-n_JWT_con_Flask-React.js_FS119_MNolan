import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Private() {

    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [loger, setLoger] = useState("");

    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    useEffect(() => {
        const token = sessionStorage.getItem("token");
        if (!token) {
            navigate("/login", { replace: true });
            return;
        }

        fetch(`${backendUrl}/api/private`, {
            method: "GET",
            headers: { Authorization: "Bearer " + token },
        })

            .then(async (resp) => {
                if (!resp.ok) {
                    sessionStorage.removeItem("token");
                    navigate("/login", { replace: true });
                    return;
                }
                const data = await resp.json();
                setLoger(` ${data.name}`);
                setLoading(false);
            })
            .catch(() => {
                sessionStorage.removeItem("token");
                navigate("/login", { replace: true });
            });
    }, [navigate]);

    if (loading) return <div>Validando...</div>;

    return (
        <div className="container-fluid py-4">

            <div className="row justify-content-center">
                <div className="col-12 col-sm-10 col-md-8 col-lg-6">
                    <div className="card shadow-sm">
                        <div className="card-header text-center bg-white">
                            <h2 className="h4 mb-1">Zona privada</h2>
                            <p className="mb-0 small">Bienvenid@ <strong>{loger}</strong></p>
                        </div>
                        <div className="card-body text-center">
                            <img
                                src="src/front/assets/img/BG4j.gif"
                                className="img-fluid rounded mx-auto d-block mb-3"
                            />
                            <p className="mb-3 small text-muted">
                                {loger} mi amigo de aqui arriba es <strong>Hipnosapo</strong>.<br />
                                Hipnosapo es feliz porque te encanta este proyecto y, antes de pulsar el botón,
                                sabrás que quieres que su desarrollador tenga un APROBADO ^.^U.
                            </p>
                        </div>
                        <div className="card-footer text-center bg-white">
                            <button
                                className="btn btn-secondary"
                                onClick={() => {
                                    sessionStorage.removeItem("token");
                                    navigate("/login");
                                }}
                            >
                                Cerrar sesión
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}