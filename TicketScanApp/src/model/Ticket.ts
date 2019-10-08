import Store from './Store';
import Company from './Company';
import TicketLine from './TicketLine';
import PaymentInformation from './PaymentInformation';

class Ticket {
  constructor(
    private _id?: string,
    private company?: Company,
    private store?: Store,
    private datetime?: Date,
    private paymentInformation?: PaymentInformation,
    private lines?: Array<TicketLine>,
  ) { }
}

export default Ticket;