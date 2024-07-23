'use client';

import { ButtonHTMLAttributes, useMemo } from 'react';
import styles from './Button.module.scss';
import { IButtonProps } from './Button.types';

export const Button = ({
    label,
    disabled,
    isLoading,
    onClick,
    type = 'submit',
    loadingLabel = 'Carregando...'
}: IButtonProps) => {
    const btnRootType = useMemo(() => {
        return ['success', 'danger'].includes(type) ? 'submit' : type as ButtonHTMLAttributes<HTMLButtonElement>['type'];
    }, [type]);
    return (
        <button
            onClick={onClick}
            disabled={disabled || isLoading}
            className={[styles.btn, styles[type]].join(' ')}
            type={btnRootType}
        >
            {isLoading ? loadingLabel : label}
        </button>
    );
};