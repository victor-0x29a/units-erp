"use client"

import React, { createContext, useMemo } from "react";
import { IAuthContext, IContextProviderProps } from "./app"

export const AuthContext = createContext<IAuthContext>({
    isAuthenticated: false,
    signIn: () => {},
    signOut: () => {}
})


export const AuthProvider = ({ children }: IContextProviderProps) => {
    function signIn(email: string, password: string) {
        console.log("signIn", email, password)
    }

    function signOut() {
        console.log("signOut")
    }

    const values = useMemo(() => ({
        isAuthenticated: false,
        signIn,
        signOut
    }), [])

    return (
        <AuthContext.Provider value={values}>
            {children}
        </AuthContext.Provider>
    )
}