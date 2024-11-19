import moment from "moment-timezone";

export const endOfDay = (date: Date): Date => moment(date).utc().endOf('day').toDate();
