import {BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import Nav from './Nav';
import './App.css';
import SignUpForm from './components/Account/SignUpForm';
import HomePage from './mainHome';
import { UserProvider } from './contexts/UserContext';
import LoginForm from './components/Account/LoginForm';
import ProfileView from './components/Profile/ProfileView';
import ProfileForm from './components/Profile/ProfileForm';
import LogOut from './components/Account/LogOut';
import AccountOne from './components/Account/AccountOne';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  const [user, setUser] = useState(null);
  return (
    <UserProvider value={{ user, setUser}}>
      <BrowserRouter>
        <Nav />
        <div className='App'>
          <Routes>
            <Route path='/*' element={<HomePage />}/>
            <Route path='/account' element={<AccountOne />} />
            <Route path='/signup' element={<SignUpForm />} />
            <Route path='/auth/login' element={<LoginForm />} />
            <Route path='/profile' element={<ProfileView />} />
            <Route path='/profile/edit' element={<ProfileForm />} />
            <Route path='/logout' element={<LogOut />} />
          </Routes>
        </div>
      </BrowserRouter>
    </UserProvider>
    );
}

export default App;
