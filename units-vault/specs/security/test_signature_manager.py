from security import SignatureManager
import datetime


class TestSignatureManager:
    def test_should_sign(self):
        secret = 'my_secret'

        signature_manager = SignatureManager(secret=secret)

        generated_signature = signature_manager.sign(payload={'key': 'value'})

        assert generated_signature

        assert isinstance(generated_signature, str)

    def test_should_decode(self):
        secret = 'my_secret'

        signature_manager = SignatureManager(secret=secret)

        generated_signature = signature_manager.sign(payload={'key': 'value'})

        decoded_signature = signature_manager.decode_signature(token=generated_signature)

        assert decoded_signature['key'] == 'value'
        assert decoded_signature['iat']
        assert decoded_signature['exp']

    def test_should_verify_signature(self):
        signature_manager_one = SignatureManager(secret='secret1')

        signature_manager_two = SignatureManager(secret='secret2')

        generated_signature_one = signature_manager_one.sign()

        generated_signature_two = signature_manager_two.sign()

        assert signature_manager_one.verify_signature(token=generated_signature_one)

        assert signature_manager_two.verify_signature(token=generated_signature_two)

        assert not signature_manager_one.verify_signature(token=generated_signature_two)

        assert not signature_manager_two.verify_signature(token=generated_signature_one)

    def test_should_reject_on_expired_signature(self):
        signature_manager = SignatureManager(secret='secret1')

        generated_signature = signature_manager.sign(payload={
            'iat': int(
                datetime.datetime.now(datetime.UTC).timestamp()
            ) - datetime.timedelta(hours=3).total_seconds(),
            'exp': int(
                datetime.datetime.now(datetime.UTC).timestamp()
            ) - datetime.timedelta(hours=2).total_seconds()
        })

        assert not signature_manager.verify_signature(token=generated_signature)
