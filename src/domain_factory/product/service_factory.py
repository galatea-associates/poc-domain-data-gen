from domain_factory.product.product_factory import ProductFactory


class ServiceFactory(ProductFactory):
    """ Class to generate services. Generate method will call the
    ProductFactory generate method in order to populate fields shared by all
    products. The generate method in this class will then populate the
    remaining attributes unique to the Service domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of products

        Parameters
        ----------
        record_count : int
            Number of Services to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' Services
        """

        records = []

        return records
