import React, { useMemo } from 'react';
import styles from './Column.module.scss';
import { IColumnProps } from './Column.types';

export const Column = ({
    children,
    className = '',
    error,
    hasError,
    isDisabled,
    isTouched
}: IColumnProps) => {
    const canShowError = useMemo(() => hasError && isTouched && error && !isDisabled, [hasError, isTouched, error, isDisabled]);

    return <div className={[styles.column, className].join(' ')}>
        {children}
        {canShowError && (<p className='error-label'>{error}</p>)}
    </div>;
};