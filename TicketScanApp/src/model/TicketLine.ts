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
    private _id?: string,
    private units?: number,
    private name?: string,
    private total?: number,
    private price?: number,
    private weight?: string,
    private weightPrice?: number,
  ) { }
}

export default TicketLine;