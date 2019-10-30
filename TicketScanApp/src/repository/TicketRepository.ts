import BaseRepository from './BaseRepository';
import Ticket from '../model/Ticket';
import CompanyRepository from '../repository/CompanyRepository';
import moment from 'moment/min/moment-with-locales';

export default class TicketRepository extends BaseRepository<Ticket> {

  updatePath = 'update_ticket';
  findAllPath = 'get_all_tickets';
  findOnePath = 'get_ticket';

  private static instance: TicketRepository;

  public static getInstance(): TicketRepository {
    if (!TicketRepository.instance) {
      TicketRepository.instance = new TicketRepository();
    }
    return TicketRepository.instance;
  }


  fromJson(item: object): Ticket {
    let { _id, company, store, date, lines, payment_information } = item;
    company = new CompanyRepository().fromJson(company);
    date = moment(date, 'DD/MM/YYYY HH:mm').toDate();
    return new Ticket(_id, company, store, date, payment_information, lines)
  }
  fromJsonArray(items: object[]): Ticket[] {
    return items.map(item => this.fromJson(item));
  }
}

