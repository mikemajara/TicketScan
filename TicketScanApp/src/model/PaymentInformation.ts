class PaymentInformation {
  constructor(
    private total?: string,
    private returned?: string,
    private method?: string,
  ) { }
}

export default PaymentInformation;