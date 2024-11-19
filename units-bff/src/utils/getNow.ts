import moment from "moment-timezone";

export const getNow = (): Date => moment().utc().toDate();
