import { identity } from '../components'

export interface ITextInputProps {
    onChange: identity;
    onBlur: identity;
    value: string;
    label: string;
    type?: 'text' | 'password';
}