import moment from "moment-timezone";

export const startOfDay = (date: Date): Date => moment(date).utc().startOf('day').toDate();
