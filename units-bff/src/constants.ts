import dotenv from "dotenv";

const environment = process.env.NODE_ENV;

export const IS_DEVELOPMENT = environment === "development";

dotenv.config();

export const MYSQL_PASSWORD: string = process.env.MYSQL_ROOT_PASSWORD;

export const MYSQL_HOSTNAME: string = process.env.MYSQL_HOSTNAME;

export const MYSQL_DATABASE: string = process.env.MYSQL_DATABASE;

export const MYSQL_PORT: number = Number(process.env.MYSQL_PORT);

dotenv.config({ path: `./.env.${environment}` });

export const MYSQL_USER: string = process.env.MYSQL_USER;

export const SERVER_PORT: number = Number(process.env.SERVER_PORT || 4500);

export const CAN_LOG: boolean = Boolean(Number(process.env.CAN_LOG));

export const UNITS_VAULT_URL: string = process.env.UNITS_VAULT;

export const UNITS_VAULT_USER_AGENT: string =
  process.env.UNITS_VAULT_USER_AGENT;

export const UNITS_VAULT_MAX_RETRIES = Number(
  process.env.UNITS_VAULT_MAX_RETRIES
);
