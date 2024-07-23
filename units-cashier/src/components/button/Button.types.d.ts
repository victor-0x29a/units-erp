import { identity } from '../components';

export interface IButtonProps {
    isLoading?: boolean;
    onClick?: identity;
    label: string;
    type?: 'success' | 'danger' | 'reset' | 'submit';
    loadingLabel?: string;
    disabled?: boolean;
}