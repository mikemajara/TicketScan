// import all interfaces
import { IWrite } from './IWrite';
import { IRead } from './IRead';

// that class only can be extended
export default abstract class BaseRepository<T> implements IWrite<T>, IRead<T> {
  // Use for development in local pc (with simulator)
  apiUrl: string = 'http://127.0.0.1:5001/';
  // Use for development in local network (insert ip of local computer)
  // apiUrl: string = 'http://172.20.10.4:5001/';

  abstract updatePath: string;
  abstract findAllPath: string;
  abstract findOnePath: string;

  //we created constructor with arguments to manipulate mongodb operations
  constructor() { }

  abstract fromJson(item: object): T;
  abstract fromJsonArray(items: object[]): T[];

  async update(item: T): Promise<boolean> {
    try {
      const response = await fetch(`${this.apiUrl}${this.updatePath}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(item),
      });
      return response.ok;
    } catch (error) {
      console.log(error)
      throw new Error('Exception handling not implemented');
    }
  }

  async findAll(): Promise<T[]> {
    try {
      const response = await fetch(`${this.apiUrl}${this.findAllPath}`);
      const responseJson = await response.json();
      const obj = this.fromJsonArray(responseJson);
      return obj;
    } catch (error) {
      console.log(error)
      throw new Error('Exception handling not implemented');
    }
  }

  async findOne(id: string): Promise<T> {
    try {
      const response = await fetch(`${this.apiUrl}${this.findOnePath}/${id}`);
      const responseJson = await response.json();
      const obj = this.fromJson(responseJson);
      return obj;
    } catch (error) {
      console.log(error)
      throw new Error('Exception handling not implemented');
    }
  }
}