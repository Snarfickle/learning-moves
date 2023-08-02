import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import UserContext from "../../contexts/UserContext";

const LogOut = () => {
    const navigate = useNavigate();
    const { setUser } = useContext(UserContext);

    useEffect(() => {    
        const logOut = async () => {
            
            const logOutUrl = 'http://localhost:8000/token';
            const fetchConfig = {
                method:"DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: 'include',
            };
            try {
                const response = await fetch(logOutUrl, fetchConfig);
                if (!response.ok) {
                    throw new Error("logout failed!");
                } else {
                    setUser(null);
                }
            } catch (error) {
                console.log(error);
            } finally {
                navigate("/");
            }
        };
        logOut();
    }, [navigate, setUser]);

    return (
        <div>logging out...</div>
    )
};

export default LogOut;
