// altCodes should be objects
// {
//  procedence: "OpenFacts",
//  id: "0174DGH3",
//  name: "Burnt eggs",
//  description: "Eggs with a touch of black"
//  otherInformation: "Very unhealthy. can be deadly"
// }

class TicketLine {

  public units: number;
  public name: string;
  public price: number;
  public weight: string;
  public weightPrice: number;
  public readableName: string;
  public id: string;

  constructor(
    units: number,
    name: string,
    price: number,
    weight: string,
    weightPrice: number,
    readableName: string,
    id: string
  ) {
    this.units = units;
    this.name = name;
    this.price = price;
    this.weight = weight;
    this.weightPrice = weightPrice;
    this.readableName = readableName;
    this.id = id;
  }
}

export default TicketLine;