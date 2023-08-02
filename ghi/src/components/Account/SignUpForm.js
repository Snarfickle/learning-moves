import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const SignUpForm = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loginSuccess, setLoginSuccess] = useState(false);
    const [loginError, setLoginError] = useState(false);

    // useEffect(() => { async function checkUsername () {
    //     const url = ''
    // } }) I want to use this to check for existing usernames. I will need to create a list of usernames to check with. 

    const handleSubmit = async (e) => {
        e.preventDefault();
        const data = {
            username,
            email,
            password,
        }
        

        const loginFormURL = 'http://localhost:8000/accounts';

        const fetchConfig = {
            method:"POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
            },
        };

        const response = await fetch(loginFormURL, fetchConfig);

        if (response.ok) {
            setEmail('');
            setUsername('');
            setPassword('');
            navigate('/');
            // setLoginError(false);
            // setLoginSuccess(true);
        } else {
            setLoginError(true);
            console.log("login error!");
        }
        
    }

    function handleUsernameChange(e) {
        const value = e.target.value;
        setUsername(value);
    }
    function handleEmailChange(e) {
        const value = e.target.value;
        setEmail(value);
    }
    function handlePasswordChange(e) {
        const value = e.target.value;
        setPassword(value);
    }

    return (
        <div>
            <h2> Create an account</h2>
            <div>
                <form onSubmit={handleSubmit}>
                    <div>
                        <input value={username} onChange={handleUsernameChange} placeholder="Username" required type="text" name="username" id="username" />
                    </div>
                    <div>
                        <input value={email} onChange={handleEmailChange} placeholder="email" required type="email" name="email" id="email" />
                    </div>
                    <div>
                        <input value={password} onChange={handlePasswordChange} placeholder="password" required type="text" name="password" id="password" />
                    </div>
                    <button>Create Account</button>
                </form>
            </div>
        </div>
    );
}

export default SignUpForm;
