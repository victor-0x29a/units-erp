import React, { useMemo } from 'react'
import { IColumnProps } from "./Column.types"

export const Column = ({
    children,
    className,
    error,
    hasError,
    isDisabled,
    isTouched
}: IColumnProps) => {
    const canShowError = useMemo(() => hasError && isTouched && error, [hasError, isTouched, error]);

    return <div>
        {children}
        {canShowError && <p className='error-label'>{error}</p>}
    </div>
}