import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

function AccountOne() {
    const navigate = useNavigate();
    const [id, setId] = useState();
    const [username, setUserName] = useState();
    const [email, setEmail] = useState();
    const [password, setPassword] = useState();
    const [isAccountLoaded, setIsAccountLoaded] = useState(false);


    const loadAccount = async () => {
        const profileURL = 'http://localhost:8000/accounts/';

        const fetchConfig = { 
            method: "GET",
            headers: {"Content-Type": "application/json"},
            credentials: 'include',
        }
        const response = await fetch(profileURL, fetchConfig);
        if (response.ok) {
            const data = await response.json();
            setId(data.account.id);
            setUserName(data.account.username);
            setEmail(data.account.email);
            setIsAccountLoaded(true);
        } else {
            console.error('Failed to load account');
            setIsAccountLoaded(false);
        }
    };
    useEffect(() => {
        loadAccount();
    }, []);

    return (
        <div className="container mt-10">
            { isAccountLoaded ? (
                <>
                    <h1 className="mb-4">Account Information</h1>
                    <div>
                        <Link to={"edit"}>Edit account information</Link>
                        </div>
                    <div className="card">
                        <div className="card-body">
                            <ul className="list-group list-group-flush">
                                <li className="list-group-item">Username: {username}</li>
                                <li className="list-group-item">Email: {email}</li>
                            </ul>
                        </div>
                    </div>
                </>
            ) : (
                <div className="alert alert-warning" role="alert">
                    Please log in at the main page!
                </div>
            )}
        </div>
    )
}
export default AccountOne;
