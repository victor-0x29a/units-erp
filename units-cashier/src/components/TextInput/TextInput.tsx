'use client';

import { ITextInputProps } from './TextInput.types';
import styles from './TextInput.module.scss';

export const TextInput = ({
    label,
    onBlur,
    onChange,
    value,
    type = 'text'
}: ITextInputProps) => {
    return (
        <div className={styles['input-container']}>
            <label>{label}</label>
            <input
                value={value}
                onChange={(event) => onChange(event.target.value)}
                onBlur={onBlur}
                type={type}
            />
        </div>
    );
};