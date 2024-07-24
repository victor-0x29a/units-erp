import React from "react";
import { identity } from "../components";

export interface IButtonProps {
    isLoading?: boolean;
    onClick?: identity;
    children: React.ReactNode;
    type?: "success" | "danger" | "default";
    loadingLabel?: string;
    disabled?: boolean;
}