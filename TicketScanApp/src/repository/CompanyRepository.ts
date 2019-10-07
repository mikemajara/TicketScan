import IRepositoryEntity from './IRepositoryEntity';
import Company from '../model/Company';

export default class CompanyRepository implements IRepositoryEntity<Company> {
  async getEntity(_id: string): Promise<Company> {
    let responseJson = null;
    try {
      const response = await fetch(`http://127.0.0.1:5001/get_company/${_id}`);
      if (response.status === 200) {
        responseJson = await response.json();
      }
      return responseJson;
    } catch (error) {
      return responseJson;
    }
  }
}

