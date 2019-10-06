import Company from '../model/Company';
import Store from '../model/Store';
import TicketLine from '../model/TicketLine';
import Ticket from '../model/Ticket';


export const STYLE_DEBUG = false;
export const styleDebug = color => (STYLE_DEBUG ? { borderWidth: 1, borderColor: color } : {});

const company = new Company('id: string', 'Mercadona S.A.', 'A-1324122', '');
const store = new Store(
  'Mercadona',
  'Spain',
  'Murcia',
  'AVDA. CICLISTA MARIANO ROJAS-AV',
  '+34 968227166',
  'A-46103834'
);
const lines = [
  new TicketLine('1', 'B, ALMENDRA S/A', '8,40', null, null, 'readableName', null, []),
  new TicketLine('4', 'L SEMI S/LACTO', '18,00', null, null, 'readableName', null, []),
  new TicketLine('3', 'GALLETA RELIEV', '3,66', null, null, 'readableName', null, []),
  new TicketLine('1', 'COPOS AVENA', '0,81', null, null, 'readableName', null, []),
  new TicketLine('1', 'COSTILLA BARB', '3,99', null, null, 'readableName', null, []),
  new TicketLine('1', 'ZANAHORIA BOLS', '0,69', null, null, 'readableName', null, []),
  new TicketLine('2', 'VENTRESCA ATUN', '4,30', null, null, 'readableName', null, []),
  new TicketLine('1', 'PAPEL HIGIENIC', '2,70', null, null, 'readableName', null, []),
  new TicketLine('1', 'HIGIENICO DOBL', '2,07', null, null, 'readableName', null, []),
  new TicketLine('1', 'PEPINO', '0,90', '0,478 kg', '1,89 €/kg', 'readableName', null, []),
  new TicketLine('1', 'PLATANO', '1,41', '0,616 kg', '2,29 €/kg', 'readableName', null, []),
];
// const proprietaryCodes = [{ OP: '068391' }, { 'FACTURA SIMPLIFICADA': '2707-022-142004' }];
const dummyTicket = new Ticket(
  '00000',
  company,
  store,
  new Date('2019-03-04T19:51'),
  null,
  'CARD',
  '46,93',
  null,
  lines
);
export const getMockupTicket = () =>
  new Ticket(
    Math.floor(Math.random() * 10000000),
    company,
    store,
    new Date('2019-03-04T19:51'),
    null,
    'CARD',
    '46,93',
    null,
    lines
  );

export const mockupTicket = dummyTicket;