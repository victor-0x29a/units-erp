import { identity } from '../components'

export interface ITextInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    onChange: identity;
    onBlur: identity;
    value: string;
    label: string;
    type?: 'text' | 'password';
};