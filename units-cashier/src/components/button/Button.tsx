import styles from "./Button.module.scss"
import { IButtonProps } from "./Button.types";

export const Button = ({
    children,
    disabled,
    isLoading,
    onClick,
    type = "default",
    loadingLabel = "Carregando..."
}: IButtonProps) => {
    return (
        <button
            onClick={onClick}
            disabled={disabled || isLoading}
            className={[styles.btn, styles[type]].join(' ')}
        >
            {isLoading ? loadingLabel : children}
        </button>
    );
}