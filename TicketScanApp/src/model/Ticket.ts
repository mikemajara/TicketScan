import Store from './Store';
import ProprietaryTicketCode from './ProprietaryTicketCode';
import TicketLine from './TicketLine';
import Company from './Company';

class Ticket {

  company: Company;
  store: Store;
  datetime: Date;
  proprietaryTicketCodes: Array<ProprietaryTicketCode>;
  paymentMethod: string;
  total: number;
  returned: number;
  lines: Array<TicketLine>;

  constructor(
    company: Company,
    store: Store,
    datetime: Date,
    proprietaryTicketCodes: Array<ProprietaryTicketCode>,
    paymentMethod: string,
    total: number,
    returned: number,
    lines: Array<TicketLine>
  ) {
    this.company = company;
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