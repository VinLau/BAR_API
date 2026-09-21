from api import app
from unittest import TestCase


class TestIntegrations(TestCase):
    def setUp(self):
        self.app_client = app.test_client()

    def test_get_arabidopsis_nie_umap_coordinates(self):
        """This tests the UMAP coordinates returned for the Arabidopsis NIE UMAP database
        :return:
        """
        # Valid data
        response = self.app_client.get("/umap_gene_expression/arabidopsis_NIE_umap")
        expected = {
            "wasSuccessful": True,
            "data": {
                "43": {"umap_1": -6.89231, "umap_2": 7.56863, "cell_type": "Metabolic stress state"},
                "44": {"umap_1": 2.87577, "umap_2": -4.82349, "cell_type": "Dividing"},
                "45": {"umap_1": -0.262505, "umap_2": -8.55344, "cell_type": "Guard"},
                "46": {"umap_1": -4.5876, "umap_2": 6.05261, "cell_type": "Defense state"},
            },
        }
        self.assertEqual(response.json, expected)

        # Invalid database
        response = self.app_client.get("/umap_gene_expression/arabidopsis_NIE_um;ap")
        expected = {"wasSuccessful": False, "error": "Invalid database"}
        self.assertEqual(response.json, expected)

    def test_get_arabidopsis_nie_umap_gene(self):
        """This tests the sparse UMAP expression data returned for a gene. Cells with no key are zero.
        :return:
        """
        # Valid data, with no expression in cell 45
        response = self.app_client.get("/umap_gene_expression/arabidopsis_NIE_umap/At1g01010")
        expected = {"wasSuccessful": True, "data": {"43": 1.152292, "44": 1.546603, "46": 1.392931}}
        self.assertEqual(response.json, expected)

        # Valid data, with expression in every cell
        response = self.app_client.get("/umap_gene_expression/arabidopsis_NIE_umap/AT3G18780")
        expected = {
            "wasSuccessful": True,
            "data": {"43": 1.673516, "44": 3.142986, "45": 1.490115, "46": 1.953491},
        }
        self.assertEqual(response.json, expected)

        # Invalid gene
        response = self.app_client.get("/umap_gene_expression/arabidopsis_NIE_umap/At1g0101x")
        expected = {"wasSuccessful": False, "error": "Invalid gene id"}
        self.assertEqual(response.json, expected)

        # Invalid database
        response = self.app_client.get("/umap_gene_expression/arabidopsis_NIE_um;ap/At1g01010")
        expected = {"wasSuccessful": False, "error": "Invalid database"}
        self.assertEqual(response.json, expected)

        # No data for a valid gene
        response = self.app_client.get("/umap_gene_expression/arabidopsis_NIE_umap/At1g01011")
        expected = {
            "wasSuccessful": False,
            "error": "There are no data found for the given gene",
        }
        self.assertEqual(response.json, expected)
