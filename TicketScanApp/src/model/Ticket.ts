import Store from './Store';
import TicketLine from './TicketLine';

class Ticket {

  store: Store;
  datetime: string;
  proprietaryCodes: string;
  paymentMethod: string;
  total: string;
  returned: string;
  lines: string;

  constructor(store, datetime, proprietaryCodes, paymentMethod, total, returned, lines) {
    this.store = store;
    this.datetime = datetime;
    this.proprietaryCodes = proprietaryCodes;
    this.paymentMethod = paymentMethod;
    this.total = total;
    this.returned = returned;
    this.lines = lines;
  }
}

export default Ticket;