import unittest
import pandas as pd
import pandas.testing as pd_testing
from load_and_clean_csv import clean_df, clean_customer_data, clean_books_data, enrich_books_data

class TestOperations(unittest.TestCase):

    def test_clean(self):
        input_df = pd.DataFrame({"col1":[None," test  ", "SECOND test", "TEST 3"],
                                 "col2":[None,"01/01/2026","32/01/2026",None]})
        output_df = clean_df(input_df, ["col1"], ["col2"])
        expected_output_df = pd.DataFrame({"Col1":["Test", "Second Test", "Test 3"],
                                 "Col2":[pd.to_datetime("01/01/2026"),pd.NaT,pd.NaT]},
                                 index=[1, 2, 3]) 
        pd_testing.assert_frame_equal(output_df, expected_output_df)

    def test_clean_customer_data(self):
        input_df = pd.DataFrame({"Customer ID":[1.0, 2.0, 3.0, None],
                                 "Customer Name":["amy ADAMS", "Billy bragg", "charlie cooper   ", None]})
        output_df = clean_customer_data(input_df)
        expected_output_df = pd.DataFrame({"Customer Id":[1.0, 2.0, 3.0],
                                 "Customer Name":["Amy Adams", "Billy Bragg", "Charlie Cooper"]}) 
        pd_testing.assert_frame_equal(output_df, expected_output_df)

    def test_clean_books_data(self):
        input_df = pd.DataFrame({"Id":[1.0, 2.0, 3.0, None],
                                 "Books":["spoilt creatures", "JANE EYRE", "   cIRcE", None],
                                 "Book Checkout":["40/02/2025", "01/02/2023", '"01/01/2000"', None],
                                 "Book Returned":["31/12/2024", "31/02/2024", "21/08/2023", None],
                                 "Days allowed to borrow":["2 weeks", "3 weeks", "4 weeks", None],
                                 "Customer ID":[1.0, 2.0, 3.0, None]})
        output_df = clean_books_data(input_df)
        expected_output_df = pd.DataFrame({"Id":[1.0, 2.0, 3.0],
                                 "Books":["Spoilt Creatures", "Jane Eyre", "Circe"],
                                 "Book Checkout":[pd.NaT, pd.to_datetime("01/02/2023"), pd.to_datetime("01/01/2000")],
                                 "Book Returned":[pd.to_datetime("31/12/2024"), pd.NaT, pd.to_datetime("21/08/2023")],
                                 "Days Allowed To Borrow":[14, 21, 28],
                                 "Customer Id":[1.0, 2.0, 3.0]})
        pd_testing.assert_frame_equal(output_df, expected_output_df)

    def test_enrich(self):
        input_df = pd.DataFrame({"Book Checkout":[pd.to_datetime('2026-01-01')],
                                 "Book Returned":[pd.to_datetime('2026-01-02')]}) 
        output_df = enrich_books_data(input_df)
        expected_output_df = pd.DataFrame({"Book Checkout":[pd.to_datetime('2026-01-01')],
                            "Book Returned":[pd.to_datetime('2026-01-02')],
                            "Time On Loan":[1]}) 
        pd_testing.assert_frame_equal(output_df, expected_output_df)


if __name__ == "__main__":

    unittest.main()