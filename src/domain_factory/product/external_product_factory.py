from domain_factory.product.product_factory import ProductFactory


class ExternalProductFactory(ProductFactory):
    """ Class to generate external products. Generate method will call the
    Product generate method in order to populate fields shared by all
    products. The generate method in this class will then populate the
    remaining attributes unique to the External Product domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of products

        Parameters
        ----------
        record_count : int
            Number of External Products to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' External Products
        """

        records = []

        return records
