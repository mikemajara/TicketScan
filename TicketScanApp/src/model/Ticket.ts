import Store from './Store';
import ProprietaryTicketCode from './ProprietaryTicketCode';
import TicketLine from './TicketLine';

class Ticket {

  store: Store;
  datetime: Date;
  proprietaryTicketCodes: Array<ProprietaryTicketCode>;
  paymentMethod: string;
  total: number;
  returned: number;
  lines: Array<TicketLine>;

  constructor(
    store: Store,
    datetime: Date,
    proprietaryTicketCodes: Array<ProprietaryTicketCode>,
    paymentMethod: string,
    total: number,
    returned: number,
    lines: Array<TicketLine>
  ) {
    this.store = store;
    this.datetime = datetime;
    this.proprietaryTicketCodes = proprietaryTicketCodes;
    this.paymentMethod = paymentMethod;
    this.total = total;
    this.returned = returned;
    this.lines = lines;
  }
}

export default Ticket;