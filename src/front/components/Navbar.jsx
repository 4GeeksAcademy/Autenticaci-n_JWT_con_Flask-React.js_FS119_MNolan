import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const token = sessionStorage.getItem("token");

  const handleLogout = () => {
    sessionStorage.removeItem("token");
    navigate("/login", { replace: true });
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">JWT Autentification</Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mainNavbar"
          aria-controls="mainNavbar"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>

        <div className="collapse navbar-collapse" id="mainNavbar">
          <div className="ms-auto d-flex align-items-center">
            {!token && (
              <>
                <Link className="btn btn-outline-light me-2" to="/register">Registrate</Link>
                <Link className="btn btn-outline-light me-2" to="/login">Login</Link>
              </>
            )}
            {token && (
              <button className="btn btn-light" onClick={handleLogout}>Cerrar sesión</button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
