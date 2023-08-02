import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import UserContext from "../../contexts/UserContext";

function LoginForm () {
    const { setUser } = useContext(UserContext);
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const loginFormURL = 'http://localhost:8000/token';
        const formParams = new URLSearchParams();
        formParams.append('username', username);
        formParams.append('password', password);

        const fetchConfig = {
            method:"POST",
            body: formParams,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            credentials: 'include',
        };
        const response = await fetch(loginFormURL, fetchConfig);


        if (response.ok) {
            const data = await response.json();
            setPassword('');
            setUsername('');
            setUser(data);
            navigate('/');
        } else {
            console.log("login failed.")
        };
    }

    function handlePasswordChange(e) {
        const value = e.target.value;
        setPassword(value);
    }
    function handleUsernameChange(e) {
        const value = e.target.value;
        setUsername(value);
    }


    return (
        <div>
        <h1>Login form</h1>
        <form onSubmit={handleSubmit}>
            <div>
                <input value={username} onChange={handleUsernameChange} placeholder="Username" required type="text" name="username" id="username" />
            </div>
            <div>
                <input value={password} onChange={handlePasswordChange} placeholder="Password" required type="password" name="password" id="password" />
            </div>
            <button type="submit">Login</button>
        </form>
        </div>
    )
}

export default LoginForm;
