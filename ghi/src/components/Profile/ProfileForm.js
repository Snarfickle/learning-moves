import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const ProfileForm = () => {
    const [id, setId] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [city, setCity] = useState('');
    const [state, setState] = useState('');
    const [profilePicture, setProfilePicture] = useState('');
    const [aboutMe, setAboutMe] = useState('');
    const [isProfileLoaded, setIsProfileLoaded] = useState(false);
    const navigate = useNavigate();

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
    }
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
            console.error('Failed to load profile here');
            setIsProfileLoaded(false);
        }
    }

    useEffect(() => {
        if (id) {
        loadProfile();
        }
    }, [id]);

    const updateProfile = async (event) => {
        event.preventDefault();
        const updateData = {
            id: id,
            account_id: id,
            first_name: firstName,
            last_name: lastName,
            email: email, 
            phone_number: phoneNumber,
            city: city, 
            state: state, 
            profile_picture: profilePicture,
            about_me: aboutMe,
        };

        const updateProfileURL = `http://localhost:8000/profiles/edit/${id}`;
        const fetchConfig = {
            method: "PUT",
            body: JSON.stringify(updateData),
            headers: {
                "Content-Type": "application/json",
            },
            credentials: 'include',
        };

        const response = await fetch(updateProfileURL, fetchConfig);

        if (response.ok) {
            navigate(`/profile/`);
        } else {
            console.error("the update broke");
        }
        
    };

    return (
        <div className="container mt-10">
            { isProfileLoaded ? (
                <>
                    <h1 className="mb-4">Profile Information</h1>
                    <div className="card">
                        <div className="card-body">
                            <form onSubmit={updateProfile}>
                                <div className="mb-3">
                                    <label className="form-label">First Name</label>
                                    <input type="text" className="form-control" value={firstName} onChange={e => setFirstName(e.target.value)} />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Last Name</label>
                                    <input type="text" className="form-control" value={lastName} onChange={e => setLastName(e.target.value)} />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Email</label>
                                    <input type="email" className="form-control" value={email} onChange={e => setEmail(e.target.value)} />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">PhoneNumber</label>
                                    <input type="phoneNumber" className="form-control" value={phoneNumber} onChange={e => setPhoneNumber(e.target.value)} />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">City</label>
                                    <input type="city" className="form-control" value={city} onChange={e => setCity(e.target.value)} />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">State</label>
                                    <input type="state" className="form-control" value={state} onChange={e => setState(e.target.value)} />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Profile Picture</label>
                                    <input type="url" className="form-control" value={profilePicture} onChange={e => setProfilePicture(e.target.value)} />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">About Me</label>
                                    <input type="text" className="form-control" value={aboutMe} onChange={e => setAboutMe(e.target.value)} />
                                </div>
                                <div className="mb-3">
                                    <button type="submit" className="btn btn-primary">Update Profile</button>
                                </div>
                            </form>
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

export default ProfileForm;
