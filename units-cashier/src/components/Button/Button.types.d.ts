import React from 'react';
import { identity } from '../components';

export interface IButtonProps {
    isLoading?: boolean;
    onClick?: identity;
    children: React.ReactNode;
    type?: 'success' | 'danger' | 'reset' | 'submit';
    loadingLabel?: string;
    disabled?: boolean;
}