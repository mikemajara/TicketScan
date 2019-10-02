class Company {

  public id: string;
  public name: string;
  public taxId: string;
  public web: string;

  constructor(
    id: string,
    name: string,
    taxId: string,
    web: string,
  ) {
    this.id = id;
    this.name = name;
    this.taxId = taxId;
    this.web = web;
  }
}

export default Company;