import Store from './Store';
import TicketLine from './TicketLine';

class Ticket {
  constructor(store, datetime, proprietaryCodes, paymentMethod, total, returned, ticketLines) {
    this.store = store;
    this.datetime = datetime;
    this.proprietaryCodes = proprietaryCodes;
    this.paymentMethod = paymentMethod;
    this.total = total;
    this.returned = returned;
    this.ticketLines = ticketLines;
  }
}

export default Ticket;