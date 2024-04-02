''' Testing Modules '''
import unittest
from datetime import datetime
from weather_man import check_valid_date, check_valid_directory, check_valid_file,\
                        extract_data_from_list_of_lists

class TestWeatherFunctions(unittest.TestCase):
    '''
        class to do unit testing
    '''

    def test_check_valid_date(self):
        '''
        Test check_valid_date function
        '''
        self.assertTrue(check_valid_date('2022'))
        self.assertTrue(check_valid_date('2022/12'))
        self.assertFalse(check_valid_date('invalid'))
        self.assertFalse(check_valid_date('2022/13'))

    def test_check_valid_directory(self):
        '''
        test the directory if there is any file in formate
        '''
        valid_path = 'Murree_weather'
        invalid_path = 'invalid_path'

        with self.subTest(path=valid_path):
            self.assertTrue(check_valid_directory(valid_path))

        with self.subTest(path=invalid_path):
            self.assertFalse(check_valid_directory(invalid_path))

    def test_check_valid_file(self):
        '''
        test the file if it is valid
        '''
        self.assertTrue(check_valid_file('Murree_weather_Murree_weather_2022_JAN.txt'))
        self.assertFalse(check_valid_file('invalid_file.txt'))

    def test_extract_data_from_list_of_lists(self):
        '''
        test the function to extract data from list of lists
        '''
        input_list = ['2022-01-01, 30, 25, 20, 90, 70, 50, 80, 60, 40,30, \
                        25, 20, 90, 70, 50, 80, 60, 40,20',
                        '2022-01-02, 32, 28, 22, 95, 75, 55, 85, 65, 45,32, 28,\
                        22, 95, 75, 55, 85, 65, 45,22']
        expected_output = [[datetime(2022, 1, 1), 30.0, 25.0, 20.0, 80.0, 60.0, 40.0],
                           [datetime(2022, 1, 2), 32.0, 28.0, 22.0,85.0, 65.0, 45.0]]
        self.assertEqual(extract_data_from_list_of_lists(input_list), expected_output)

if __name__ == '__main__':
    unittest.main()
