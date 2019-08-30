// altCodes should be objects 
// {
//  procedence: "OpenFacts",
//  id: "0174DGH3",
//  name: "Burnt eggs",
//  description: "Eggs with a touch of black"
//  otherInformation: "Very unhealthy. can be deadly"
// }
class TicketLine {
  constructor(quantity, weight, price, name, readableName, id, altCodes) {
    this.quantity = quantity;
    this.weight = weight;
    this.price = price;
    this.name = name;
    this.readableName = readableName;
    this.id = id;
    this.altCodes = altCodes;
  }
}

export default TicketLine;