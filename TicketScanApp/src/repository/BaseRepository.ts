// import all interfaces
import { IWrite } from './IWrite';
import { IRead } from './IRead';

// that class only can be extended
export default abstract class BaseRepository<T> implements IWrite<T>, IRead<T> {
  apiUrl: string = 'http://127.0.0.1:5001/';

  abstract updatePath: string;
  abstract deletePath: string;
  abstract findAllPath: string;
  abstract findOnePath: string;

  //we created constructor with arguments to manipulate mongodb operations
  constructor() { }

  abstract fromJson(item: object): T;
  abstract fromJsonArray(items: object[]): T[];

  update(id: string, item: T): Promise<boolean> {
    throw new Error('Method not implemented.');
  }
  delete(id: string): Promise<boolean> {
    throw new Error('Method not implemented.');
  }
  async findAll(): Promise<T[]> {
    try {
      const response = await fetch(this.apiUrl + this.findAllPath);
      const responseJson = await response.json();
      const obj = this.fromJsonArray(responseJson);
      return obj;
    } catch (error) {
      throw new Error('Exception handling not implemented');
    }
  }
  findOne(id: string): Promise<T> {
    throw new Error('Method not implemented.');
  }
}