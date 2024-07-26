"use client"
import React, { createContext, useContext, useState, useEffect, useMemo } from 'react';
import { buildApiUrl } from '@/utils/api';
import { useSession } from 'next-auth/react';

type OmoUserType = {
    email: string,
    connectors: any[],
    vector_store: object,
    id: number,
    team_id: number,
    is_active: boolean,
    updated_at: string,
    created_at: string,
}

const defaultAuthContext = {
    omoUser: { // Typing this object as OmoUserType
        email: '',
        connectors: [],
        vector_store: {},
        id: 0,
        team_id: 0,
        is_active: false,
        updated_at: '',
        created_at: '',
    } as OmoUserType,
    isOmoUserLoading: false,
}
export const AuthContext = createContext(defaultAuthContext);

export const AuthProvider = ({ children }: any) => {

    const [omoUser, setOmoUser] = useState<OmoUserType>({} as OmoUserType);
    const [isOmoUserLoading, setIsOmoUserLoading] = useState(true)
    const { data: session, status } = useSession() 

    useEffect(() => {
        if (!session) {
            return;
        }
        const fetchUser = async (endpoint: string) => {
            await fetch(endpoint, {
                credentials: 'include'
            }).then((res) => {
                return res.json()
            }).then((data) => {
                setOmoUser(data);
            }).catch( (error) => {
                console.error('Error fetching Omo user', error);
            }).finally( () => {
                setIsOmoUserLoading(false);
            })
        }
        const endpoint = buildApiUrl('/v1/me');
        fetchUser(endpoint);

    }, [session])

    return (
        <AuthContext.Provider value={{ omoUser, isOmoUserLoading }}>
            {children}
        </AuthContext.Provider>
    );
};