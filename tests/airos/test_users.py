from .mock import ConverterTest, UsersAirOs


class TestUsersConverter(ConverterTest):
    """
    tests for backends.airos.renderers.SystemRenderer
    """
    backend = UsersAirOs

    def test_user(self):

        o = self.backend({
            'user': {
                'name': 'ubnt',
                'password': 'changeme',
                'salt': 'goodsalt',
            }
        })
        o.to_intermediate()
        expected = [
            {
                'status': 'enabled',
            },
            {
                '1.name': 'ubnt',
                '1.password': '$1$goodsalt$changeme',
                '1.status': 'enabled',
            }
        ]

        self.assertEqualConfig(o.intermediate_data['users'], expected)
