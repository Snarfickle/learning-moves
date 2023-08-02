import React from "react";
import { useActionData } from "react-router-dom";

const UserContext = React.createContext();

export const UserProvider = UserContext.Provider;
export const UserConsumer = UserContext.Consumer;
export default UserContext;
