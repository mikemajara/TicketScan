interface IRepositoryEntity<T> {
  getEntity(_id: string): Promise<T>;
}

export default IRepositoryEntity;