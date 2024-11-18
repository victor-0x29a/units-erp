import moment from "moment-timezone";

export const getByTimestamp = (timestamp: number): Date => moment(timestamp).utc().toDate();
