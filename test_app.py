from unittest import TestCase


from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            # nice to not include ending tag for more flexibility
            self.assertIn('<table class="board"',html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')

            # is JSON
            self.assertTrue(response.is_json)
            # has gameID
            self.assertIn("gameId",response.get_json())
            # is game board a list-of-lists
            gameboard = response.get_json()["board"]
            game_id = response.get_json()["gameId"]
            self.assertEqual(type(gameboard),list)
            self.assertEqual(type(gameboard[0]),list)
            breakpoint()
            #the route stores the new game in the games dictionary
            self.assertIn(game_id,games)


    def test_score_word(self):
        """Test scoring word."""

        with self.client as client:
            response = client.post('/api/new-game')
            json_response = response.get_json()

            game_id = json_response["gameId"]
            game = games[game_id]
            game.board = [
                    ['E', 'I', 'A', 'N', 'K'],
                    ['G', 'L', 'S', 'N', 'I'],
                    ['O', 'N', 'M', 'T', 'J'],
                    ['C', 'B', 'O', 'O', 'Y'],
                    ['O', 'E', 'V', 'E', 'F']
                ]
            #Test valid word
            response = client.post("/api/score-word", json={
                "gameId" : game_id,
                "word-input": "MOVE"})

            json_response = response.get_json()

            self.assertEqual({"result":"ok"}, json_response)

            #Test invalid word
            response = client.post("/api/score-word", json={
                "gameId" : game_id,
                "word-input": "ZZZZ"})

            json_response = response.get_json()

            self.assertEqual({"result":"not-word"}, json_response)

            #Test word not on board
            response = client.post("/api/score-word", json={
                "gameId" : game_id,
                "word-input": "TIGER"})

            json_response = response.get_json()

            self.assertEqual({"result":"not-on-board"}, json_response)


