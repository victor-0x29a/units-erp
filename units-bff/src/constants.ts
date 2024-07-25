import dotenv from "dotenv";

const environment = process.env.NODE_ENV;

dotenv.config({ path: `./.env.${environment}` });

export const SERVER_PORT: number = Number(process.env.SERVER_PORT || 4500);

export const CAN_LOG: boolean = Boolean(Number(process.env.CAN_LOG));

export const UNITS_VAULT_URL: string = process.env.UNITS_VAULT;

export const UNITS_VAULT_USER_AGENT: string =
  process.env.UNITS_VAULT_USER_AGENT;

export const UNITS_VAULT_MAX_RETRIES = Number(
  process.env.UNITS_VAULT_MAX_RETRIES
);
