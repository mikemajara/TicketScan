class Store {

  public company: string;
  public country: string;
  public city: string;
  public address: string;
  public phone: string;
  public id: string;

  constructor(
    company: string,
    country: string,
    city: string,
    address: string,
    phone: string,
    id: string
  ) {
    this.company = company;
    this.country = country;
    this.city = city;
    this.address = address;
    this.phone = phone;
    this.id = id;
  }
}

export default Store;