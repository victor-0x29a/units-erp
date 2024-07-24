import { object, string } from 'yup';

const userRequiredLabel = 'O usuário é obrigatório';
const passwordRequiredLabel = 'A senha é obrigatória';

export const LoginSchema = object({
    username: string().typeError(userRequiredLabel).required(userRequiredLabel),
    password: string().typeError(passwordRequiredLabel).min(6, 'A senha deve ter no mínimo 6 dígitos').max(20, 'A senha deve ter no máximo 20 dígitos').required(passwordRequiredLabel)
});

export const LoginInitialValues = {
    username: '',
    password: ''
};
