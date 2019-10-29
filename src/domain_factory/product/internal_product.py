from domain_factory.product.product import Product


class InternalProduct(Product):
    """ Class to generate internal products. Generate method will call the
    Product generate method in order to populate fields shared by all
    products. The generate method in this class will then populate the
    remaining attributes unique to the Internal Product domain factory. """

    def generate(self, record_count, start_id):
        """ Generate a set number of products

        Parameters
        ----------
        record_count : int
            Number of Internal Products to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' Internal Products
        """

        records = []

        return records
