from app import process_new_image


class TestProcessRecord:
    @staticmethod
    def test_process_record():
        record = {
            "SK": {"S": "raw"},
            "post_text": {"S": " Deux places disponibles de mseken ou sahloul vers Tunis à 19h. num 92281064"},
            "id": {"S": "01d7e748aa1876bd62908591a946b0d1"}
        }
        res = process_new_image(record)
        assert res == {'id': '01d7e748aa1876bd62908591a946b0d1', 'loc_from': 'mseken,sahloul', 'loc_to': 'Tunis',
                       'n_seats': 'Deux', 'cov_time': '19h', 'phone': '92281064',
                       'category': 'dispo'}
