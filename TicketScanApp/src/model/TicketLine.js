// altCodes should be objects 
// {
//  procedence: "OpenFacts",
//  id: "0174DGH3",
//  name: "Burnt eggs",
//  description: "Eggs with a touch of black"
//  otherInformation: "Very unhealthy. can be deadly"
// }
class TicketLine {
  constructor(units, name, price, weight, weightPrice, readableName, id, altCodes) {
    this.units = units;
    this.name = name;
    this.price = price;
    this.weight = weight;
    this.weightPrice = weightPrice;
    this.readableName = readableName;
    this.id = id;
    this.altCodes = altCodes;
  }
}

export default TicketLine;