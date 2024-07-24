export interface IAuthContext {
    isAuthenticated: boolean;
    signIn: (email: string, password: string) => void;
    signOut: () => void;
}

export interface IContextProviderProps {
    children: React.ReactNode;
}