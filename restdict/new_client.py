import sys
import pprint
import restdict

SERVER_ADDRESS = 'http://localhost:5001'
SERVER_API_URI = f'{SERVER_ADDRESS}/api/v1'

NON_STRING_VALUE = 0
TEST_KEY = 'test_key'
TEST_VALUE = 'test_value'
NEW_KEY = 'new_key'
NEW_VALUE = 'new_value'
ANOTHER_KEY = 'another_key'
ANOTHER_VALUE = 'another_value'
TEST_DICT = {NEW_KEY: NEW_VALUE, ANOTHER_KEY: ANOTHER_VALUE}


def main():
    test_dict = restdict.new_client(SERVER_API_URI, 'test_dict')
    test_dict2 = restdict.new_client(SERVER_API_URI)
    test_dict[TEST_KEY] = None
    test_dict2[TEST_KEY] = TEST_VALUE
    print(test_dict2)

if __name__ == '__main__':
    sys.exit(main())
