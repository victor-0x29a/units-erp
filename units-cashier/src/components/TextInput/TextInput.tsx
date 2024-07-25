'use client';

import { ITextInputProps } from './TextInput.types';
import styles from './TextInput.module.scss';

export const TextInput = ({
    label,
    onBlur,
    onChange,
    value,
    type = 'text',
    ...others
}: ITextInputProps) => {
    return (
        <div className={styles['input-container']}>
            <label>{label}</label>
            <input
                value={value}
                onChange={onChange}
                onBlur={onBlur}
                type={type}
                {...others}
            />
        </div>
    );
};