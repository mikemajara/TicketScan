import BaseRepository from './BaseRepository';
import Company from '../model/Company';

export default class CompanyRepository extends BaseRepository<Company> {

  updatePath = '';
  findAllPath = 'get_companies';
  findOnePath = '';

  private static instance: CompanyRepository;

  public static getInstance(): CompanyRepository {
    if (!CompanyRepository.instance) {
      CompanyRepository.instance = new CompanyRepository();
    }
    return CompanyRepository.instance;
  }

  fromJson(item: object): Company {
    return Object.assign(new Company, item);
  }
  fromJsonArray(items: object[]): Company[] {
    return items.map(item => this.fromJson(item));
  }
}

