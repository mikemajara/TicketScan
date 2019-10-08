// - Temporarily deleted, keep this here for idea
// altCodes should be objects
// {
//  procedence: "OpenFacts",
//  id: "0174DGH3",
//  name: "Burnt eggs",
//  description: "Eggs with a touch of black"
//  otherInformation: "Very unhealthy. can be deadly"
// }

class TicketLine {
  constructor(
    private units?: number,
    private name?: string,
    private price?: number,
    private weight?: string,
    private weightPrice?: number,
    private readableName?: string,
    private id?: string,
  ) { }
}

export default TicketLine;