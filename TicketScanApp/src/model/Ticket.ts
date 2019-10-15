import Store from './Store';
import ProprietaryTicketCode from './ProprietaryTicketCode';
import TicketLine from './TicketLine';
import Company from './Company';

class Ticket {
  _id: string;
  company: Company;
  store: Store;
  datetime: Date;
  proprietaryTicketCodes: Array<ProprietaryTicketCode>;
  paymentMethod: string;
  total: number;
  returned: number;
  lines: Array<TicketLine>;

  constructor(
    _id: string,
    company: Company,
    store: Store,
    datetime: Date,
    proprietaryTicketCodes: Array<ProprietaryTicketCode>,
    paymentMethod: string,
    total: number,
    returned: number,
    lines: Array<TicketLine>
  ) {
    this._id = _id;
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