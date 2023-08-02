import React from 'react';
import { NavLink } from 'react-router-dom';
import UserContext from './contexts/UserContext';
import { useContext } from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';

function NavComponent() {
    const {user} = useContext(UserContext);

    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand as={NavLink} to="/">Learning Moves</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    {user ? (
                        <>
                            <NavDropdown title="Account" id="basic-nav-dropdown">
                                <NavDropdown.Item as={NavLink} to="/account">Account</NavDropdown.Item>
                                <NavDropdown.Item as={NavLink} to="/profile">Profile</NavDropdown.Item>
                                <NavDropdown.Item as={NavLink} to="/logout">Logout</NavDropdown.Item>
                            </NavDropdown>
                        </>
                    ) : (
                        <>
                            <Nav.Link as={NavLink} to="/auth/login">Login</Nav.Link>
                            <Nav.Link as={NavLink} to="/signup">Sign Up</Nav.Link>
                        </>
                    )}
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    )
}

export default NavComponent;
