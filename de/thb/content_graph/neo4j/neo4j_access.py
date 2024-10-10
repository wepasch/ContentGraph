import requests
from requests.auth import HTTPBasicAuth
from neo4j import GraphDatabase, Driver


class Neo4jAccess:
    def __init__(self, host: str, port: int, user: str, password: str):
        uri = f"bolt://{host}:{port}"
        self.__driver: Driver = GraphDatabase.driver(uri, auth=(user, password))
        if not self.__is_connected():
            raise Exception("Neo4j connection failed")

    def __is_connected(self) -> bool:
        try:
            with self.__driver.session() as session:
                session.run("RETURN 1")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def bl(self):
        print(self.__driver.get_server_info())

class Neo4jQuery:
    @staticmethod
    def create_node(label: str, data: dict[str, str | int | list[str]]) -> str:
        data_str: str = ''
        if data.keys():
            pass
        for k, v in data.items():
            data_str += f'{k}: {Neo4jQuery.__value_to_string(v)}, '
        data_str = '{' + data_str[0:-2] + '}'

        return f'CREATE (n:{label} {data_str})'

    @staticmethod
    def create_nodes(data: list[dict[str, str | int | list[str]]]) -> str:
        nodes: list[str] = []

    @staticmethod
    def __value_to_string(value: str | int | list[str]) -> str:
        v_type = type(value)
        if isinstance(value, str) or isinstance(value, int):
            return '\'' + str(value) + '\''
        elif isinstance(value, list):
            if len(value) == 0 or isinstance(value[0], str) or isinstance(value[0], int):
                return str(value)
        else:
            raise TypeError('value must be str or int or list[str | int]')
class Neo4jAccess:
    __base_url: str
    __auth_header: str

    def __init__(self, host: str, port: int, username: str, password: str):
        self.__base_url = f"http://{host}:{port}/db/data/"
        self.__auth_header = HTTPBasicAuth(username, password)

    def is_connected(self) -> bool:
        try:
            # Sending a simple GET request to the Neo4j root URL to check connectivity
            response = requests.get(self.__base_url, auth=self.__auth_header)
            # If status code is 200, the connection is successful
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            # If there's an exception during the request, connection failed
            print(f"Connection error: {e}")
            return False

