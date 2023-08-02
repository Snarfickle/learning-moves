import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const ProfileView = () => {
    const [id, setId] = useState();
    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();
    const [email, setEmail] = useState();
    const [phoneNumber, setPhoneNumber] = useState();
    const [city, setCity] = useState();
    const [state, setState] = useState();
    const [profilePicture, setProfilePicture] = useState();
    const [aboutMe, setAboutMe] = useState();
    const [isProfileLoaded, setIsProfileLoaded] = useState(false);

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
            setIsProfileLoaded(true);
        } else {
            console.error('Failed to load account');
            setIsProfileLoaded(false);
        }
    };
    useEffect(() => {
        loadAccount();
    }, []);

    const loadProfile = async () => {

        const profileURL = `http://localhost:8000/profiles/${id}`;

        const fetchConfig = { 
            method: "GET",
            headers: {"Content-Type": "application/json"},
            credentials: 'include',
        }
        const response = await fetch(profileURL, fetchConfig);
        
        if (response.ok) {
            const data = await response.json();
            setFirstName(data.first_name);
            setLastName(data.last_name);
            setEmail(data.email);            
            setPhoneNumber(data.phone_number);
            setCity(data.city);
            setState(data.state);
            setProfilePicture(data.profile_picture);
            setAboutMe(data.about_me);
            setIsProfileLoaded(true);
        } else {
            console.error('Failed to load profile');
            setIsProfileLoaded(false);
        }
    }

    useEffect(() => {
        if (id) {
        loadProfile();
        }
    }, [id])

    return (
        <div className="container mt-10">
            { isProfileLoaded ? (
                <>
                    <h1 className="mb-4">Profile Information</h1>
                    <div>
                        <Link to={"edit"}>Edit profile information</Link>
                        </div>
                    <div className="card">
                        <div className="card-body">
                            <ul className="list-group list-group-flush">
                                <li className="list-group-item">First Name: {firstName}</li>
                                <li className="list-group-item">Last Name: {lastName}</li>
                                <li className="list-group-item">Email: {email}</li>
                                <li className="list-group-item">Phone Number: {phoneNumber}</li>
                                <li className="list-group-item">City: {city}</li>
                                <li className="list-group-item">State: {state}</li>
                                <li className="list-group-item">Profile Picture (URL only): {profilePicture}</li>
                                <li className="list-group-item">About Me: {aboutMe}</li>
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
    );
};

export default ProfileView;
