import BaseRepository from './BaseRepository';
import Ticket from '../model/Ticket';

export default class TicketRepository extends BaseRepository<Ticket> {

  updatePath = 'update_ticket';
  findAllPath = 'get_all_tickets';
  findOnePath = 'get_ticket';

  fromJson(item: object): Ticket {
    return Object.assign(new Ticket, item);
  }
  fromJsonArray(items: object[]): Ticket[] {
    return items.map(item => this.fromJson(item));
  }
}

