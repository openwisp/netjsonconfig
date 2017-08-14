from .mock import ConverterTest, SshdAirOs


class TestSshdConverter(ConverterTest):

    backend = SshdAirOs

    def test_with_password(self):
        o = self.backend({
            'sshd': {
                'port': 22,
                'enabled': True,
                'password_auth': True,
            },
        })
        o.to_intermediate()
        expected = [
            {
                'auth.passwd': 'enabled',
                'port': 22,
                'status': 'enabled',
            }
        ]
        self.assertEqualConfig(o.intermediate_data['sshd'], expected)

    def test_with_key(self):
        o = self.backend({
            'sshd': {
                'port': 22,
                'enabled': True,
                'password_auth': True,
                'keys': [
                    {
                        'type': 'ssh-rsa',
                        'key': 'my-public-key-here',
                        'comment': 'this is netjsonconfig pubkey',
                        'enabled': True,
                    }
                ]
            },
        })
        o.to_intermediate()
        expected = [
            {
                'auth.passwd': 'enabled',
                'auth.key.1.status': 'enabled',
                'auth.key.1.type': 'ssh-rsa',
                'auth.key.1.value': 'my-public-key-here',
                'auth.key.1.comment': 'this is netjsonconfig pubkey',
                'port': 22,
                'status': 'enabled',
            }
        ]

        self.assertEqualConfig(o.intermediate_data['sshd'], expected)
