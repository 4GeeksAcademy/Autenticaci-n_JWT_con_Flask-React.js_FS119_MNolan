/*
import { React, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export const Login = () => {

    const { store, dispatch } = useGlobalReducer()
    const navigate = useNavigate();

    const login = async (username, password) => {
        const resp = await fetch(`https://your_api.com/token`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        })

        if (!resp.ok) throw Error("There was a problem in the login request")

        if (resp.status === 401) {
            throw ("Invalid credentials")
        }
        else if (resp.status === 400) {
            throw ("Invalid email or password format")
        }
        const data = await resp.json()
        // Guarda el token en la localStorage
        // También deberías almacenar el usuario en la store utilizando la función setItem
        localStorage.setItem("jwt-token", data.token);

        return data
    }




}
*/